
from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path(
        "product/<int:product_id>/",
        views.product_detail,
        name="product_detail",
    ),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("cart/", views.cart_view, name="cart"),
    path(
    "add-to-cart/<int:product_id>/",
    views.add_to_cart,
    name="add_to_cart",
),
    
path(
    "update-cart/<int:product_id>/",
    views.update_cart,
    name="update_cart",
),

    
path("checkout/", views.checkout_view, name="checkout"),

]

