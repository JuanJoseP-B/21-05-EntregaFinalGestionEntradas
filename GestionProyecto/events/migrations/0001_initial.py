import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('direccion', models.CharField(max_length=300)),
                ('ciudad', models.CharField(max_length=100)),
                ('capacidad_maxima', models.PositiveIntegerField()),
            ],
            options={'verbose_name': 'Ubicación', 'verbose_name_plural': 'Ubicaciones'},
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('imagen_banner', models.ImageField(blank=True, null=True, upload_to='events/')),
                ('estado', models.CharField(
                    choices=[('BORRADOR', 'Borrador'), ('PUBLICADO', 'Publicado'), ('CANCELADO', 'Cancelado'), ('FINALIZADO', 'Finalizado')],
                    default='BORRADOR',
                    max_length=20,
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('organizador', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='eventos',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('ubicacion', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to='events.ubicacion',
                )),
            ],
            options={'verbose_name': 'Evento', 'verbose_name_plural': 'Eventos', 'ordering': ['-created_at']},
        ),
    ]
