from django.urls import path
from . import views
app_name = 'graph_app'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/',views.post_new,name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('graph/', views.graph, name='graph'),
    path('chart/', views.get_svg, name="plot"),
    path('scatter/', views.get_png, name='scatter'),
 
]