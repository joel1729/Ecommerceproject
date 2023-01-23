from django.shortcuts import render, redirect, get_object_or_404
from ecommerceapp.models import product
from.models import cart,cartItem

from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart
def add_cart(request,product_id):
    Product=product.objects.get(id=product_id)
    try:
        Cart=cart.objects.get(cart_id=_cart_id(request))
    except cart.DoesNotExist:
        Cart=cart.objects.create(cart_id=_cart_id(request))
        Cart.save()
    try:
        cart_item=cartItem.objects.get(Product=Product,Cart=Cart)
        if cart_item.quantity < cart_item.Product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except cartItem.DoesNotExist:
        cart_item=cartItem.objects.create(Product=Product,quantity=1,Cart=Cart)
        cart_item.save()
    return redirect('cart:cart_detail')
def cart_detail(request,total=0,counter=0,cart_item=None):
    try:
        Cart=cart.objects.get(cart_id=_cart_id(request))
        cart_items=cartItem.objects.filter(Cart=Cart,active=True)
        for cart_item in cart_items:
            total += (cart_item.Product.Price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request,'cart.html',dict(cart_items= cart_items,total=total,counter=counter))
def cart_remove(request,product_id):
    Cart=cart.objects.get(cart_id=_cart_id(request))
    Product=get_object_or_404(product,id=product_id)
    cart_item=cartItem.objects.get(Product=Product,Cart=Cart)
    if cart_item.quantity >1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return   redirect('cart:cart_detail')
def full_remove(request,product_id):
    Cart = cart.objects.get(cart_id=_cart_id(request))
    Product = get_object_or_404(product, id=product_id)
    cart_item = cartItem.objects.get(Product=Product, Cart=Cart)
    cart_item.delete()
    return redirect('cart:cart_detail')








