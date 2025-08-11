from django.contrib import admin
from .models import *


admin.site.register(Category)

class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('user','job','status','timestamp')
    list_filter = ('status', 'job')
    search_fields = ('user__first_name', 'user__last_name', 'job__title')
    
admin.site.register(Applicant,ApplicantAdmin)


class JobAdmin(admin.ModelAdmin):
    list_display = ('title','category','job_type','timestamp')

admin.site.register(Job,JobAdmin)

class BookmarkJobAdmin(admin.ModelAdmin):
    list_display = ('job','user','timestamp')
admin.site.register(BookmarkJob,BookmarkJobAdmin)


from django.contrib import admin
from .models import ProductCategory, Brand, Product

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_filter = ['created_at']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'price', 'discounted_price', 'stock_quantity', 'is_available', 'is_featured', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category', 'brand', 'sizes', 'colors', 'is_available', 'is_featured', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_available', 'is_featured', 'stock_quantity']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'category', 'brand')
        }),
        ('Pricing', {
            'fields': ('price', 'discounted_price')
        }),
        ('Product Details', {
            'fields': ('image', 'sizes', 'colors', 'stock_quantity')
        }),
        ('Availability', {
            'fields': ('is_available', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )