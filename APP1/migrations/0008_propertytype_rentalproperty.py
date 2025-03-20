# Generated by Django 4.2.16 on 2025-03-01 16:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('APP1', '0007_districts_regions_remove_location_state_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RentalProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=20)),
                ('latitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('place_id', models.CharField(blank=True, help_text='Google Maps Place ID', max_length=255, null=True)),
                ('number_of_rooms', models.IntegerField()),
                ('monthly_rent', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('available', 'Available'), ('occupied', 'Occupied'), ('under_maintenance', 'Under Maintenance')], default='available', max_length=20)),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='APP1.districts')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_properties', to=settings.AUTH_USER_MODEL)),
                ('property_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='APP1.propertytype')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='APP1.regions')),
                ('ward', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='APP1.wards')),
            ],
        ),
    ]
