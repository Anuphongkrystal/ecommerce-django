from store.models import Category,Cart,CartItem
from store.views import _cart_id

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)

def counter(request):
    item_count = 0

    if 'admin' in request.path:
        return {}
    else:
        try:
            #query cart
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            #CartItem
            cart_Item = CartItem.objects.all().filter(cart=cart[:1])

            for item in cart_Item:
                item_count += item.quantity
        except Cart.DoesNotExist:
            #ถ้ายังไม่มีสินค้าในตะกร้าเลย
            item_count = 0
    return dict(item_count=item_count)
