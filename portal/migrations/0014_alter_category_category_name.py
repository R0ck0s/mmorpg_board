# Generated by Django 4.1.6 on 2023-02-14 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0013_alter_advert_advert_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=255),
        ),
    ]
