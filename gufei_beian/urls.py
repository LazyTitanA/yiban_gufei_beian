from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'applications', views.ApplicationViewSet, basename='application')

urlpatterns = [
    # 注册 & 登录
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('me/', views.me, name='me'),
    # 统计
    path('stats/', views.stats, name='stats'),
    # 申请 CRUD
    path('', include(router.urls)),
]