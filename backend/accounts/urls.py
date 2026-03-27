from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

# WHY use SimpleJWT's built-in views for login and token refresh?
# They're battle-tested, handle edge cases correctly, and return the standard
# { access, refresh } JSON format. No reason to rewrite them.
urlpatterns = [
    path('register/', views.register, name='auth-register'),
    path('login/', TokenObtainPairView.as_view(), name='auth-login'),
    path('logout/', views.logout, name='auth-logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='auth-token-refresh'),
    path('me/', views.me, name='auth-me'),
]
