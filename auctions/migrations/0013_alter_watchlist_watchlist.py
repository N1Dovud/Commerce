# Generated by Django 5.0 on 2024-01-16 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_watchlist_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watchlists', to='auctions.listing'),
        ),
    ]
