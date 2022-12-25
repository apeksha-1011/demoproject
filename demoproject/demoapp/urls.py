from django.urls import path, include
from . import views
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('', include(router.urls)),
    path('index/', views.index, name='index'),
    path('display_products/', views.display_products, name="display_products"),
    path('delete_product/<str:id>/', views.delete_product, name="delete_product"),
    path('product_details/<int:id>/', views.product_details, name="product_details"),
    path('update_product_detail/', views.update_product_detail, name="update_product_detail"),
    # path("class_based_update_product/<str:id>/", views.UpdateProductDetail.as_view({'get': 'get_product_detail'}), name="class_update_product_detail"),
    path('login_user/', views.login_user, name="login_user"), 
    path('logout_user/', views.logout_user, name="logout_user"),
    path('api_productdetails/', views.ProductViewset.as_view({'get': 'list', 'post': 'create'})),
    path('retrieve_product/<str:pk>/', views.ProductViewset.as_view({'get': 'retrieve',
                                                                    'patch':'partial_update'})),
    path('display_product_api/', views.display_product_api),
    path('delete_product_api/<str:id>/', views.delete_product_api),
    path('login_by_api/', views.login_by_api),
] 