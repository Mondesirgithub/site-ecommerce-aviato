# Generated by Django 4.0.5 on 2022-06-13 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=128)),
                ('prix', models.FloatField(default=0.0)),
                ('description', models.TextField()),
                ('slug', models.SlugField(max_length=128)),
                ('stock', models.IntegerField(default=1)),
            ],
        ),
    ]