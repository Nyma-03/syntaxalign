from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import DevelopmentInquiry
from .models import DevelopmentInquiry, DesignInquiry,Lead

admin.site.register(DevelopmentInquiry)
admin.site.register(DesignInquiry)
from django.contrib import admin
from .models import Product, PurchaseRequest
admin.site.register(Lead)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'demo_link')
    list_filter = ('category',)


@admin.register(PurchaseRequest)
class PurchaseRequestAdmin(admin.ModelAdmin):
    list_display = ('product', 'email', 'whatsapp', 'requested_at')
    list_filter = ('product', 'requested_at')
