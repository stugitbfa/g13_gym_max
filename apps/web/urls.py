from django.urls import path
from . import views


urlpatterns = [
    path('', views.enter_email, name='enter_email'),  # Home page is now email input
    path('verify-otp/', views.verify_otp, name='verify_otp'),  # This should already exist
    path('login/', views.login_view, name='login'),  # Existing login view
]