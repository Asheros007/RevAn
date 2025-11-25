from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('analyze/', views.analyze, name='analyze'),
    path('history/', views.history, name='history'),
    path('logout/', views.logout, name='logout'),
    path('result/', views.result, name='result'),
    path('save-analysis/', views.save_analysis, name='save_analysis'),
    path('analysis/<int:analysis_id>/', views.analysis_detail, name='analysis_detail'),
    path('delete-analysis/<int:analysis_id>/', views.delete_analysis, name='delete_analysis'),
    
]
