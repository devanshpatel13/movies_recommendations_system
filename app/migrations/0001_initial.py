# Generated by Django 4.0.6 on 2022-07-29 07:15

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MoviesUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_login', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='MoviesDataBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=500)),
                ('Year', models.CharField(max_length=500)),
                ('Duration', models.CharField(max_length=500)),
                ('Rating', models.CharField(max_length=500)),
                ('MetaScore', models.CharField(max_length=500)),
                ('Vote', models.CharField(max_length=500)),
                ('Gross', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='MoviesDataModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('budget', models.FloatField()),
                ('genres', models.CharField(max_length=500)),
                ('homepage', models.CharField(max_length=500, null=True)),
                ('keywords', models.CharField(max_length=500)),
                ('original_language', models.CharField(max_length=500)),
                ('original_title', models.CharField(max_length=500)),
                ('overview', models.CharField(max_length=500, null=True)),
                ('popularity', models.IntegerField()),
                ('production_companies', models.CharField(max_length=500)),
                ('production_countries', models.CharField(max_length=500)),
                ('release_date', models.CharField(blank=True, max_length=100, null=True)),
                ('revenue', models.FloatField()),
                ('runtime', models.FloatField(max_length=500, null=True)),
                ('spoken_languages', models.CharField(max_length=500)),
                ('status', models.IntegerField()),
                ('tagline', models.CharField(max_length=500, null=True)),
                ('title', models.CharField(max_length=500)),
                ('vote_average', models.IntegerField()),
                ('vote_count', models.IntegerField()),
                ('movie_id', models.IntegerField()),
                ('cast', models.CharField(max_length=1000)),
                ('crew', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='SearchMoviesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_movie_name', models.CharField(max_length=500)),
                ('search_movie_date', models.CharField(blank=True, max_length=100, null=True)),
                ('search_movie_cast', models.CharField(max_length=500)),
                ('search_movie_crew', models.CharField(max_length=500)),
                ('search_movie_overview', models.CharField(max_length=500, null=True)),
                ('search_movie_popularity', models.IntegerField()),
                ('search_movies_vote_average', models.CharField(max_length=500)),
                ('search_movies_vote_count', models.CharField(max_length=500)),
                ('search_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
