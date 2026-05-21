import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrecioCategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cantidad_disponible', models.PositiveIntegerField()),
                ('evento', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='categorias',
                    to='events.evento',
                )),
            ],
            options={'verbose_name': 'Categoría de precio', 'verbose_name_plural': 'Categorías de precio'},
        ),
    ]
