# Generated by Django 3.1.5 on 2021-03-10 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookMng', '0002_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='web',
            field=models.URLField(null=True),
        ),
    ]
