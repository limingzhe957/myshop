from django import forms
from models import User


# 用户校验
class UserForm(forms.Form):
    username = forms.CharField(max_length=12, required=False, min_length=6)
    email = forms.EmailField(label='邮箱')


class UserForm2(forms.Form):
    class Meta:
        model = User
        fields = ['username', 'email']



