from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
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
    path('space/<int:space>/remove/<int:user>', views.DeleteOwner, name='remove_owner'),
    #suggestions
    path('suggestion/<int:space_id>/', views.Suggestions, name='space_suggestion'),
    path('suggestions/', views.AllSuggestion, name='all_suggestion'),
    path('suggestion/<int:suggestion_id>', views.Discart_suggestion, name='discart_suggestion'),
    path('space/<int:pk>/edit/<int:suggestion_id>', views.Acept_suggestion, name='edit_space_suggest'),
    # CSV Interactive Importer
    path('csv/upload/', views.upload_file, name='upload_file'),
    path('analyze/provisional_spaces/', views.analyze_spaces, name='analyze_spaces'),
    path('provisional_space/', views.provisional_space, name='provisional_spaces'),
    path('space_csv/', views.space_csv, name='space_csv'),

    path('space/filter/', views.list_spaces, name='list_spaces'),
    path('space/<int:id>/history/', views.show_data_credit, name='show_data_credit'),

    # REST API
    path('api/space/filter/', views.filter_spaces, name='filter_spaces'),
    #Users
    path(r'admin/', admin.site.urls),
    
    path('signup', views.signup, name='signup'),
    path(r'login/', auth_views.login, name='login'),
    path(r'logout/', auth_views.logout,{'next_page': '/'}, name='logout'),
    path(r'reset_password',views.password_reset,name='password_reset'),
    path('reset_done',auth_views.password_reset_done,name='password_reset_done'),
    url(r'password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.password_reset_confirm,name='password_reset_confirm'),
    #activation email
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

]
