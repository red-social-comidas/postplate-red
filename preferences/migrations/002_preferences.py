from django.db import migrations


def create_default_preferences(apps, schema_editor):
    Preference = apps.get_model('preferences', 'Preferences')
    preferences = [{'name': 'Salado'}, {'name': 'Dulce'}, {
        'name': 'Ácido'}, {'name': 'Picante'}, {'name': 'Amargo'}, {'name': 'Umami'}, {'name': 'Crujiente'}, {'name': 'Cremoso'}, {'name': 'Suave'}, {'name': 'Jugoso'}, {'name': 'Seco'}, {'name': 'Masticable'}, {'name': 'Frio'}, {'name': 'Caliente'}, {'name': 'Tibio'}]

    for preference in preferences:
        Preference.objects.get_or_create(
            name=preference['name'],
            defaults={'name': preference['name']}
        )


class Migration(migrations.Migration):

    dependencies = [
        ('preferences', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_preferences),
    ]
