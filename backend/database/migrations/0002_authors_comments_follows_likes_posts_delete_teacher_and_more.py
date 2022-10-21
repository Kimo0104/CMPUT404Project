# Generated by Django 4.1.2 on 2022-10-21 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=255)),
                ('display_name', models.CharField(max_length=32)),
                ('github_url', models.CharField(blank=True, max_length=255, null=True)),
                ('profile_image', models.CharField(blank=True, max_length=255, null=True)),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('accepted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.authors')),
            ],
        ),
        migrations.CreateModel(
            name='Follows',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship_state', models.IntegerField(choices=[(0, 'Pending'), (1, 'Following')], default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='database.authors')),
                ('foreign_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed', to='database.authors')),
            ],
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.authors')),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description_type', models.CharField(blank=True, choices=[('PT', 'PLAINTEXT'), ('CM', 'COMMONMARK')], default='PT', max_length=2, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField()),
                ('image_url', models.CharField(blank=True, max_length=255, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.authors')),
            ],
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
        migrations.AddField(
            model_name='likes',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.posts'),
        ),
        migrations.AddField(
            model_name='comments',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.posts'),
        ),
    ]
