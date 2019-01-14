# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-01-10 15:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import geotrek.authent.models


def move_data(apps, schema_editor):
    # We can't import Infrastructure models directly as it may be a newer
    # version than this migration expects. We use the historical version.
    OldSignage = apps.get_model('infrastructure', 'Signage')
    NewSignage = apps.get_model('signage', 'Signage')
    InfrastructureType = apps.get_model('infrastructure', 'InfrastructureType')
    SignageType = apps.get_model('signage', 'SignageType')
    correspondance = {}
    for signagetype in InfrastructureType.objects.all().filter(type='S').values():
        old_key = signagetype['id']
        del signagetype['id']
        del signagetype['type']
        object_signage_type = SignageType.objects.create(**signagetype)
        new_key = object_signage_type.pk
        correspondance[old_key] = new_key
    for signage in OldSignage.objects.all().values():
        signage['type_id'] = correspondance[signage['type_id']]
        NewSignage.objects.create(**signage)
    InfrastructureType.objects.filter(type='S').delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('infrastructure', '0009_remove_base_infrastructure'),
        ('common', '0003_auto_20180608_1236'),
        ('core', '0008_aggregation_infrastructure'),
        ('authent', '0003_auto_20181203_1518'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signage',
            fields=[
                ('published', models.BooleanField(db_column=b'public', default=False, help_text='Online', verbose_name='Published')),
                ('publication_date', models.DateField(blank=True, db_column=b'date_publication', editable=False, null=True, verbose_name='Publication date')),
                ('topo_object', models.OneToOneField(db_column=b'evenement', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Topology')),
                ('name', models.CharField(db_column=b'nom', help_text='Reference, code, ...', max_length=128, verbose_name='Name')),
                ('description', models.TextField(blank=True, db_column=b'description', help_text='Specificites', verbose_name='Description')),
                ('implantation_year', models.PositiveSmallIntegerField(db_column=b'annee_implantation', null=True, verbose_name='Implantation year')),
                ('eid', models.CharField(blank=True, db_column=b'id_externe', max_length=1024, null=True, verbose_name='External id')),
                ('code', models.CharField(blank=True, db_column=b'code', max_length=250, null=True, verbose_name='Code')),
                ('printed_elevation', models.IntegerField(blank=True, db_column=b'altitude_imprimee', null=True, verbose_name='Printed Elevation')),
                ('manager', models.ForeignKey(db_column=b'gestionnaire', null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, to='common.Organism', verbose_name='Manager')),
                ('condition', models.ForeignKey(blank=True, db_column=b'etat', null=True, on_delete=django.db.models.deletion.PROTECT, to='infrastructure.InfrastructureCondition', verbose_name='Condition')),
            ],
            options={
                'db_table': 's_t_signaletique',
                'verbose_name': 'Signage',
                'verbose_name_plural': 'Signages',
            },
            bases=('core.topology', models.Model),
        ),
        migrations.CreateModel(
            name='Sealing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(db_column=b'etat', max_length=250, verbose_name='Name')),
                ('structure', models.ForeignKey(blank=True, db_column=b'structure', default=geotrek.authent.models.default_structure_pk, null=True, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure')),
            ],
            options={
                'db_table': 's_b_scellement',
                'verbose_name': 'Sealing',
                'verbose_name_plural': 'Sealings',
            },
        ),
        migrations.CreateModel(
            name='SignageType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pictogram', models.FileField(blank=True, db_column=b'picto', max_length=512, null=True, upload_to=b'upload', verbose_name='Pictogram')),
                ('label', models.CharField(db_column=b'nom', max_length=128)),
                ('structure', models.ForeignKey(blank=True, db_column=b'structure', default=geotrek.authent.models.default_structure_pk, null=True, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure')),
            ],
            options={
                'db_table': 's_b_signaletique',
                'verbose_name': 'Signage Type',
                'verbose_name_plural': 'Signage Types',
            },
        ),
        migrations.AddField(
            model_name='signage',
            name='sealing',
            field=models.ForeignKey(db_column=b'scellement', null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, to='signage.Sealing', verbose_name='Sealing'),
        ),
        migrations.AddField(
            model_name='signage',
            name='structure',
            field=models.ForeignKey(db_column=b'structure', default=geotrek.authent.models.default_structure_pk, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure'),
        ),
        migrations.AddField(
            model_name='signage',
            name='type',
            field=models.ForeignKey(db_column=b'type', on_delete=django.db.models.deletion.CASCADE, to='signage.SignageType', verbose_name='Type'),
        ),
        migrations.CreateModel(
            name='Blade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(db_column=b'numero', verbose_name='Blade Number')),
                ('type', models.CharField(db_column=b'type', max_length=250, verbose_name='Blade Type')),
            ],
            options={
                'db_table': 's_t_lame',
                'verbose_name': 'Blade',
                'verbose_name_plural': 'Blades',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(db_column=b'etiquette', max_length=128)),
            ],
            options={
                'db_table': 's_b_color',
                'verbose_name': 'Color Blade',
                'verbose_name_plural': 'Colors Blade',
            },
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(db_column=b'nombre', verbose_name='Number')),
                ('text', models.CharField(db_column=b'texte', max_length=1000, verbose_name='Text')),
                ('distance',
                 models.DecimalField(blank=True, db_column=b'distance', decimal_places=3, max_digits=8, null=True,
                                     verbose_name='Distance')),
                ('pictogram_name', models.CharField(blank=True, db_column=b'nom_pictogramme', max_length=250, null=True,
                                                    verbose_name='Name pictogramm')),
                ('time', models.DurationField(blank=True, db_column=b'temps', null=True, verbose_name='Temps')),
                ('blade',
                 models.ForeignKey(db_column=b'lame', on_delete=django.db.models.deletion.PROTECT, to='signage.Blade',
                                   verbose_name='Blade')),
                ('structure',
                 models.ForeignKey(db_column=b'structure', default=geotrek.authent.models.default_structure_pk,
                                   on_delete=django.db.models.deletion.CASCADE, to='authent.Structure',
                                   verbose_name='Related structure')),
            ],
            options={
                'db_table': 's_t_ligne',
                'verbose_name': 'Line',
                'verbose_name_plural': 'Lines',
            },
        ),
        migrations.CreateModel(
            name='Orientation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(db_column=b'etiquette', max_length=128)),
            ],
            options={
                'db_table': 's_b_orientation',
                'verbose_name': 'Orientation',
                'verbose_name_plural': 'Orientations',
            },
        ),
        migrations.AddField(
            model_name='blade',
            name='color',
            field=models.ForeignKey(blank=True, db_column=b'couleur', null=True,
                                    on_delete=django.db.models.deletion.PROTECT, to='signage.Color'),
        ),
        migrations.AddField(
            model_name='blade',
            name='condition',
            field=models.ForeignKey(blank=True, db_column=b'etat', null=True,
                                    on_delete=django.db.models.deletion.PROTECT,
                                    to='infrastructure.InfrastructureCondition', verbose_name='Condition'),
        ),
        migrations.AddField(
            model_name='blade',
            name='orientation',
            field=models.ForeignKey(db_column=b'orientation', on_delete=django.db.models.deletion.PROTECT,
                                    to='signage.Orientation', verbose_name='Orientation'),
        ),
        migrations.AddField(
            model_name='blade',
            name='signage',
            field=models.ForeignKey(db_column=b'signaletique', on_delete=django.db.models.deletion.PROTECT,
                                    to='signage.Signage', verbose_name='Signage'),
        ),
        migrations.AddField(
            model_name='blade',
            name='structure',
            field=models.ForeignKey(db_column=b'structure', default=geotrek.authent.models.default_structure_pk,
                                    on_delete=django.db.models.deletion.CASCADE, to='authent.Structure',
                                    verbose_name='Related structure'),
        ),
        migrations.RunPython(move_data),
    ]
