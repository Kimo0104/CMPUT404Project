# Generated by Django 4.1.2 on 2022-10-22 23:32

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
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('type', models.CharField(default='author', max_length=255)),
                ('host', models.CharField(max_length=255)),
                ('displayName', models.CharField(max_length=32)),
                ('url', models.CharField(max_length=255)),
                ('github', models.CharField(max_length=255)),
                ('accepted', models.BooleanField(default=False)),
                ('profileImage', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('type', models.CharField(default='comment', max_length=16)),
                ('comment', models.CharField(max_length=255)),
                ('contentType', models.CharField(choices=[('text/plain', 'PLAINTEXT'), ('text/markdown', 'MARKDOWN')], default='text/plain', max_length=15)),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.authors')),
            ],
        ),
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('followed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='database.authors')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed', to='database.authors')),
            ],
        ),
        migrations.CreateModel(
            name='FollowRequests',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('reciever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reciever', to='database.authors')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester', to='database.authors')),
            ],
        ),
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.authors')),
            ],
        ),
        migrations.CreateModel(
            name='Liked',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.authors')),
            ],
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('context', models.CharField(max_length=255)),
                ('summary', models.CharField(max_length=64)),
                ('type', models.CharField(default='like', max_length=16)),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.authors')),
            ],
        ),
        migrations.CreateModel(
            name='LikesComments',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('context', models.CharField(max_length=255)),
                ('summary', models.CharField(max_length=64)),
                ('type', models.CharField(default='likescomment', max_length=16)),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.authors')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.comments')),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('type', models.CharField(default='post', max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('source', models.CharField(max_length=255)),
                ('origin', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('contentType', models.CharField(choices=[('text/plain', 'PLAINTEXT'), ('text/markdown', 'COMMONMARK')], default='text/plain', max_length=15)),
                ('content', models.TextField()),
                ('count', models.IntegerField(default=0)),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('visibility', models.CharField(choices=[('PUBLIC', 'PUBLIC'), ('FRIENDS', 'FRIENDS')], default='PUBLIC', max_length=8)),
                ('unlisted', models.BooleanField(default=False)),
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
            model_name='liked',
            name='like',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.likes'),
        ),
        migrations.AddField(
            model_name='inbox',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.posts'),
        ),
        migrations.AddField(
            model_name='comments',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.posts'),
        ),
    ]
