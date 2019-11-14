# Generated by Django 2.1.5 on 2019-11-14 22:28

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0001_revised_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataCreditLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('space_id', models.IntegerField()),
                ('ip_address', models.GenericIPAddressField()),
                ('credit', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('is_provisional', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FieldSuggestion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('field_name', models.CharField(blank=True, max_length=500, null=True)),
                ('field_suggestion', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Moderator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('province', models.CharField(blank=True, max_length=140)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('is_moderator', models.BooleanField(default=False)),
                ('is_country_moderator', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Owners',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ProvisionalSpace',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=140)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('address1', models.CharField(blank=True, max_length=255, null=True)),
                ('address2', models.CharField(blank=True, max_length=150, null=True)),
                ('city', models.CharField(blank=True, max_length=150, null=True)),
                ('province', models.CharField(blank=True, max_length=255, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=15, null=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('additional_directions', models.CharField(blank=True, max_length=255, null=True)),
                ('fhash', models.CharField(blank=True, max_length=500, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=128, null=True)),
                ('website', models.CharField(blank=True, max_length=255, null=True)),
                ('date_opened', models.DateField(blank=True, null=True)),
                ('date_closed', models.DateField(blank=True, null=True)),
                ('short_description', models.CharField(blank=True, max_length=140, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('data_credit', models.CharField(blank=True, max_length=100, null=True)),
                ('residencies', models.NullBooleanField()),
                ('membership', models.IntegerField(blank=True, null=True)),
                ('users', models.IntegerField(blank=True, null=True)),
                ('size_in_sq_meters', models.IntegerField(blank=True, null=True)),
                ('wheelchair_accessibility', models.NullBooleanField()),
                ('business_model', models.CharField(blank=True, max_length=1000, null=True)),
                ('hours_of_operation', models.CharField(blank=True, max_length=1000, null=True)),
                ('override_analysis', models.NullBooleanField()),
                ('discarded', models.NullBooleanField()),
                ('operational_status', models.CharField(blank=True, choices=[('In Operation', 'In Operation'), ('Planned', 'Planned'), ('Closed', 'Closed')], max_length=12, null=True)),
                ('validation_status', models.CharField(blank=True, choices=[('Verified', 'Verified Address and Operation Status'), ('Flagged', 'Flagged')], max_length=8, null=True)),
                ('other_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('governance_type', models.ManyToManyField(blank=True, to='application.GovernanceOption')),
                ('network_affiliation', models.ManyToManyField(blank=True, to='application.AffiliationOption')),
                ('ownership_type', models.ManyToManyField(blank=True, to='application.OwnershipOption')),
            ],
            options={
                'permissions': (('analyse_provisional_spaces', 'Grants permission to use the analyser'), ('upload_provisonal_spaces', 'Grants permission to use the uploader')),
            },
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='space',
            name='fhash',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='space',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Space'),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='owners',
            name='space',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Space'),
        ),
        migrations.AddField(
            model_name='owners',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fieldsuggestion',
            name='suggestion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Suggestion'),
        ),
    ]
