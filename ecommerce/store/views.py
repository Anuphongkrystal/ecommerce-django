from django.shortcuts import render,get_object_or_404
from store.models import Category,Product

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
        product = Product.objects.get(category_slug=category_slug,slug=product_slug) #ให้ Column category_slug == category_slug ที่ส่งมา และ ให้ Column slug = product_slug ที่ส่งมา
    except Exception as e :
        raise e
    return render(request,'product.html',{'product':product})
