# Generated by Django 4.0.2 on 2022-02-26 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('votes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile_M',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=10)),
                ('profile_img', models.ImageField(null=True, upload_to='profile_imgs')),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPoint_M',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_point', models.IntegerField()),
                ('last_updated_at', models.DateField()),
                ('point_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_point', to='votes.points_m')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_point', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPoint_H',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_at', models.DateField(auto_now_add=True)),
                ('amount_point', models.IntegerField()),
                ('point_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_point_history', to='votes.points_m')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_point_history', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
