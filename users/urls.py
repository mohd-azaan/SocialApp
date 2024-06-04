from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.user_login, name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path('changePassword/', auth_views.PasswordChangeView.as_view(template_name='users/changePassword.html', success_url='/users/changePasswordDone'), name='changePassword'),
    path('changePasswordDone/', auth_views.PasswordChangeDoneView.as_view(template_name="users/changePasswordDone.html"), name="changePasswordDone"),
    
    path('resetPassword/', auth_views.PasswordResetView.as_view(template_name="users/resetPassword.html", success_url='/users/resetPasswordDone'), name="resetPassword"),
    path('resetPasswordDone/', auth_views.PasswordResetDoneView.as_view(template_name="users/resetPasswordDone.html"), name="resetPasswordDone"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/resetPasswordConfirm.html", success_url='/users/resetPasswordComplete'), name="password_reset_confirm"),
    path('resetPasswordComplete/', auth_views.PasswordResetCompleteView.as_view(template_name="users/resetPasswordComplete.html"), name="resetPasswordComplete"),
    path('register/', views.register, name='register'),
    path('editUser/', views.editUser, name='editUser'),
]

