# Generated by Django 2.1.7 on 2019-04-08 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('client', 'client'), ('stylist', 'stylist'), ('admin', 'admin')], default='stylist', max_length=7),
        ),
    ]
