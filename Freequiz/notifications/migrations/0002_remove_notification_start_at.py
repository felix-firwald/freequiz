# Generated by Django 3.2.16 on 2022-10-10 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='start_at',
        ),
    ]