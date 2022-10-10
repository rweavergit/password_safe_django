from django import forms
from .models import User #, UserPw

non_allowed_usernames = ['abc']

class RegisterForm(forms.Form):
      username = forms.CharField()
      email = forms.EmailField()
      password1 = forms.CharField(
            label='Password',
            widget=forms.PasswordInput(
                  attrs={
                        "id": "user-password"
                  }
            )
      )
      password2 = forms.CharField(
            label='Confirm Password',
            widget = forms.PasswordInput(
                  attrs={
                        "id": "user-confirm-password"
                  }
            )
      )

      def clean_password2(self):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')

            if not password2:
                  raise forms.ValidationError("You must confirm your password.")
            if password1 != password2:
                  raise forms.ValidationError("Your passwords do not match")
            return password2

      def clean_username(self):
            username = self.cleaned_data.get('username')
            qs = User.objects.filter(username__iexact=username)
            if username in non_allowed_usernames:
                  raise forms.ValidationError("This is an invalid username, please pick another")

            if qs.exists():
                  raise forms.ValidationError("This is an invalid username, please pick another")

            return username
      
      def clean_email(self):
            email = self.cleaned_data.get('email')
            qs = User.objects.filter(email__iexact=email)
            if qs.exists():
                  raise forms.ValidationError("This email is already in use.")
            return email

class LoginForm(forms.Form):
      username = forms.CharField(widget=forms.TextInput(
            attrs={
                  "class": "form-control"
            }
      ))
      password = forms.CharField(
            widget = forms.CharField(
                  widget = forms.PasswordInput(
                        attrs={
                              "class": "form-control",
                              "id": "user-password"
                        }
                  )
            )
      )

      def clean_username(self):
            username = self.cleaned_data.get("username")
            qs = User.objects.filter(username__iexact=username)
            if not qs.exists():
                  raise forms.ValidationError("This is an invalid user.")
            if qs.count() != 1:
                  raise forms.ValidationError("This is an invalid user.")

            return username