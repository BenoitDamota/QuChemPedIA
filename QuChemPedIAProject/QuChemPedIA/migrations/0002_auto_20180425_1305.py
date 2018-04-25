# Generated by Django 2.0 on 2018-04-25 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuChemPedIA', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='query',
            old_name='homo',
            new_name='homo_alpha_energy',
        ),
        migrations.RenameField(
            model_name='query',
            old_name='lumo',
            new_name='homo_beta_energy',
        ),
        migrations.AddField(
            model_name='query',
            name='lumo_alpha_energy',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='query',
            name='lumo_beta_energy',
            field=models.FloatField(default=None, null=True),
        ),
    ]
