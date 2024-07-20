from django.contrib import admin
from .models import ProductCategory
# Register your models here.
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
     list_display=['id','name','description','datetime','status']