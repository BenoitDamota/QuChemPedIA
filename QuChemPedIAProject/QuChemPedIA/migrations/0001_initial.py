# Generated by Django 2.0.5 on 2018-07-25 05:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImportFile',
            fields=[
                ('id_file', models.BigAutoField(primary_key=True, serialize=False)),
                ('path_file', models.FilePathField(default=None)),
                ('status', models.CharField(default='stand-by', max_length=100)),
                ('is_opt', models.BooleanField(default=False)),
                ('is_opt_es_et', models.BooleanField(default=False)),
                ('is_freq', models.BooleanField(default=False)),
                ('is_freq_es_et', models.BooleanField(default=False)),
                ('is_sp', models.BooleanField(default=False)),
                ('is_td', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'imported file',
            },
        ),
        migrations.CreateModel(
            name='ImportRule',
            fields=[
                ('id_rule', models.BigAutoField(primary_key=True, serialize=False)),
                ('rule', models.CharField(default='manual', max_length=40)),
            ],
            options={
                'verbose_name': 'rule of import',
            },
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('id_job_type', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default=None, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id_software', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default=None, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SoftwareVersion',
            fields=[
                ('id_version', models.BigAutoField(primary_key=True, serialize=False)),
                ('version_number', models.CharField(default=None, max_length=40)),
                ('id_software', models.OneToOneField(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='QuChemPedIA.Software')),
            ],
            options={
                'verbose_name': 'software version',
            },
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(default=None, max_length=255, unique=True, verbose_name='email address')),
                ('group', models.CharField(default='user', max_length=50)),
                ('last_name', models.CharField(default=None, max_length=150, null=True)),
                ('first_name', models.CharField(default=None, max_length=200, null=True)),
                ('affiliation', models.TextField(default=None, null=True)),
                ('city', models.TextField(default=None, null=True)),
                ('country', models.TextField(default=None, null=True)),
                ('orcid', models.CharField(default=None, max_length=19, null=True)),
                ('last_date_upload', models.DateField(default=None, null=True)),
                ('number_of_upload_this_day', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='importrule',
            name='id_job_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='QuChemPedIA.JobType'),
        ),
        migrations.AddField(
            model_name='importrule',
            name='id_software',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='QuChemPedIA.Software'),
        ),
        migrations.AddField(
            model_name='importrule',
            name='id_version',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='QuChemPedIA.SoftwareVersion'),
        ),
        migrations.AddField(
            model_name='importfile',
            name='id_job_type',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='QuChemPedIA.JobType'),
        ),
        migrations.AddField(
            model_name='importfile',
            name='id_software',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='QuChemPedIA.Software'),
        ),
        migrations.AddField(
            model_name='importfile',
            name='id_user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='importfile',
            name='id_version',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='QuChemPedIA.SoftwareVersion'),
        ),
    ]