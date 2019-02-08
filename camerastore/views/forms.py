from django.forms import Form, ChoiceField, CharField, IntegerField, Select


class CartItemForm(Form):
    product = CharField()
    quantity = IntegerField()


class ShippingMethodForm(Form):
    shipping_method = ChoiceField(label='Shipping method')


class CheckoutForm(Form):
    customer_firstName = CharField(label='First Name')
    customer_lastName = CharField(label='Last Name')
    customer_email = CharField(label='Email')
    billingAddress_streetLine1 = CharField(label='StreetLine 1')
    billingAddress_streetLine2 = CharField(label='StreetLine 2')
    billingAddress_city = CharField(label='City')
    billingAddress_state = ChoiceField(label='State')
    billingAddress_zipCode = CharField(label='Zip Code')
    billingAddress_country = ChoiceField(label='Country')
    shippingAddress_streetLine1 = CharField(label='StreetLine 1')
    shippingAddress_streetLine2 = CharField(label='StreetLine 2')
    shippingAddress_city = CharField(label='City')
    shippingAddress_state = ChoiceField(label='State')
    shippingAddress_zipCode = CharField(label='Zip Code')
    shippingAddress_country = ChoiceField(label='Country')


