# Generated by Django 2.0 on 2019-05-10 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_room_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='profile_picture',
            field=models.ImageField(default='images/room.png', upload_to='room_img/'),
        ),
    ]
