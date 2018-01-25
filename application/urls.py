from django.urls import path
from . import views

urlpatterns = [
    # None of these pages require access to the database
    path('', views.home, name='home'),
    path('map/', views.map, name='map'),
    path('about/', views.about, name='about'),
    path('about/goals/', views.goals, name='goals'),
    path('docs/', views.userDocs, name='userDocs'),
    path('docs/developer/', views.devDocs, name='devDocs'),
    path('wiki/', views.wiki, name='wiki'),
    path('contribute/', views.contribute, name='contribute'),

    # Individual spaces
    path('wikipage/<str:pk>', views.spacepage, name='spacepage'),
    path('editspace/<str:pk>', views.editspace, name='editspace'),
    path('api/getSpace/<str:pk>', views.getspace, name='getspace'),
    path('api/changeSpace/<str:pk>', views.change_space, name='change_space'),
]
