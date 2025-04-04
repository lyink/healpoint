# Generated by Django 4.2.16 on 2025-03-03 12:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('APP1', '0008_propertytype_rentalproperty'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='property_images/%Y/%m/', verbose_name='Image')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Title')),
                ('alt_text', models.CharField(blank=True, help_text='Alternative text for accessibility', max_length=255, verbose_name='Alt Text')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('is_primary', models.BooleanField(default=False, help_text='Set as the main image for this property', verbose_name='Primary Image')),
                ('display_order', models.PositiveIntegerField(default=0, help_text='Order in which images are displayed (lowest first)', verbose_name='Display Order')),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Uploaded At')),
                ('category', models.CharField(blank=True, choices=[('exterior', 'Exterior'), ('interior', 'Interior'), ('kitchen', 'Kitchen'), ('bathroom', 'Bathroom'), ('bedroom', 'Bedroom'), ('living_area', 'Living Area'), ('view', 'View'), ('other', 'Other')], max_length=50, verbose_name='Category')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='APP1.rentalproperty', verbose_name='Property')),
            ],
            options={
                'verbose_name': 'Property Image',
                'verbose_name_plural': 'Property Images',
                'ordering': ['display_order', 'uploaded_at'],
            },
        ),
    ]
