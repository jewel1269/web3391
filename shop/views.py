from django.shortcuts import get_object_or_404, redirect, render

from .cart import Cart
from .models import Category, Product


def product_list(request, category_slug=None):
    """
    Homepage product list with optional category filter.
    """
    cart = Cart(request)
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    selected_category = None

    if category_slug is not None:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    return render(
        request,
        "shop/list.html",
        {
            "categories": categories,
            "products": products,
            "selected_category": selected_category,
            "cart": cart,
        },
    )


def category_list(request):
    """
    Dedicated page listing all categories.
    """
    cart = Cart(request)
    categories = Category.objects.all()
    return render(
        request,
        "shop/categories.html",
        {
            "categories": categories,
            "cart": cart,
        },
    )


def product_detail(request, id, slug):
    """
    Detail page for a single product.
    """
    product = get_object_or_404(
        Product,
        id=id,
        slug=slug,
        available=True,
    )
    cart = Cart(request)
    return render(
        request,
        "shop/detail.html",
        {
            "product": product,
            "cart": cart,
        },
    )


def add_to_cart(request, product_id):
    """
    Add a product to the session-based cart or update its quantity.
    Expects a POST request with an optional 'quantity' field.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, available=True)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    cart.add(product=product, quantity=quantity)
    return redirect("shop:cart_detail")


def cart_detail(request):
    """
    Display the contents of the cart.
    """
    cart = Cart(request)
    return render(
        request,
        "shop/cart.html",
        {
            "cart": cart,
        },
    )


def checkout(request):
    """
    Simple checkout flow: on POST, clear cart and redirect to success page.
    """
    cart = Cart(request)
    if request.method == "POST":
        if len(cart):
            cart.clear()
        return redirect("shop:order_success")

    return render(
        request,
        "shop/checkout.html",
        {
            "cart": cart,
        },
    )


def order_success(request):
    """
    Order success page shown after checkout.
    """
    cart = Cart(request)
    return render(
        request,
        "shop/success.html",
        {
            "cart": cart,
        },
    )
