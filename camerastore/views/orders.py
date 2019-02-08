from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.conf import settings

from camerastore.views.forms import CheckoutForm, ShippingMethodForm
from tradenity import Address, Customer, Order, ShoppingCart, ShippingMethod, PaymentToken, CreditCardPayment, Country, State
from tradenity.exceptions import EntityNotFoundException


@login_required
def index(request):
    customer = Customer.find_one_by(username=request.user.username)
    orders = Order.find_all_by(customer=customer.id)
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
    customer = Customer.find_one_by(username=request.user.username)
    request.session['customer_id'] = customer.id
    form = CheckoutForm(get_form_data(customer))
    usa = Country.find_one_by(iso2="US")
    countries = Country.find_all(size=250, sort="name")
    states = State.find_all_by(country=usa.id, size=60, sort="name")
    form.fields['billingAddress_country'].choices = [(s.id, s.name) for s in countries]
    form.fields['shippingAddress_country'].choices = [(s.id, s.name) for s in countries]
    form.fields['billingAddress_state'].choices = [(s.id, s.name) for s in states]
    form.fields['shippingAddress_state'].choices = [(s.id, s.name) for s in states]
    return render(request, "orders/checkout.html", {"form": form, "cart": cart, "stripe_pub_key": settings.STRIPE_PUBLIC_KEY})


@login_required
def create_order(request):
    form = CheckoutForm(request.POST)
    usa = Country.find_one_by(iso2="US")
    countries = Country.find_all(size=250, sort="name")
    states = State.find_all_by(country=usa.id, size=60, sort="name")
    form.fields['billingAddress_country'].choices = [(s.id, s.name) for s in countries]
    form.fields['shippingAddress_country'].choices = [(s.id, s.name) for s in countries]
    form.fields['billingAddress_state'].choices = [(s.id, s.name) for s in states]
    form.fields['shippingAddress_state'].choices = [(s.id, s.name) for s in states]
    # get_form_data(form)
    if form.is_valid():
        order = populate_order(form.data, request.user.username)
        order.create()
        request.session["order_id"] = order.id
        shipping_methods = ShippingMethod.find_all_for_order(order.id)
        shipping_form = ShippingMethodForm()
        shipping_form.fields['shipping_method'].choices = [(sm.id, sm.name) for sm in shipping_methods]
        return render(request, "orders/shipping_form.html", {"shipping_form": shipping_form})
    else:
        print form.errors


@login_required
def add_shipping(request):
    order = Order.find_by_id(request.session["order_id"])
    order.shipping_method = ShippingMethod(id=request.POST["shipping_method"])
    order.update()
    return render(request, "orders/payment_form.html", {})


@login_required
def place_order(request):
    order = Order.find_by_id(request.session["order_id"])
    payment_source = PaymentToken(token=request.POST['token'], customer=Customer(id=request.session["customer_id"]), status="new").create()
    CreditCardPayment(order=order, payment_source=payment_source).create()
    return HttpResponseRedirect("/orders/{id}".format(id=order.id))


@login_required
def refund(request, order_id):
    if request.method == 'POST':
        transaction = Order.refund(order_id)
        return HttpResponseRedirect("/orders/{id}".format(id=transaction.order.id))


def create_address(country):
    return Address(street_line1="3290 Hermosillo Place", street_line2="n/a", city="Washington", state=State(), zip_code="20521-3290", country=country)


# Django forms does not allow nested forms and object graphs like WTForms do
# so we have to do it by hand
# feel free to optimize this code if you know a better way
# you can check how WTForm significantly reduce this code in the flask sample
def get_form_data(customer):
    usa = Country.find_one_by(iso2="US")
    billing_address = create_address(usa)
    shipping_address = create_address(usa)
    return dict(
        customer_firstName=customer.first_name,
        customer_lastName=customer.last_name,
        customer_email=customer.email,
        billingAddress_streetLine1=billing_address.street_line1,
        billingAddress_streetLine2=billing_address.street_line2,
        billingAddress_city=billing_address.city,
        billingAddress_state=billing_address.state,
        billingAddress_zipCode=billing_address.zip_code,
        billingAddress_country=billing_address.country,
        shippingAddress_streetLine1=shipping_address.street_line1,
        shippingAddress_streetLine2=shipping_address.street_line2,
        shippingAddress_city=shipping_address.city,
        shippingAddress_state=shipping_address.state,
        shippingAddress_zipCode=shipping_address.zip_code,
        shippingAddress_country=shipping_address.country,
    )


def populate_order(data, username):
    customer = Customer.find_one_by(username=username)
    billing_address = Address(
        street_line1=data['billingAddress_streetLine1'],
        street_line2=data['billingAddress_streetLine2'],
        city=data['billingAddress_city'],
        state=State(id=data['billingAddress_state']),
        zip_code=data['billingAddress_zipCode'],
        country=Country(id=data['billingAddress_country'])
    )
    shipping_address = Address(
        street_line1=data['shippingAddress_streetLine1'],
        street_line2=data['shippingAddress_streetLine2'],
        city=data['shippingAddress_city'],
        state=State(id=data['shippingAddress_state']),
        zip_code=data['shippingAddress_zipCode'],
        country=Country(id=data['shippingAddress_country'])
    )
    return Order(customer=customer, billing_address=billing_address, shipping_address=shipping_address)
