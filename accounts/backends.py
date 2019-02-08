from django.contrib.auth.models import User
from tradenity import Customer, is_valid_password


class CustomerUserAuthBackend(object):
    def authenticate(self, username=None, password=None):
        customer = Customer.find_one_by(username=username)
        if customer is not None and is_valid_password(customer, password):
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username, password=customer.password)
                user.is_staff = False
                user.is_superuser = False
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

