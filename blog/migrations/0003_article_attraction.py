# Generated by Django 3.2 on 2022-03-04 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_comment_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='attraction',
            field=models.CharField(default='Attraction', max_length=200, unique=True),
        ),
    ]
