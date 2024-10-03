from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    path('product/<slug:slug>/detail/', views.ProductDetailView.as_view(), name='product_detail'),

    # Cart
    path('cart/', views.CartListView.as_view(), name='cart_list'),
    path('cart/<int:pk>/add/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/<int:pk>/remove/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('cart/<int:pk>/delete/', views.CartDeleteView.as_view(), name='cart_delete'),

    path('product/<slug:slug>/comment/', views.CommentView.as_view(), name='comment'),
]