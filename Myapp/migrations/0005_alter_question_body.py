# Generated by Django 4.0 on 2023-05-04 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0004_blog_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='body',
            field=models.TextField(max_length=100000),
        ),
    ]
