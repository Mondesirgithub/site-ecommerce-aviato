# Generated by Django 4.0.5 on 2022-06-15 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0003_remove_utilisateur_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='comptes/utilisateurs'),
        ),
    ]
