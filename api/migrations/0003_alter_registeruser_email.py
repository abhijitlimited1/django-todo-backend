# Generated by Django 5.1.1 on 2024-10-02 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_pssword_registeruser_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeruser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
