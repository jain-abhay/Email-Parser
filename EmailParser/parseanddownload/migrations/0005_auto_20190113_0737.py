# Generated by Django 2.1.5 on 2019-01-13 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parseanddownload', '0004_auto_20190113_0045'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='talksdata',
            unique_together={('Sender', 'Subject', 'DateofEmail', 'DateofWorkshop', 'Message_body', 'Venue', 'Time', 'DateofWorkshop', 'Topic')},
        ),
    ]
