# Generated by Django 4.1.7 on 2023-04-07 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='date_published',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Blog',
        ),
    ]