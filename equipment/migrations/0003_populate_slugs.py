from django.db import migrations
from django.utils.text import slugify

def populate_slugs(apps, schema_editor):
    Equipment = apps.get_model('equipment', 'Equipment')
    for eq in Equipment.objects.all():
        if not eq.slug:
            base_slug = slugify(f"{eq.name}-{eq.inv_num}")
            if not base_slug:
                base_slug = f"equipment-{eq.inv_num}"
            
            eq.slug = base_slug
            eq.save(update_fields=['slug'])

class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0002_equipment_slug_alter_equipment_inv_num_and_more'), # Проверьте номер вашей предыдущей миграции
    ]

    operations = [
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
    ]
