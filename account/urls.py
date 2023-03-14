from django.urls import path
from . import views
from . import views
from rest_framework_nested import routers
from rest_framework_nested.routers import DefaultRouter

router = DefaultRouter()
router.register('profile', views.ProfileViewSet, basename='profiles')

profile_router = routers.NestedDefaultRouter(router, 'profile', lookup='profile')
profile_router.register('sites', views.SiteViewSet, basename='profile-sites')

urlpatterns = [
    path('', views.exam, name='exam'),
    # path('profile/', views.ProfileViewSet.as_view(), name='profile'),
    
] + router.urls + profile_router.urls
