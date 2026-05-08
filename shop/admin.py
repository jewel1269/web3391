from django.contrib import admin

from .models import Category, Order, OrderItem, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "available", "created")
    list_filter = ("available", "created", "updated", "category")
    list_editable = ("price", "stock", "available")
    search_fields = ("name", "category__name")
    prepopulated_fields = {"slug": ("name",)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "product_name", "price", "quantity", "total")

    def total(self, obj):
        return obj.total


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "status",
        "payment_method",
        "total_paid",
        "created",
    )
    list_filter = ("status", "payment_method", "created")
    list_editable = ("status",)
    search_fields = ("first_name", "last_name", "email", "phone")
    readonly_fields = ("created",)
    inlines = [OrderItemInline]
    fieldsets = (
        ("Customer", {
            "fields": ("user", "first_name", "last_name", "email", "phone"),
        }),
        ("Shipping", {
            "fields": ("address", "city", "postal_code"),
        }),
        ("Payment & Status", {
            "fields": ("payment_method", "total_paid", "status", "created"),
        }),
    )
