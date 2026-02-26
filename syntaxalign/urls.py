from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('work/', views.work, name='work'),
    path('pricing/', views.pricing, name='pricing'),
    path('products/', views.products_list, name='products'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('signup/', views.signup, name='signup'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('design/', views.design, name='design'),
path('development/', views.development, name='development'),
path("start-development/", views.start_development, name="start_development"),
path("thank-you/", views.thank_you, name="thank_you"),
path("start-design/", views.start_design, name="start_design"),
  path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
path('process/', views.buy_now, name='buy_now'),
    path('process/request/<int:product_id>/', views.purchase_request, name='purchase_request'),

]
