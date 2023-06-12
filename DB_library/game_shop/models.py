from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator


class UserProfile(models.Model):
    number_regex = RegexValidator(
        regex=r'^[0-9]+$',
        message="Only numbers from 0 to 9 are allowed."
    )
    location = models.CharField(null=False, max_length=50)
    age = models.PositiveIntegerField()
    phone = models.CharField(
        max_length=10,
        validators=[number_regex]
    )
    email = models.EmailField(null=False)
    user = models.OneToOneField(null=True, to=User, on_delete=models.CASCADE)
    phonecontact = models.BooleanField(null=True,blank=True, default=False)
    emailcontact = models.BooleanField(null=True, default=False, blank=True)
    webcontact = models.BooleanField(null=True, default=False, blank=True)
    

    class Meta:
        db_table = "User Profile"

    def __str__(self):
        return f"{self.user}\n"


class Game(models.Model):
    CONSOLE_CHOICES = [
        ('PS3', 'PS3'), ('PS4', 'PS4'), ('PS5', 'PS5'),
        ('Xbox 360', 'Xbox 360'), ('Xbox One', 'Xbox One'),
        ('Xbox Series X/S', 'Xbox Series X/S'), ('Nintendo Switch', 'Nintendo Switch'),
        ('PS2', 'PS2'), ('PS ONE', 'PS ONE'), ('Wii', 'Wii'), ('PSP', 'PSP'),
        ('Game Boy', 'Game Boy'), ('Atari', 'Atari'), ('Nintendo DS', 'Nintendo DS'),
        ('Xbox Original', 'Xbox Original'), ('PC', 'PC')
    ]

    GAME_TYPE_CHOICES = [
        ('New', 'New'),
        ('Old', 'Old'),
    ]

    game_type = models.CharField(max_length=3, choices=GAME_TYPE_CHOICES)
    console = models.CharField(max_length=15, null=False, blank=False)
    game_name = models.CharField(null=False, max_length=50)
    price = models.PositiveIntegerField(null=False)
    game_img = models.ImageField(null=True, blank=True, upload_to="images/")
    uploader = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "Games"

    def __str__(self):
        return f"{self.game_type} - {self.console} - {self.game_name} (Uploader: 		{self.uploader.user.username} - {self.uploader.location})"


class ContactMsg(models.Model):
    subject = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)
    email = models.EmailField()
    status = models.CharField(max_length=20, choices=[('in_progress', 'In Progress'), ('completed', 'Completed')])
    sent_time = models.DateTimeField(default=timezone.now)
    last_edited_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Mail"
        verbose_name_plural = "Mail"

    def __str__(self):
        return f"{self.sent_time} - {self.subject} - {self.email}"


class Message(models.Model):
    sender = models.CharField(max_length=15, null=False, blank=False)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=20)
    content = models.TextField()
    email = models.CharField(max_length=254, null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = "Message"


