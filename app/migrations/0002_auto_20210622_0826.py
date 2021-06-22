# Generated by Django 3.2 on 2021-06-22 08:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='dislikes',
            field=models.ManyToManyField(null=True, related_name='answers_dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='answer',
            name='likes',
            field=models.ManyToManyField(null=True, related_name='answers_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='dislikes',
            field=models.ManyToManyField(null=True, related_name='question_dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='likes',
            field=models.ManyToManyField(null=True, related_name='question_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
