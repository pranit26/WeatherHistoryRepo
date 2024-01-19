# Generated by Django 4.2.9 on 2024-01-18 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0005_alter_user_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=250, unique=True)),
                ('password', models.TextField(db_column='password', max_length=250)),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]