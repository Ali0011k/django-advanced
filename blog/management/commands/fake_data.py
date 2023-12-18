from io import StringIO
from typing import Any
from django.core.management.base import BaseCommand
from faker import Faker

class Command(BaseCommand):
    """a custom commans in fake data"""
    
    help = "insert fake data"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faker = Faker()
    
    def handle(self, *args, **kwargs):
        self.stdout.write(self.faker.name(), self.style.ERROR)
