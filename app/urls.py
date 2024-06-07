
from django.urls import path
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path('contact/',views.contact,name='contact'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('blog/',views.blog,name='blog'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('signup_view/',views.signup_view,name='signup_view'),
    path('login_view/',views.login_view,name='login_view'),
    path('logout_view/',views.logout_view,name='logout_view'),
    path('create_post/',views.create_post,name='create_post'),
    path('view_post/<int:post_id>/',views.view_post,name='view_post'),
    path('edit_post/<int:post_id>/',views.edit_post,name='edit_post'),
    path('delete_post/<int:post_id>/',views.delete_post,name='delete_post')
]
