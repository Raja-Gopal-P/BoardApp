# Generated by Django 2.2.4 on 2019-08-21 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Boards', '0002_auto_20190816_0827'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='topic',
            name='subject',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
