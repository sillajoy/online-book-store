# Generated by Django 5.0.1 on 2024-02-20 04:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookApp', '0003_reviewmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewmodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bookApp.usermodel'),
        ),
    ]
