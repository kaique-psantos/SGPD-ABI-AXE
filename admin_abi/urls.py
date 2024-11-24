from django.urls import path
from admin_abi import views
from django.contrib.auth import views as auth_views
from abi.views import dashboard



urlpatterns = [
  path('', dashboard, name='index'),

  # Authentication
  # Kaique: comentei as rotas de registro e resete de  senha até as regras sobre estas telas estrem definidas, para cadastro e reset de senha somente pelo super usuário pode fazer isso

  #path('accounts/register/', views.UserRegistrationView.as_view(), name='register'),
  path('accounts/register/', views.index, name='register'), #TEMPORARIO
  path('accounts/login/', views.UserLoginView.as_view(), name='login'),
  path('accounts/logout/', views.logout_view, name='logout'),

  path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
  path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
      template_name='accounts/auth-password-change-done.html'
  ), name="password_change_done"),
  
  path('accounts/password-reset/', views.index, name='password_reset'), #TEMPORARIO
  
  #path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
  #path('accounts/password-reset-confirm/<uidb64>/<token>/',
  #  views.UserPasswrodResetConfirmView.as_view(), name="password_reset_confirm"
  #),
  #path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
  #  template_name='accounts/auth-password-reset-done.html'
  #), name='password_reset_done'),
  #path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
  #  template_name='accounts/auth-password-reset-complete.html'
  #), name='password_reset_complete'),

  #
  path('profile/', views.profile, name='profile'),
  path('profile_update/', views.profile_update, name='profile_update'),
]
