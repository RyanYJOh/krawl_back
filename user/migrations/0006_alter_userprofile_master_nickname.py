# Generated by Django 4.0.2 on 2022-03-18 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_userprofile_master_nickname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile_master',
            name='nickname',
            field=models.CharField(default='스티븐 #537', max_length=10),
        ),
    ]
