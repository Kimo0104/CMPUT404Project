# Generated by Django 4.1.2 on 2022-10-25 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_authors_comments_followers_followrequests_inbox_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authors',
            name='github',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
