from threading import Thread


class SendEmailThread(Thread):
    """a Threading for sending emails"""

    def __init__(self, email):
        self.email = email

    def run(self):
        """sending email"""
        self.email.send()
