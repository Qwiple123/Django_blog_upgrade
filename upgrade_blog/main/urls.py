from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('reg', views.SignUpView.as_view(), name='reg'),
    path('', include('django.contrib.auth.urls'), name='login'),
    path('create', views.create_post, name='create_post'),
    path('<slug:slug>/', views.post_view, name = 'post_view'),
    path('<slug:slug>/edit', views.post_edit, name = 'post_edit'),
    path('<slug:slug>/delete', views.post_delete, name = 'post_delete'),
]
