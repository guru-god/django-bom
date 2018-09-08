# Generated by Django 2.1.1 on 2018-09-06 02:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=128)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=255)),
                ('subscription', models.CharField(choices=[('F', 'Free'), ('P', 'Pro')], max_length=1)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_item', models.CharField(blank=True, default=None, max_length=4, validators=[django.core.validators.RegexValidator('^[0-9]*$', 'Only numeric characters are allowed.')])),
                ('number_variation', models.CharField(blank=True, default=None, max_length=2, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')])),
                ('description', models.CharField(default=None, max_length=255)),
                ('revision', models.CharField(max_length=2)),
                ('manufacturer_part_number', models.CharField(blank=True, default='', max_length=128)),
                ('manufacturer', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='bom.Manufacturer')),
            ],
        ),
        migrations.CreateModel(
            name='PartClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True)),
                ('name', models.CharField(default=None, max_length=255)),
                ('comment', models.CharField(blank=True, default=None, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PartFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='partfiles/')),
                ('upload_date', models.DateField(auto_now=True)),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bom.Part')),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=128)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bom.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='SellerPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minimum_order_quantity', models.IntegerField(blank=True, null=True)),
                ('minimum_pack_quantity', models.IntegerField(blank=True, null=True)),
                ('unit_cost', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                ('lead_time_days', models.IntegerField(blank=True, null=True)),
                ('nre_cost', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                ('ncnr', models.BooleanField(default=False)),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bom.Part')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bom.Seller')),
            ],
        ),
        migrations.CreateModel(
            name='Subpart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('assembly_part', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='assembly_part', to='bom.Part')),
                ('assembly_subpart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='assembly_subpart', to='bom.Part')),
            ],
        ),
        migrations.CreateModel(
            name='UserMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('A', 'Admin'), ('V', 'Viewer')], max_length=1)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='bom.Organization')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='part',
            name='number_class',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='number_class', to='bom.PartClass'),
        ),
        migrations.AddField(
            model_name='part',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bom.Organization'),
        ),
        migrations.AddField(
            model_name='part',
            name='subparts',
            field=models.ManyToManyField(blank=True, through='bom.Subpart', to='bom.Part'),
        ),
        migrations.AddField(
            model_name='manufacturer',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bom.Organization'),
        ),
        migrations.AlterUniqueTogether(
            name='sellerpart',
            unique_together={('seller', 'part', 'minimum_order_quantity', 'unit_cost')},
        ),
        migrations.AlterUniqueTogether(
            name='part',
            unique_together={('number_class', 'number_item', 'number_variation', 'organization')},
        ),
    ]