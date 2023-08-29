from django.urls import path
from orders import views


urlpatterns = [
    path('checkout/',views.checkout,name='checkout'),
    path('payment-confirmation/',views.payment_confirmation,name='payment-confirmation'),
    # path('place_order/',views.place_order,name='place_order'),
    path('confirmation/',views.confirmation,name='confirmation'),
]
