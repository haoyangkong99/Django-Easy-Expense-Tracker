# Generated by Django 4.2.1 on 2023-08-18 15:26

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Mode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.TextField(null=True)),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('note', models.TextField()),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='expense_tracker.category')),
                ('mode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='expense_tracker.mode')),
            ],
        ),
    ]
