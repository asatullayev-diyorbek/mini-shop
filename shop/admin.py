from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Comment, Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'slug', 'get_image_fields')
    prepopulated_fields = {'slug': ('name',)}

    def get_image_fields(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" alt="Rasm yo\'q" width="80px" height="80px" style="border-radius: 10px">')


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('user', 'content', 'rating', 'created_at')
    readonly_fields = ('user', 'content', 'rating', 'created_at')


class ProductAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ('name', 'category', 'slug', 'short_description', 'price', 'discount', 'is_discount', 'measurement_unit', 'stock', 'available', 'get_image_fields')
    list_filter = ('category', 'available')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('available', 'price', 'discount', 'is_discount', 'measurement_unit')

    def get_image_fields(self, obj):
        return mark_safe(f'<img src="{obj.get_image()}" alt="Rasm yo\'q" width="80px" height="80px" style="border-radius: 10px">')
    get_image_fields.short_description = 'Image'

    def short_description(self, obj):
        return obj.description[:30] + '...'
    short_description.short_description = 'Tavsif'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
