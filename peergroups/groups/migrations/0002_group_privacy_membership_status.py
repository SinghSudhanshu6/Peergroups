from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='privacy',
            field=models.CharField(choices=[
                ('public', 'Public — anyone can join'),
                ('private', 'Private — leader approves who joins'),
            ], default='public', max_length=10),
        ),
        migrations.AddField(
            model_name='membership',
            name='status',
            field=models.CharField(choices=[
                ('approved', 'Approved'), ('pending', 'Pending'),
            ], default='approved', max_length=10),
        ),
    ]
