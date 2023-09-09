from django.urls import path
from orders import views


urlpatterns = [
    # path('place-order/',views.place_order,name='place-order'),
    path('checkout/',views.checkout,name='checkout'),
    path('create-order/',views.create_order,name='create-order'),
    path('confirmation/',views.confirmation,name='confirmation'),
    path('confirmation-cod/<int:id>',views.confirmation_cod,name='confirmation-cod'),
    path('my-order/',views.my_order,name='my-order'),
    path('order-details/<int:id>',views.order_details,name='order-details'),
]
