from . import views as v
from django.urls import path


urlpatterns = [
    path('login/', v.Login.as_view(), name='login'),
    path('login/refresh/', v.RefreshLogin.as_view(), name='login_refresh'),
    
    path('sign-up/', v.sign_up),
    
    path('change-password/', v.change_password),
    path('change-username/', v.change_username),
    
    path('verify-email/<str:token>/', v.verify_email)
    
]
