# Generated by Django 2.0.3 on 2018-04-01 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='company',
            name='english_company_name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='company',
            name='sector_code',
            field=models.CharField(default='', max_length=3),
        ),
        migrations.AlterField(
            model_name='company',
            name='security_code',
            field=models.CharField(default='', max_length=5),
        ),
        migrations.AlterField(
            model_name='company',
            name='stock_market',
            field=models.CharField(default='', max_length=45),
        ),
    ]
