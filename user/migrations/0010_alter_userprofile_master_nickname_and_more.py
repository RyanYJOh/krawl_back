# Generated by Django 4.0.2 on 2022-03-18 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_alter_userprofile_master_nickname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile_master',
            name='nickname',
            field=models.CharField(default='스티븐 #230', max_length=10),
        ),
        migrations.AlterField(
            model_name='userprofile_master',
            name='profile_img',
            field=models.ImageField(blank=True, default='profile_imgs/strange_uchtn8.jpg', null=True, upload_to='profile_imgs'),
        ),
    ]