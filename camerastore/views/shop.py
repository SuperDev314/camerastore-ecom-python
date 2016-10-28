from django.shortcuts import render

from tradenity.sdk.entities import *


def home(request):
    categories = Category.find_all()
    collections = Collection.find_all()
    cart = ShoppingCart.get()
    return render(request, "shop/index.html", {"categories": categories, "collections": collections, "cart": cart})


def products(request):
    if 'query' in request.GET:
        products = Product.find_all(title=request.GET['query'])
    else:
        products = Product.find_all()
    brands = Brand.find_all()
    categories = Category.find_all()
    featured = Collection.find_by_name("featured")
    cart = ShoppingCart.get()
    return render(request, "shop/products.html", {"brands": brands, "categories": categories, "products": products,
                                             "featured": featured, "cart": cart})


def browse_category(request, category_id):
    brands = Brand.find_all()
    categories = Category.find_all()
    featured = Collection.find_by_name("featured")
    products = Product.find_all_by_category(category_id)
    cart = ShoppingCart.get()
    return render(request, "shop/products.html", {"brands": brands, "categories": categories, "products": products,
                                             "featured": featured, "cart": cart})


def browse_brand(request, brand_id):
    brands = Brand.find_all()
    categories = Category.find_all()
    featured = Collection.find_by_name("featured")
    products = Product.find_all_by_brand(brand_id)
    cart = ShoppingCart.get()
    return render(request, "shop/products.html", {"brands": brands, "categories": categories, "products": products,
                                             "featured": featured, "cart": cart})


def product_details(request, product_id):
    brands = Brand.find_all()
    categories = Category.find_all()
    featured = Collection.find_by_name("featured")
    product = Product.find_by_id(product_id)
    cart = ShoppingCart.get()
    return render(request, "shop/single.html", {"brands": brands, "categories": categories, "product": product,
                                           "featured": featured, "cart": cart})




