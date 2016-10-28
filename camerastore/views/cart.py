import json

from django.http import HttpResponse
from django.shortcuts import render

from camerastore.views.forms import CartItemForm
from tradenity.sdk.entities import ShoppingCart, Category


def show(request):
    cart = ShoppingCart.get()
    return render(request, "shop/cart.html", {"cart": cart, "categories": Category.find_all()})


def add_to_cart(request):
    if request.method == 'POST':
        form = CartItemForm(request.POST)
        if form.is_valid():
            cart = ShoppingCart.add(product=form.cleaned_data['product'], quantity=form.cleaned_data['quantity'])
            data = {"status": "success", "total": cart.total, "count": cart.count}
            return HttpResponse(json.dumps(data), content_type="application/json")
    return HttpResponse(json.dumps({"status": "error"}), content_type="application/json")


def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart = ShoppingCart.remove(item_id)
        data = {"status": "success", "total": cart.total, "count": cart.count }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return HttpResponse(json.dumps({"status": "error"}), content_type="application/json")
