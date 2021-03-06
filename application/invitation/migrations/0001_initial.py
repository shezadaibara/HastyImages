# Generated by Django 2.1.7 on 2019-08-27 04:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('token', models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False, verbose_name='Token')),
                ('email', models.EmailField(max_length=100, verbose_name='Email')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Create Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
                ('expires_at', models.DateTimeField(verbose_name='Expire Date')),
            ],
            options={
                'verbose_name': 'Invitation',
                'verbose_name_plural': 'Invitations',
            },
        ),
    ]
