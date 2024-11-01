from django.db import migrations


def create_default_roles(apps, schema_editor):
    Role = apps.get_model('roles', 'Role')
    roles = [
        {'id': 1, 'name': 'Regular',
            'description': 'User looking for other users who share their interests.'},
        {'id': 2, 'name': 'Creator',
            'description': 'User who shares content and seeks to expand their audience.'},
        {'id': 3, 'name': 'Admin',
            'description': 'User who can manage permissions and moderate content on the platform.'},
    ]
    for role in roles:
        Role.objects.get_or_create(
            id=role['id'],
            defaults={
                'name': role['name'],
                'description': role['description'],
            }
        )


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_roles),
    ]