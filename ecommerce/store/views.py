from django.shortcuts import render,get_object_or_404
from store.models import Category,Product,Cart,CartItem

def index(request,category_slug=None):

    products = None
    category_page = None
    if category_slug != None : #เซต ฟิวเตอร์
        category_page = get_object_or_404(Category,slug=category_slug) #ทำการค้นหาข้อมูล ที่อยู่ในmodel category
        products = Product.objects.all().filter(category=category_page,available=True)
    else :
        products = Product.objects.all().filter(available=True)


    return render(request,'index.html',{'products':products,'category':category_page})

def productPage(request,category_slug,product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug,slug=product_slug) #ให้ Column category_slug == category_slug ที่ส่งมา และ ให้ Column slug = product_slug ที่ส่งมา
    except Exception as e :
        raise e
    return render(request,'product.html',{'product':product})

def _cart_id(request):#session cart
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def addCart(request,product_id):
    #ดึงสินค้าที่ซื้อขึ้นมาแสดง
    product = Product.objects.get(id=product_id)
    #สร้างตะกร้าสินค้า
    try:
        #ในกรณีที่สร้าตะกร้าสินค้ามาแล้ว
        cart = Cart.objects.get(cart_id=_cart_id(request)) #เอาcolumn cart_id ไปเช็คกับฟังก์ชั่น def _cart_id():
    except Cart.DoesNotExist:
        #ถ้าตะกร้าสินค้ายังไม่ได้สร้าง ก็สร้างขึ้น
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
