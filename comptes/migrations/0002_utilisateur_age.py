# Generated by Django 4.0.5 on 2022-06-14 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='age',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]
