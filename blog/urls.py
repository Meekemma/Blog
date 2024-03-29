from django.urls import path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap

from django.contrib.auth import views as auth_views

from .import views

sitemaps = {
    'posts': PostSitemap,
}



urlpatterns = [
    path('register/', views.registerPage, name = "register"),
    path('login/', views.loginPage, name= "login"),
    path('logout/', views.logoutUser, name= "logout"),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="blog/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="blog/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="blog/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="blog/password_reset_done.html"), 
        name="password_reset_complete"),
    
    path('', views.PostList, name="index"),
    path('accounts/', views.accountSettings, name="accounts"),
    path('<slug:slug>/', views.PostDetail, name="detail"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name="sitemap"),

   
    


]