# Generated by Django 4.1.2 on 2022-11-25 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authors',
            name='displayName',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='authors',
            name='profileImage',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='posts',
            name='contentType',
            field=models.CharField(choices=[('text/plain', 'PLAINTEXT'), ('text/markdown', 'COMMONMARK'), ('image', 'IMAGE')], default='text/plain', max_length=15),
        ),
    ]
