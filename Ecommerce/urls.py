from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('store/', views.StoreView.as_view(), name='store'),
    path('update_item/', views.UpdateItemView.as_view(), name='update_item'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('process_order/', views.ProcessOrderView.as_view(), name='process_order'),
]
