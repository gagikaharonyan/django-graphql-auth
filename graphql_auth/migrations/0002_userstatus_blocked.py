# Generated by Django 4.0.5 on 2022-06-12 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphql_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstatus',
            name='blocked',
            field=models.BooleanField(default=False),
        ),
    ]
