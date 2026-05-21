from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('checkin/', views.checkin, name='checkin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/api/ventas/<int:evento_id>/', views.api_ventas, name='api_ventas'),
    path('dashboard/api/asistencia/<int:evento_id>/', views.api_asistencia, name='api_asistencia'),
    path('dashboard/exportar/<int:evento_id>/', views.export_excel, name='export_excel'),
]
