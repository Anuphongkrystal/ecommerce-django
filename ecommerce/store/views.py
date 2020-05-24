from django.shortcuts import render,get_object_or_404,redirect
from store.models import Category,Product,Cart,CartItem
from store.forms import SignUpForm
from django.contrib.auth.models import Group,User
#form
from django.contrib.auth.forms import AuthenticationForm
#เช็คความถูกต้องของข้อมูล
from django.contrib.auth import login, authenticate,logout
from django.core.paginator import Paginator,EmptyPage,InvalidPage # import paginator,หน้าว่าง,systex ผิดๆ

def index(request,category_slug=None):
    products = None
    category_page = None
    if category_slug != None : #เซต ฟิวเตอร์
        category_page = get_object_or_404(Category,slug=category_slug) #ทำการค้นหาข้อมูล ที่อยู่ในmodel category
        products = Product.objects.all().filter(category=category_page,available=True)
    else :
        products = Product.objects.all().filter(available=True)

    paginator = Paginator(products,2) # แสดง 4 รายการต่อ 1 หน้า

    try:
        page = int(request.GET.get('page','1')) #convert string to int
    except:
        page = 1

    try:
        productperPage = paginator.page(page)
    except (EmptyPage,InvalidPage) :
        productperPage = paginator.page(paginator.num_pages)

    return render(request,'index.html',{'products':productperPage,'category':category_page})

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
        #ในกรณีที่สร้างตะกร้าสินค้ามาแล้ว
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        #ถ้าตะกร้าสินค้ายังไม่ได้สร้าง ก็สร้างขึ้น
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        #ซื้อสินค้าซ้ำกัน
        cart_item = CartItem.objects.get(product=product,cart=cart)

        #check ถ้าสินค้าที่ ซื้อน้อยกว่าในสต็อค
        if cart_item.quantity < cart_item.product.stock:
             #ให้เพิ่มทีล่ะหนึ่งตัว
            cart_item.quantity += 1
            #อัพเดตค่า
            cart_item.save()
    except CartItem.DoesNotExist: #check ว่าตัว object CartItem ยังไม่เคยถูกสร้างขึ้นมาเลย
        #ซื้อครั้งแรก
        #และมีการบันทึกลงฐานข้อมูล
        cart_item = CartItem.objects.create(
            product = product,
            cart = cart,
            quantity = 1,
        )
        cart_item.save()
    return redirect('/')

def cartdetail(request):
    total = 0
    counter = 0
    cart_items = None
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) #ดึงตะกร้า
        cart_items = CartItem.objects.filter(cart=cart,active=True) #ดึงข้อมูลสินค้าในตะกร้า
        for item in cart_items:
            total += (item.product.price*item.quantity) #ราคาสินค้า * จำนวน
            counter += item.quantity
    except Exception as e:
        pass
    return render(request,'cartdetail.html',
    dict(cart_items=cart_items,total=total,counter=counter))

def removeCart(request,product_id):
    #ทำงานกับตะกร้าสินค้า A
    cart = Cart.objects.get(cart_id=_cart_id(request))

    #ทำงานกับสินค้าที่จะลบ 1
    product = get_object_or_404(Product,id=product_id)
    cartItem = CartItem.objects.get(product=product,cart=cart)

    #ลบรายการสินค้า 1 ออกจากตะกร้า A โดยลบจาก รายการสินค้าในตะกร้า(CartItem)
    cartItem.delete()
    return redirect('cartdetail')

def signUpView(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        #เช็คความถูกต้องของ แบบฟอร์ม
        if form.is_valid():
            #บันทึกข้อมูล user
            form.save()
            #บันทึกกลุ่มข้อมูล ของ user
            #ดึง username จาก form เอามาใช้
            #เช็คความถูกต้อง
            username = form.cleaned_data.get('username')
            #ดึงข้อมูล user จากฐานข้อมูล
            signUpUser = User.objects.get(username=username)
            #จัดกลุ่ม user
            customer_group = Group.objects.get(name="Customer")

            customer_group.user_set.add(signUpUser)
    else:
        form = SignUpForm()

    return render(request,'signup.html',{'form':form})

def signInView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        #เช็คความถูกต้องของแบบฟอร์ม
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            if user is not None :
                login(request,user)
                return redirect('home')
            else:
                return redirect('signUp')
    else:
        #สร้าง obj form login
        form = AuthenticationForm()
    return render(request,'signin.html',{'form':form})

def signOutView(request):
    logout(request)
    return redirect('signIn')

def search(request):
    products = Product.objects.filter(name__contains=request.GET['title'])
    return render(request,'index.html',{'products':products})
