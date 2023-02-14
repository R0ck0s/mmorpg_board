# Generated by Django 4.1.6 on 2023-02-09 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_advert_advert_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='advert_category',
            field=models.CharField(choices=[('TK', 'Танки'), ('HL', 'Хилы'), ('DD', 'ДД'), ('DL', 'Торговцы'), ('GM', 'Гилдмастеры'), ('QG', 'Квестгиверы'), ('BS', 'Кузнецы'), ('TN', 'Кожевники'), ('PM', 'Зельевар'), ('SM', 'Мастер заклинаний')], default='TK', max_length=2),
        ),
    ]
