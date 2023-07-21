from django.contrib import admin
from django.urls import path
from live_video_recorder import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('record-video/', views.record_video, name='record_video'),
    path('record-audio/', views.record_audio, name='record_audio'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', views.dashboard, name='dashboard'),  
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('random_question/', views.random_question, name='random_question'),
    path('submit_response/', views.submit_response, name='submit_response'),
    path('record-list/', views.record_list, name='record_list'),
    path('question/', views.question, name='question'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
