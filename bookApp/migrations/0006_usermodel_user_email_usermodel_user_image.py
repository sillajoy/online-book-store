# Generated by Django 5.0.1 on 2024-02-23 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookApp', '0005_alter_reviewmodel_review_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='user_email',
            field=models.EmailField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='user_image',
            field=models.ImageField(null=True, upload_to='user_images/'),
        ),
    ]
