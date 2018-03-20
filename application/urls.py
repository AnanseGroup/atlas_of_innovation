from django.urls import path
from . import views

urlpatterns = [
    # None of these pages require access to the database
    path('', views.map, name='home'),
    path('map/', views.map, name='map'),
    path('about/', views.about, name='about'),
    path('about/goals/', views.goals, name='goals'),
    path('docs/', views.userDocs, name='userDocs'),
    path('docs/developer/', views.devDocs, name='devDocs'),
    path('wiki/', views.wiki, name='wiki'),
    path('contribute/', views.contribute, name='contribute'),

    # Individual spaces
    path('space_page/<int:id>/', views.space_page, name='space_page'),
    path('edit_space/<int:id>/', views.edit_space, name='edit_space'),

    # API-based CRUD
    path('api/get_space/<int:id>/', views.get_space, name='get_space'),
    path('api/edit_space/<int:id>/', views.edit_space, name='edit_space'),
    path('api/add_space/<int:id>/', views.add_space, name='add_space'),
    path('api/delete_space/<int:id>/', views.delete_space, name='delete_space'),

    # Bulk actions
    path('api/getAllSpaces/', views.all_innovation_spaces, name='all_innovation_spaces'),
    ]
