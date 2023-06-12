from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    location = models.CharField(null=False, max_length=50)
    age = models.PositiveIntegerField()
    phone = models.PositiveIntegerField(null=False)
    email = models.EmailField(null=False)
    user = models.OneToOneField(null=True, to=User, on_delete=models.CASCADE)

    class Meta:
        db_table = "User Profile"

    def __str__(self):
        return f"{self.user}\n"


class Game(models.Model):
    GAME_TYPE_CHOICES = (
        ('new', 'New'),
        ('old', 'Old'),
    )

    NEW_CONSOLE_CHOICES = (
        ('PS3', 'PS3'), ('PS4', 'PS4'), ('PS5', 'PS5'),
        ('Xbox 360', 'Xbox 360'), ('Xbox One', 'Xbox One'),
        ('Xbox Series X/S', 'Xbox Series X/S'), ('Nintendo Switch', 'Nintendo Switch')
    )

    OLD_CONSOLE_CHOICES = (
        ('PS2', 'PS2'), ('PS ONE', 'PS ONE'), ('Wii', 'Wii'), ('PSP', 'PSP'),
        ('Game Boy', 'Game Boy'), ('Atari', 'Atari'), ('Nintendo DS', 'Nintendo DS'),
        ('Xbox Original', 'Xbox Original'), ('PC', 'PC')
    )

    game_type = models.CharField(max_length=3, choices=GAME_TYPE_CHOICES, null=False, blank=False)
    console = models.CharField(max_length=15, choices=NEW_CONSOLE_CHOICES, null=False, blank=False)
    game_name = models.CharField(null=False, max_length=50)
    price = models.PositiveIntegerField(null=False)
    game_img = models.ImageField(null=True, blank=True, upload_to="images/")
    uploader = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "Game"

    def __str__(self):
        return f"{self.console}, {self.game_name}"



class Game(models.Model):
    CONSOLE_CHOICES = (
        ('PS3', 'PS3'), ('PS4', 'PS4'), ('PS5', 'PS5'),
        ('Xbox 360', 'Xbox 360'), ('Xbox One', 'Xbox One'),
        ('Xbox Series X/S', 'Xbox Series X/S'), ('Nintendo Switch', 'Nintendo Switch'))

    console = models.CharField(max_length=15, choices=CONSOLE_CHOICES, null=False, blank=False)
    game_name = models.CharField(null=False, max_length=50)
    price = models.PositiveIntegerField(null=False)
    game_img = models.ImageField(null=True, blank=True, upload_to="images/")
    uploader = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "Game"

    def __str__(self):
        return f"{self.console , self.game_name}"


class OldSchool(models.Model):
    CONSOLE_CHOICES = (
        ('PS2', 'PS2'), ('PS ONE', 'PS ONE'), ('Wii', 'Wii'), ('PSP', 'PSP'),
        ('Game Boy', 'Game Boy'), ('Atari', 'Atari'), ('Nintendo DS', 'Nintendo DS'),
        ('Xbox Original', 'Xbox Original'), ('PC', 'PC')
    )

    console = models.CharField(max_length=13, choices=CONSOLE_CHOICES, null=False, blank=False)
    game_name = models.CharField(null=False, max_length=50)
    price = models.PositiveIntegerField(null=False)
    game_img = models.ImageField(null=True, blank=True, upload_to="images/")
    uploader = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "Old School"

    def __str__(self):
        return f"{self.console , self.game_name}"



# class MessageUser(models.Model):
#     subject = models.CharField(max_length=100)
#     body = models.CharField(max_length=1000)
#     email = models.EmailField()
#     sent_time = models.DateTimeField(default=timezone.now)
#     user = models.OneToOneField(to=User, on_delete=models.CASCADE)
#     unread_count = models.IntegerField(default=0)
    
#     def __str__(self):
#         return f"Inbox for {self.user.username}"