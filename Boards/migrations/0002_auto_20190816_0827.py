# Generated by Django 2.2.4 on 2019-08-16 08:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Boards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
