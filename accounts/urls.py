from django.urls import path, re_path
from accounts import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'

urlpatterns = [
   path ('signup/', views.signup, name='signup'),
   path('login/', LoginView.as_view(template_name='accounts/login_form.html'), name='login'),
   path('profile/', views.profile, name='profile'),
   path('logout/', views.logout, name='logout'),
   path('edit/', views.profile_edit, name='profile_edit'),
   path ('password_change/', views.password_change, name='password_change'),
   re_path(r'^(?P<username>[\w.@+-]+)/follow/$', views.user_follow, name='user_follow'),
   re_path(r'^(?P<username>[\w.@+-]+)/unfollow/$', views.user_unfollow, name='user_unfollow'),

]
