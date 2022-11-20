# Generated by Django 4.1.3 on 2022-11-19 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0010_remove_report_selling_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='reporttype',
            name='name',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='seller',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='report',
            unique_together={('date', 'seller', 'brand', 'report_type')},
        ),
    ]