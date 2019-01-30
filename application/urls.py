from django.urls import path
from . import views

from django.contrib import admin

urlpatterns = [
    # None of these pages require access to the database
    path('', views.map, name='home'),
    path('map/', views.map, name='map'),
    path('whitelabel_map/', views.whitelabel_map, name='whitelabel_map'),
    path('about/', views.about, name='about'),
    path('about/goals/', views.goals, name='goals'),
    path('about/contributors/', views.contributors, name='contributors'),
    path('docs/', views.devDocs, name='userDocs'),
    path('docs/developer/', views.devDocs, name='devDocs'),
    path('filter/', views.wiki, name='wiki'),
    path('contribute/', views.contribute, name='contribute'),

    # Individual spaces
    path('space/<int:id>/', views.space_profile, name='space_profile'),
    path('space/<int:pk>/edit/', views.edit_space, name='edit_space'),
    path('space/add/', views.add_space, name='create_space'),
    
    # CSV Interactive Importer
    path('csv/upload/', views.upload_file, name='upload_file'),
    path('analyze/provisional_spaces/', views.analyze_spaces, name='analyze_spaces'),
    path('provisional_space/', views.provisional_space, name='provisional_spaces'),
    path('space_csv/', views.space_csv, name='space_csv'),

    path('space/filter/', views.list_spaces, name='list_spaces'),
    path('space/<int:id>/history/', views.show_data_credit, name='show_data_credit'),

    # REST API
    path('api/space/filter/', views.filter_spaces, name='filter_spaces'),

    path(r'admin/', admin.site.urls),
]
