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
    path('wikipage/<str:id>/', views.spacepage, name='spacepage'),
    path('editspace/<str:id>/', views.editspace, name='editspace'),
    path('api/getSpace/<str:id>/', views.getspace, name='getspace'),
    path('api/changeSpace/<str:id>/', views.change_space, name='change_space'),

    # Bulk actions
    path('api/getAllSpaces/', views.all_innovation_spaces, name='all_innovation_spaces'),
    path('uifunc/wikilist/<str:param>/<str:value>/', views.singlefilterlist, name='singlefilterlist'),
    path('searchapi/findSpacesByType/', views.singlefilter, name='singlefilter'),
]
