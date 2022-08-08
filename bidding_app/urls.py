from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signup),
    path('', views.login_user),
    path('logout/', views.logout_user, name='logout'),
    path('home/', views.home, name='home'),
    path('add/', views.create_view, name='add'),
    path('prod-detail/(?P<key>[\w-]+)$', views.prod_detail, name='prod_detail'),
    path('delete-prod/(?P<key>[\w-]+)$', views.delete_bid, name='delete_bid'),
    path('create_bid/', views.create_bid, name='create_bid'),
    path('bid_filter/', views.bid_filter, name='bid_filter'),
]