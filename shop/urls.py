from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    path('product/<slug:slug>/detail/', views.ProductDetailView.as_view(), name='product_detail'),

    path('product/<slug:slug>/comment/', views.CommentView.as_view(), name='comment'),
]