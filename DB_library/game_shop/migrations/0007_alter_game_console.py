# Generated by Django 4.2 on 2023-05-19 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_shop', '0006_alter_game_uploader'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='console',
            field=models.CharField(choices=[], max_length=15),
        ),
    ]
