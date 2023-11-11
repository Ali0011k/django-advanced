from accounts.models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import *
from rest_framework.filters import OrderingFilter, SearchFilter
from accounts.api.v1.serializers import *
from accounts.api.v1.permissions import IsAdminOrOwner
from accounts.api.v1.paginations import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.conf import settings
from mail_templated import send_mail
from mail_templated import EmailMessage
from accounts.api.utils import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import *
import jwt


class UserModelViewSet(ModelViewSet):
    """a model view set for user model"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["is_active", "is_staff", "is_superuser"]
    search_fields = ["email"]
    ordering_fields = ["id", "is_active", "is_staff", "is_superuser"]
    pagination_class = UserPagination


class ProfileModelViewSet(ModelViewSet):
    """a model view set for profile model"""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrOwner]
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ["user", "first_name", "last_name"]
    ordering_fields = ["id"]
    pagination_class = ProfilePagination


class CustomGetAuthToken(ObtainAuthToken):
    """a custom view for see user's token and create a new token (for know it see the inheritances)"""

    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"email": user.email, "token": token.key})


class UpdateAuthToken(APIView):
    """delete user's token and replace it with a new token"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.auth_token.delete()
        token, created = Token.objects.get_or_create(user=user)
        return Response({"email": user.email, "token": token.key})


class CustomTokenObtainPairView(TokenObtainPairView):
    """custom jwt view for getting or creating jwt tokens for user"""

    serializer_class = CustomTokenObtainPairSerializer


class ChangePassword(generics.GenericAPIView):
    """a view for changing user's password"""

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """getting user from request instead of url query params"""
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        """updateing user's password"""
        serializer = self.serializer_class(data=request.data)
        self.object = self.get_object()

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": "password does not correct"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                validate_password(serializer.data.get("new_password1"), self.object)
            except DjangoValidationError as e:
                return Response(
                    {"detail": list(e.messages)}, status=status.HTTP_400_BAD_REQUEST
                )

            self.object.set_password(serializer.data.get("new_password1"))
            self.object.save()
            return Response(
                {"detail": "password has been changed"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendTestEmail(generics.GenericAPIView):
    """sends console email"""

    serializer_class = None

    def get(self, request, *args, **kwargs):
        # send_mail('email/mail.html', {'name': 'ali'}, 'admin@admin.com', ['test@test.com'])
        email = EmailMessage(
            "email/mail.html", {"name": "ali"}, "admin@admin.com", to=["test@test.com"]
        )
        # email.send()
        SendEmailThread(email=email).start

        return Response(
            {
                "details": "email sent",
            }
        )


class SendVerificationEmailApiView(generics.GenericAPIView):
    """sends email Verification for user"""

    serializer_class = VerifyUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        token = self.get_token_for_user(user=user)
        link = str(
            request.build_absolute_uri().replace(
                "send-verification-email/", "verify-account/"
            )
            + token
        )

        email = EmailMessage(
            "email/token_email.html",
            {"name": user, "link": link},
            "admin@admin.com",
            to=["test@test.com"],
        )
        email.send()
        return Response({"detail": "email sent", "email": user.email})

    @classmethod
    def get_token_for_user(self, user):
        token = RefreshToken.for_user(user)
        return str(token.access_token)


class VerifyAccount(APIView):
    """verifys account with given json web token"""

    def get(self, request, token, *args, **kwargs):
        try:
            decoded_token = jwt.decode(
                token,
                settings.SIMPLE_JWT["SIGNING_KEY"],
                settings.SIMPLE_JWT["ALGORITHM"],
            )
        except:
            return Response(
                {"detail": "your token is invalid or expierd"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = User.objects.get(pk=decoded_token.get("user_id"))

        if user.is_verified:
            return Response({"detail": "your account already verified"})

        user.is_verified = True
        user.save()

        return Response({"detail": "your account has been verified"})
