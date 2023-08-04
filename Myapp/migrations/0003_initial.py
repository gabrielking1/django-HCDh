# Generated by Django 4.0 on 2023-03-31 00:01

import autoslug.fields
import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Myapp', '0002_remove_answer_liker_remove_answer_question_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(max_length=1000)),
                ('likes', models.IntegerField(default=0)),
                ('slug', models.SlugField(max_length=200, null=True, unique=True)),
                ('liker', models.ManyToManyField(related_name='answer_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Myapp_answer',
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('cover_picture', models.ImageField(blank=True, default='blogs/content.jpeg', upload_to='blogs/')),
                ('body', ckeditor.fields.RichTextField()),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True)),
                ('views', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=15)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=25)),
                ('message', models.TextField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=25)),
                ('user', models.CharField(max_length=25)),
                ('topic', models.CharField(max_length=25)),
                ('notify', models.CharField(max_length=100)),
                ('ids', models.CharField(max_length=100)),
                ('isread', models.CharField(choices=[('Read', 'Read'), ('Unread', 'Unread')], default='Unread', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=15)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='tag', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('culprit', models.CharField(max_length=20)),
                ('content', models.TextField(max_length=1000)),
                ('screenshot', models.ImageField(blank=True, upload_to='report/')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('in progress', 'Inprogess'), ('Treated', 'Treated')], default='Pending', max_length=30)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Myapp.type')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('screenshot', models.ImageField(blank=True, default='/blogs/q.png', upload_to='question/')),
                ('body', models.TextField(max_length=5000)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, max_length=100, populate_from='title', unique=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Myapp.tag')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(upload_to='profilePic/')),
                ('bio', models.CharField(max_length=1000)),
                ('phone', models.CharField(max_length=11)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Myapp.location')),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='LikeContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Myapp.blog')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Myapp.answer')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField(max_length=1000)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Myapp.blog')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='BlogView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_at', models.DateTimeField(auto_now_add=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Myapp.blog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog', to='Myapp.category'),
        ),
        migrations.AddField(
            model_name='blog',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Myapp.question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]
