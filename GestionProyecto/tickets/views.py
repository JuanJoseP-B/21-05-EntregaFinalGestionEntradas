from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from openpyxl import Workbook

from .models import Entrada
from events.models import Evento, PrecioCategoria


@login_required
def my_tickets(request):
    entradas = Entrada.objects.filter(
        asistente=request.user
    ).select_related('evento', 'categoria').order_by('-fecha_compra')
    return render(request, 'tickets/my_tickets.html', {'entradas': entradas})


@login_required
def checkin(request):
    if not request.user.is_operador:
        messages.error(request, 'Solo los operadores pueden hacer check-in.')
        return redirect('home')

    entrada = None
    error = None

    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip()
        try:
            entrada = Entrada.objects.select_related('asistente', 'evento', 'categoria').get(codigo_unico=codigo)
            if entrada.usado:
                error = 'Esta entrada ya fue utilizada.'
            elif not entrada.pagado:
                error = 'Esta entrada no ha sido pagada.'
            else:
                from django.utils import timezone
                entrada.usado = True
                entrada.fecha_uso = timezone.now()
                entrada.save()
                messages.success(request, f'✓ Check-in exitoso — {entrada.asistente.get_full_name() or entrada.asistente.username}')
                entrada = None
        except Entrada.DoesNotExist:
            error = 'Código no encontrado.'

    return render(request, 'tickets/checkin.html', {'entrada': entrada, 'error': error})


@login_required
def dashboard(request):
    if not request.user.is_organizador:
        messages.error(request, 'Solo los organizadores tienen acceso al dashboard.')
        return redirect('events:list')

    eventos = list(Evento.objects.filter(organizador=request.user).order_by('-created_at'))

    total_vendidas = Entrada.objects.filter(
        evento__organizador=request.user, pagado=True
    ).count()

    total_ingresos = Entrada.objects.filter(
        evento__organizador=request.user, pagado=True
    ).aggregate(total=Sum('categoria__precio'))['total'] or 0

    for evento in eventos:
        evento.entradas_vendidas = Entrada.objects.filter(evento=evento, pagado=True).count()
        result = Entrada.objects.filter(evento=evento, pagado=True).aggregate(total=Sum('categoria__precio'))
        evento.ingresos_totales = result['total'] or 0

    return render(request, 'dashboard/index.html', {
        'eventos': eventos,
        'total_vendidas': total_vendidas,
        'total_ingresos': total_ingresos,
    })


@login_required
def api_ventas(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id, organizador=request.user)
    categorias = PrecioCategoria.objects.filter(evento=evento)
    labels = [c.nombre for c in categorias]
    vendidas = [Entrada.objects.filter(categoria=c, pagado=True).count() for c in categorias]
    disponibles = [c.cantidad_disponible for c in categorias]
    return JsonResponse({'labels': labels, 'vendidas': vendidas, 'disponibles': disponibles})


@login_required
def api_asistencia(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id, organizador=request.user)
    data = (
        Entrada.objects.filter(evento=evento, pagado=True)
        .annotate(dia=TruncDate('fecha_compra'))
        .values('dia')
        .annotate(count=Count('id'))
        .order_by('dia')
    )
    labels = [str(d['dia']) for d in data]
    counts = [d['count'] for d in data]
    return JsonResponse({'labels': labels, 'counts': counts})


@login_required
def export_excel(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id, organizador=request.user)
    entradas = Entrada.objects.filter(evento=evento).select_related('asistente', 'categoria')

    wb = Workbook()
    ws = wb.active
    ws.title = 'Entradas'
    ws.append(['Código', 'Asistente', 'Email', 'Categoría', 'Precio', 'Pagado', 'Usado', 'Fecha Compra'])

    for e in entradas:
        ws.append([
            str(e.codigo_unico),
            e.asistente.get_full_name() or e.asistente.username,
            e.asistente.email,
            e.categoria.nombre,
            float(e.categoria.precio),
            'Sí' if e.pagado else 'No',
            'Sí' if e.usado else 'No',
            e.fecha_compra.strftime('%Y-%m-%d %H:%M') if e.fecha_compra else '',
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="entradas_{evento_id}.xlsx"'
    wb.save(response)
    return response
