from django.urls import path
from adminpanel import views


urlpatterns = [
    path('admin-login/',views.admin_login,name='admin-login'),
    path('admin-dashboard/',views.admin_dashboard,name='admin-dashboard'),
    path('admin-logout/',views.admin_logout,name='admin-logout'),

    path('users/',views.userlist,name='users'),
    path('blockuser/<int:id>/',views.blockuser,name='blockuser'),
    path('unblockuser/<int:id>/',views.unblockuser,name='unblockuser'),

    path('categories/',views.categories,name='categories'),
    path('add-category/',views.add_category,name='add-category'),
    path('delete-category/<int:id>/',views.delete_category,name='delete-category'),
    path('edit-category/<int:id>/',views.edit_category,name='edit-category'),

    path('product/',views.product,name='product'),
    path('add-product/',views.add_product,name='add-product'),
    path('edit-product/<int:id>/',views.edit_product,name='edit-product'),
    path('delete-product/<int:id>/',views.delete_product,name='delete-product'), 

    path('variants/<int:id>/',views.variant,name='variants'),
    path('add-variant/<int:id>/',views.add_variant,name='add-variant'),
    path('edit-variant/<int:variant_id>',views.edit_variant,name='edit-variant'),
    path('delete-variant/<int:id>/',views.delete_variant,name='delete-variant'),

    path('product-images/<int:id>/',views.product_image,name='product-images'),
    path('add-images/<int:id>/',views.add_image,name='add-images'),
    path('edit-images/<int:id>/',views.edit_image,name='edit-images'),
    path('delete-images/<int:id>/',views.delete_image,name='delete-images'),
 
]
