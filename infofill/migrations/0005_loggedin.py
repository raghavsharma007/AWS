# Generated by Django 2.2.3 on 2019-07-25 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infofill', '0004_fillup_client_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoggedIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('role', models.CharField(choices=[('Sales', 'Sales'), ('Sales Approver', 'Sales Approver'), ('IT Approver', 'IT Approver'), ('OPS Approver', 'OPS Approver')], max_length=50)),
            ],
        ),
    ]