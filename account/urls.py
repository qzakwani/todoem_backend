from . import views as v
from django.urls import path


urlpatterns = [
    path('', v.get_user),
    path('update/', v.update_profile),
    
    path('login/', v.Login.as_view(), name='login'),
    path('login/refresh/', v.RefreshLogin.as_view(), name='login_refresh'),
    
    path('sign-up/', v.sign_up),
    
    path('change-password/', v.change_password),
    path('change-username/', v.change_username),
    
    path('verify-email/', v.request_email_verification),
    path('verify-email/resend/', v.resend_email_verification),
    path('verify-email/<str:token>/', v.verify_email),
    # forgot password
    path('frogot-password/', v.forgot_password),
    path('frogot-password/<str:token>/', v.rest_forgot_password),
    
    
    path('deactivate/', v.deactivate_account)
    
]
