from django.contrib import admin
from store.models  import Category,Product,Cart,CartItem,Order,OrderItem

#จัดรูปแบบการแสดงข้อมูล
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','stock','created','updated']
    list_editable = ['price','stock'] #แก้ไขบนหน้าเว็ปได้เลย
    list_per_page = 5 #แสดง 5 สินค้า 5 อย่างต่อหน้า

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','total','token','created','updated']
    list_per_page = 5

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','product','quantity','price','created','updated']
    list_per_page = 5

admin.site.register(Category)
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
