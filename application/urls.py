from django.urls import path
from . import views

urlpatterns = [
    # None of these pages require access to the database
    path('', views.map, name='home'),
    path('map/', views.map, name='map'),
    path('whitelabel_map/', views.whitelabel_map, name='whitelabel_map'),
    path('about/', views.about, name='about'),
    path('about/goals/', views.goals, name='goals'),
    path('docs/', views.userDocs, name='userDocs'),
    path('docs/developer/', views.devDocs, name='devDocs'),
    path('filter/', views.wiki, name='wiki'),
    path('contribute/', views.contribute, name='contribute'),

    # Individual spaces
    path('space/<int:id>/', views.space_profile, name='space_profile'),
    path('space/<int:pk>/edit/', views.edit_space, name='edit_space'),
    path('space/add/', views.add_space, name='create_space'),

    path('space/filter/', views.list_spaces, name='list_spaces'),

    # REST API
    path('api/space/<int:id>/', views.get_space, name='get_space'),
    path('api/space/filter/', views.filter_spaces, name='filter_spaces'),

    # Bulk actions
    path('api/getAllSpaces/', views.all_innovation_spaces, name='all_innovation_spaces'),
]
