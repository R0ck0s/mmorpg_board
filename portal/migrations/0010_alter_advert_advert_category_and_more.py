# Generated by Django 4.1.6 on 2023-02-14 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0009_alter_advert_advert_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='advert_category',
            field=models.ForeignKey(choices=[('TK', 'Танки'), ('HL', 'Хилы'), ('DD', 'ДД'), ('DL', 'Торговцы'), ('GM', 'Гилдмастеры'), ('QG', 'Квестгиверы'), ('BS', 'Кузнецы'), ('TN', 'Кожевники'), ('PM', 'Зельевар'), ('SM', 'Мастер заклинаний')], on_delete=django.db.models.deletion.CASCADE, to='portal.category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(default='TK', max_length=2),
        ),
    ]