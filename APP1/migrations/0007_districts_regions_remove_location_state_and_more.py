# Generated by Django 4.2.16 on 2025-03-01 14:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('APP1', '0006_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Districts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dname', models.CharField(max_length=150, verbose_name='District Name')),
            ],
            options={
                'ordering': ['dname'],
            },
        ),
        migrations.CreateModel(
            name='Regions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rname', models.CharField(max_length=100, verbose_name='Region Name')),
                ('code', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'ordering': ['rname'],
            },
        ),
        migrations.RemoveField(
            model_name='location',
            name='state',
        ),
        migrations.AlterField(
            model_name='location',
            name='city',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='location',
            name='country',
            field=models.CharField(default='Tanzania', max_length=100),
        ),
        migrations.AlterField(
            model_name='location',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)]),
        ),
        migrations.AlterField(
            model_name='location',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)]),
        ),
        migrations.AlterField(
            model_name='location',
            name='zip_code',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.CreateModel(
            name='Wards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wname', models.CharField(max_length=150, verbose_name='Ward Name')),
                ('wilaya', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='APP1.districts', verbose_name='District')),
            ],
            options={
                'ordering': ['wname'],
            },
        ),
        migrations.AddField(
            model_name='districts',
            name='mkoa_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='APP1.regions', verbose_name='Region'),
        ),
        migrations.AddField(
            model_name='location',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='APP1.districts'),
        ),
        migrations.AddField(
            model_name='location',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='APP1.regions'),
        ),
        migrations.AddField(
            model_name='location',
            name='ward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='APP1.wards'),
        ),
    ]
