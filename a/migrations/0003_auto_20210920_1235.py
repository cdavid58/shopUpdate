# Generated by Django 2.2.3 on 2021-09-20 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0002_auto_20210920_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(default='Camisas 100% Personalizadas'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(default='Camisas', max_length=150),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.CharField(default=0, max_length=10),
        ),
    ]
