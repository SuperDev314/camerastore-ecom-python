from django.conf.urls import url
from camerastore.views import shop
from camerastore.views import cart
from camerastore.views import orders

urlpatterns = [
    url(r'^$', shop.home),
    url(r'^index.html$', shop.home),
    url(r'^products$', shop.products),
    url(r'^products/(?P<product_id>[^/]+)', shop.product_details),
    url(r'^categories/(?P<category_id>[^/]+)', shop.browse_category),
    url(r'^brands/(?P<brand_id>[^/]+)', shop.browse_brand),
    url(r'^cart$', cart.show),
    url(r'^cart/add$', cart.add_to_cart),
    url(r'^cart/remove/(?P<item_id>[^/]+)', cart.remove_from_cart),
    url(r'^orders$', orders.index),
    url(r'^orders/checkout$', orders.checkout),
    url(r'^orders/create$', orders.place_order),
    url(r'^orders/refund/(?P<order_id>[^/]+)', orders.refund),
    url(r'^orders/(?P<order_id>[^/]+)', orders.show),
]
