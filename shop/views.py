from decimal import Decimal

from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .cart import Cart
from .models import Category, Order, OrderItem, Product


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
    related_products = (
        Product.objects.filter(category=product.category, available=True)
        .exclude(id=product.id)[:4]
    )
    return render(
        request,
        "shop/detail.html",
        {
            "product": product,
            "cart": cart,
            "related_products": related_products,
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
    cart = Cart(request)

    if request.method == "POST" and len(cart):
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=request.POST.get("first_name", "").strip(),
            last_name=request.POST.get("last_name", "").strip(),
            email=request.POST.get("email", "").strip(),
            phone=request.POST.get("phone", "").strip(),
            address=request.POST.get("address", "").strip(),
            city=request.POST.get("city", "").strip(),
            postal_code=request.POST.get("postal_code", "").strip(),
            payment_method=request.POST.get("payment", "card"),
            total_paid=cart.get_total_price(),
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                product_name=item["product"].name,
                price=Decimal(item["price"]),
                quantity=item["quantity"],
            )
        cart.clear()
        request.session["last_order_id"] = order.id
        return redirect("shop:order_success")

    return render(request, "shop/checkout.html", {"cart": cart})


def order_success(request):
    cart = Cart(request)
    order = None
    order_id = request.session.get("last_order_id")
    if order_id:
        order = Order.objects.filter(id=order_id).prefetch_related("items").first()
    return render(
        request,
        "shop/success.html",
        {
            "cart": cart,
            "order": order,
        },
    )


def about(request):
    cart = Cart(request)
    return render(request, "shop/about.html", {"cart": cart})


def new_arrivals(request):
    cart = Cart(request)
    products = Product.objects.filter(available=True).order_by("-created")[:12]
    categories = Category.objects.all()
    return render(
        request,
        "shop/new_arrivals.html",
        {
            "cart": cart,
            "products": products,
            "categories": categories,
        },
    )


def search(request):
    cart = Cart(request)
    categories = Category.objects.all()
    query = request.GET.get("q", "").strip()
    products = Product.objects.none()

    if query:
        products = (
            Product.objects.filter(available=True)
            .filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(category__name__icontains=query)
            )
            .distinct()
        )

    return render(
        request,
        "shop/search.html",
        {
            "cart": cart,
            "categories": categories,
            "query": query,
            "products": products,
            "result_count": products.count() if query else 0,
        },
    )
