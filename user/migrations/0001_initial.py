# Generated by Django 3.0.8 on 2020-09-12 12:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to='product.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'wishlist',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.FloatField(verbose_name='quantity')),
                ('price', models.FloatField(help_text='price per quantity', verbose_name='price')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Active'), (0, 'Deactive')], default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='order', to='product.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.FloatField(default=1.0, validators=[django.core.validators.MinValueValidator(0.1), django.core.validators.MaxValueValidator(5.0)], verbose_name='star')),
                ('comment', models.CharField(max_length=250, verbose_name='comment')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Active'), (0, 'Deactive')], default=1)),
                ('read_status', models.PositiveSmallIntegerField(choices=[(0, 'Checked'), (1, 'Not Checked')], default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'feedback',
            },
        ),
        migrations.CreateModel(
            name='Compare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ManyToManyField(blank=True, related_name='compare', to='product.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compare', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'compare',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.FloatField(verbose_name='quantity')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='product.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cart',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_type', models.CharField(choices=[('billing', 'Billing'), ('shipping', 'Shipping')], default='billing', max_length=10)),
                ('first_name', models.CharField(blank=True, max_length=30, validators=[django.core.validators.RegexValidator('^[a-zA-Z]*$', 'Enter Only Characters')], verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, validators=[django.core.validators.RegexValidator('^[a-zA-Z]*$', 'Enter Only Characters')], verbose_name='last name')),
                ('company_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='company name')),
                ('appartment', models.CharField(max_length=20, verbose_name='appartment')),
                ('street_address', models.CharField(max_length=150, verbose_name='street address')),
                ('city', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('^[a-zA-Z]*$', 'Enter Only Characters')], verbose_name='city')),
                ('country', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('^[a-zA-Z]*$', 'Enter Only Characters')], verbose_name='country')),
                ('pin_code', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator('^[0-9]*$', 'Enter Only Numeric Value')], verbose_name='pin code')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'address',
            },
        ),
    ]