# Generated by Django 2.1.4 on 2019-10-17 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_feedbackprofile_hashtagprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackprofile',
            name='Username',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='hashtagprofile',
            name='Username',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]