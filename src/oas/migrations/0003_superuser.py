import os
from django.db import migrations


_SQL = """
INSERT INTO auth_user
(password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) 
VALUES ('%s', true, 'oas' , '', '', 'oas@nowhere.ch', true, true, now());
""" % ('pbkdf2_sha256$120000$%s=' % os.getenv('DJANGO_SUPERUSER_PASSWORD'))


class Migration(migrations.Migration):

    dependencies = [
        ('oas', '0002_ref_data'),
    ]

    operations = [
        migrations.RunSQL(_SQL),
    ]
