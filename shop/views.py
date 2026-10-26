
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .models import Product
from .forms import RegisterForm


def product_list(request):
    products = Product.objects.all()
    return render(
        request,
        "shop/product_list.html",
        {"products": products},
    )


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(
        request,
        "shop/product_detail.html",
        {"product": product},
    )


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("product_list")
    else:
        form = RegisterForm()

    return render(request, "shop/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Login successful!")
            return redirect("product_list")
    else:
        form = AuthenticationForm(request)

    return render(request, "shop/login.html", {"form": form})


def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect("product_list")
  

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from decimal import Decimal

@login_required
def checkout_view(request):
    cart = request.session.get("cart", {})
    cart_items = []

    for product_id, quantity in cart.items():
        product = Product.objects.filter(id=product_id).first()

        if product:
            quantity = int(quantity)

            if quantity > 0 and quantity <= product.stock:
                cart_items.append((product, quantity))

    if not cart_items:
        messages.error(request, "Your cart is empty or unavailable.")
        return redirect("cart")

    if request.method == "POST":
        with transaction.atomic():
            total = Decimal("0.00")

            for product, quantity in cart_items:
                product = Product.objects.select_for_update().get(
                    id=product.id
                )

                if quantity > product.stock:
                    messages.error(
                        request,
                        "Stock changed. Please review your cart."
                    )
                    return redirect("cart")

                total += product.price * quantity

            order = Order.objects.create(
                user=request.user,
                total=total,
            )

            for product, quantity in cart_items:
                product = Product.objects.select_for_update().get(
                    id=product.id
                )

                if quantity > product.stock:
                    messages.error(
                        request,
                        "Stock changed. Please review your cart."
                    )
                    return redirect("cart")

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price,
                )

                product.stock -= quantity
                product.save(update_fields=["stock"])

        request.session["cart"] = {}
        messages.success(request, "Your order was placed successfully!")
        return redirect("product_list")

    return render(request, "shop/checkout.html")

  

def cart_view(request):
    cart = request.session.get("cart", {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.filter(id=product_id).first()

        if product:
            quantity = int(quantity)
            subtotal = product.price * quantity
            total += subtotal

            cart_items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            })

    return render(
        request,
        "shop/cart.html",
        {"cart_items": cart_items, "total": total},
    )
    
def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)

        cart = request.session.get("cart", {})
        product_id_str = str(product.id)

        current_quantity = int(cart.get(product_id_str, 0))

        if current_quantity < product.stock:
            cart[product_id_str] = current_quantity + 1

        request.session["cart"] = cart

    return redirect("cart")

def update_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get("cart", {})
        product_id_str = str(product.id)

        try:
            quantity = int(request.POST.get("quantity", 1))
        except (ValueError, TypeError):
            quantity = 1

        if quantity <= 0:
            cart.pop(product_id_str, None)
        elif quantity <= product.stock:
            cart[product_id_str] = quantity

        request.session["cart"] = cart

    return redirect("cart")

    




