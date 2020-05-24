from django.contrib import admin
from store.models  import Category,Product,Cart,CartItem

#จัดรูปแบบการแสดงข้อมูล
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','stock','created','updated']
    list_editable = ['price','stock'] #แก้ไขบนหน้าเว็ปได้เลย
    list_per_page = 5 #แสดง 5 สินค้า 5 อย่างต่อหน้า
admin.site.register(Category)
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
