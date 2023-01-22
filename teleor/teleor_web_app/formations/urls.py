from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('details_post/', views.details_post, name='details_post'),
    path('details_get/<int:code>/', views.details_get, name='details_get'),
    path('calculate_cpf_post/', views.calculate_cpf_post, name='calculate_cpf_post'),
    path('get_copyrights/', views.get_copyrights, name='get_copyrights'),
    #path('db/', views.database_fill, name='database_fill'),
]
