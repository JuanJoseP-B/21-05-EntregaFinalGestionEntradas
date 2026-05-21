import uuid
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_unico', models.CharField(default=uuid.uuid4, max_length=50, unique=True)),
                ('pagado', models.BooleanField(default=False)),
                ('usado', models.BooleanField(default=False)),
                ('fecha_compra', models.DateTimeField(auto_now_add=True)),
                ('fecha_uso', models.DateTimeField(blank=True, null=True)),
                ('codigo_qr', models.ImageField(blank=True, null=True, upload_to='qr/')),
                ('asistente', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='entradas',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('categoria', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='entradas',
                    to='events.preciocategoria',
                )),
                ('evento', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='entradas',
                    to='events.evento',
                )),
            ],
            options={'verbose_name': 'Entrada', 'verbose_name_plural': 'Entradas', 'ordering': ['-fecha_compra']},
        ),
    ]
