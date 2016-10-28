from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.conf import settings

from camerastore.views.forms import CheckoutForm
from tradenity.sdk.entities import Address, Customer, Order, ShoppingCart
from tradenity.sdk.exceptions import EntityNotFoundException


@login_required
def index(request):
    customer = Customer.find_by_username(request.user.username)
    orders = Order.find_all_by_customer(customer=customer.id)
    return render(request, "orders/index.html", {"orders": orders})


@login_required
def show(request, order_id):
    try:
        order = Order.find_by_id(order_id)
        return render(request, "orders/show.html", {"order": order})
    except EntityNotFoundException as e:
        return HttpResponseNotFound()


@login_required
def checkout(request):
    cart = ShoppingCart.get()
    customer = Customer.find_by_username(request.user.username)
    form = CheckoutForm(get_form_data(customer))
    return render(request, "orders/checkout.html", {"form": form, "cart": cart, "stripe_pub_key": settings.STRIPE_PUBLIC_KEY})


@login_required
def place_order(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = populate_order(form.cleaned_data, request.user.username)
            paymentSource = request.POST['token']
            transaction = Order.checkout(order, paymentSource)
            return HttpResponseRedirect("/orders/{id}".format(id=transaction.order.id))
        else:
            print form.errors
            cart = ShoppingCart.get()
            return render(request, "orders/checkout.html", {"form": form, "cart": cart})


@login_required
def refund(request, order_id):
    if request.method == 'POST':
        transaction = Order.refund(order_id)
        return HttpResponseRedirect("/orders/{id}".format(id=transaction.order.id))


def create_address():
    return Address(streetLine1="3290 Hermosillo Place", streetLine2="n/a", city="Washington", state="Washington, DC", zipCode="20521-3290", country="USA")


# Django forms does not allow nested forms and object graphs like WTForms do
# so we have to do it by hand
# feel free to optimize this code if you know a better way
# you can check how WTForm significantly reduce this code in the flask sample
def get_form_data(customer):
    billing_address = create_address()
    shipping_address = create_address()
    return dict(
        customer_firstName=customer.firstName,
        customer_lastName=customer.lastName,
        customer_email=customer.email,
        billingAddress_streetLine1=billing_address.streetLine1,
        billingAddress_streetLine2=billing_address.streetLine2,
        billingAddress_city=billing_address.city,
        billingAddress_state=billing_address.state,
        billingAddress_zipCode=billing_address.zipCode,
        billingAddress_country=billing_address.country,
        shippingAddress_streetLine1=shipping_address.streetLine1,
        shippingAddress_streetLine2=shipping_address.streetLine2,
        shippingAddress_city=shipping_address.city,
        shippingAddress_state=shipping_address.state,
        shippingAddress_zipCode=shipping_address.zipCode,
        shippingAddress_country=shipping_address.country,
    )

def populate_order(data, username):
    customer = Customer.find_by_username(username)
    billingAddress = Address(
        streetLine1=data['billingAddress_streetLine1'], 
        streetLine2=data['billingAddress_streetLine2'],
        city=data['billingAddress_city'],
        state=data['billingAddress_state'],
        zipCode=data['billingAddress_zipCode'],
        country =data['billingAddress_country'],
    )
    shippingAddress = Address(
        streetLine1=data['shippingAddress_streetLine1'],
        streetLine2=data['shippingAddress_streetLine2'],
        city=data['shippingAddress_city'],
        state=data['shippingAddress_state'],
        zipCode=data['shippingAddress_zipCode'],
        country =data['shippingAddress_country'],)
    return Order(customer=customer, billingAddress=billingAddress, shippingAddress=shippingAddress)
