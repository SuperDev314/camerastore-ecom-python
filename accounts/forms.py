from django.forms import Form, CharField, TextInput, PasswordInput


class LoginForm(Form):
    username = CharField(widget=TextInput)
    password = CharField(widget=PasswordInput)


class RegistrationForm(Form):
    first_name = CharField(widget=TextInput)
    last_name = CharField(widget=TextInput)
    email = CharField(widget=TextInput)
    username = CharField(widget=TextInput)
    password = CharField(widget=PasswordInput)
    confirm_password = CharField(widget=PasswordInput)
