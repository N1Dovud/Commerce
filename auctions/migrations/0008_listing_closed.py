# Generated by Django 5.0 on 2024-01-15 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_comment_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='closed',
            field=models.BooleanField(default=True),
        ),
    ]