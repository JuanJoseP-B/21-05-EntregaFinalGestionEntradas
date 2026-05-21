import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Evento, PrecioCategoria, Ubicacion
from .forms import EventoForm, UbicacionForm


def event_list(request):
    eventos = Evento.objects.filter(
        estado=Evento.Estado.PUBLICADO
    ).select_related('ubicacion', 'organizador').order_by('fecha_inicio')
    return render(request, 'events/list.html', {'eventos': eventos})


@login_required
def event_manage(request):
    if not request.user.is_organizador:
        messages.error(request, 'Solo los organizadores pueden gestionar eventos.')
        return redirect('events:list')
    eventos = Evento.objects.filter(organizador=request.user).select_related('ubicacion')
    return render(request, 'events/manage.html', {'eventos': eventos})


@login_required
def event_create(request):
    if not request.user.is_organizador:
        messages.error(request, 'Solo los organizadores pueden crear eventos.')
        return redirect('events:list')

    form = EventoForm(request.POST or None, request.FILES or None)
    ubicacion_form = UbicacionForm(request.POST or None, prefix='ub')

    if request.method == 'POST' and form.is_valid():
        evento = form.save(commit=False)
        evento.organizador = request.user

        if not evento.ubicacion and ubicacion_form.is_valid():
            data = ubicacion_form.cleaned_data
            if any(data.values()):
                ubicacion = ubicacion_form.save()
                evento.ubicacion = ubicacion

        evento.save()
        messages.success(request, 'Evento creado exitosamente.')
        return redirect('events:manage')

    return render(request, 'events/create.html', {'form': form, 'ubicacion_form': ubicacion_form})


def event_detail(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    categorias = evento.categorias.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f'/users/login/?next=/events/{pk}/')
        if not request.user.is_asistente:
            messages.error(request, 'Solo los asistentes pueden comprar entradas.')
        else:
            categoria_id = request.POST.get('categoria_id')
            try:
                from tickets.models import Entrada
                categoria = PrecioCategoria.objects.get(pk=categoria_id, evento=evento)
                if categoria.disponibles <= 0:
                    messages.error(request, 'No hay entradas disponibles en esta categoría.')
                else:
                    Entrada.objects.create(
                        codigo_unico=str(uuid.uuid4()),
                        pagado=True,
                        asistente=request.user,
                        categoria=categoria,
                        evento=evento,
                    )
                    messages.success(request, '¡Entrada comprada exitosamente!')
                    return redirect('tickets:my_tickets')
            except PrecioCategoria.DoesNotExist:
                messages.error(request, 'Categoría no encontrada.')

    return render(request, 'events/detail.html', {'evento': evento, 'categorias': categorias})


@login_required
def event_edit(request, pk):
    evento = get_object_or_404(Evento, pk=pk, organizador=request.user)
    form = EventoForm(request.POST or None, request.FILES or None, instance=evento)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Evento actualizado exitosamente.')
        return redirect('events:manage')

    return render(request, 'events/edit.html', {'form': form, 'evento': evento})
