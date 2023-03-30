# Generated by Django 4.0 on 2023-03-30 23:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='blog',
            name='image',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='country',
        ),
        migrations.RemoveField(
            model_name='question',
            name='image',
        ),
        migrations.AddField(
            model_name='blog',
            name='cover_picture',
            field=models.ImageField(blank=True, default='blogs/content.jpeg', upload_to='blogs/'),
        ),
        migrations.AddField(
            model_name='question',
            name='screenshot',
            field=models.ImageField(blank=True, default='/blogs/q.png', upload_to='question/'),
        ),
        migrations.AddField(
            model_name='profile',
            name='state',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='Myapp.location'),
            preserve_default=False,
        ),
    ]
