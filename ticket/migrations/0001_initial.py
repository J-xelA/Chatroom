# Generated by Django 2.0.13 on 2022-02-16 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TicketEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=128)),
                ('entry', models.CharField(max_length=65536)),
                ('status', models.BooleanField(default=False)),
                ('name', models.CharField(default='anon', max_length=128)),
            ],
        ),
    ]
