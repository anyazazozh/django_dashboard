# Generated by Django 4.1.3 on 2022-11-12 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_dt', models.DateField()),
                ('turnover', models.DecimalField(decimal_places=2, max_digits=10)),
                ('margin', models.DecimalField(decimal_places=2, max_digits=10)),
                ('selling_type', models.CharField(max_length=10)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.brand')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.seller')),
            ],
        ),
    ]
