from django import forms
# django provides built-in model that is User,contains-username,first_name,last_name,email,password etc.
from django.contrib.auth.models import User

# django provides built-in forms that is UserCreationForm form, contains- username ,password1 and password2
# it provides password matching and password validation
from django.contrib.auth.forms import UserCreationForm,SetPasswordForm,PasswordResetForm

# django provides built-in forms that is AuthenticationForm form, contains- username ,password
from django.contrib.auth.forms import AuthenticationForm

# creation of Registration Form inheriting UserCreationForm form and User model
class RegistrationForm(UserCreationForm):
     username=forms.CharField(label="username",widget=forms.TextInput(attrs={'class':'form-control'}))
     email=forms.EmailField(label="email",widget=forms.EmailInput(attrs={'class':'form-control'}))
     password1=forms.CharField(label='password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
     password2=forms.CharField(label='confirm password(again)',widget=forms.PasswordInput(attrs={'class':'form-control'}))
     class Meta:
       #    user model is taken to create user in the model by this form
          model=User
       #    username','email will dispaly first
          fields=['username','email']

     def clean_email(self):
                 email = self.cleaned_data['email']
                 if User.objects.filter(email=email).exists():
                        raise forms.ValidationError("This email is already exist.")
                 return email


# class for login Form
class LoginForm(AuthenticationForm):
       username=forms.CharField(label="username",widget=forms.TextInput(attrs={'class':'form-control'})) 
       password=forms.CharField(label="password",widget=forms.PasswordInput(attrs={'class':'form-control'}))


# explanation of PasswordResetForm, SetPasswordForm
# from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
# PasswordResetForm ->contains only email field to send the link to reset password
# SetPasswordForm -> it contains only password and password(again) filds

# form to reset password -gives email to reset
class CustomPasswordResetForm(PasswordResetForm):
      email=forms.EmailField(label="email",widget=forms.EmailInput(attrs={'class':'form-control'}))

# form to set new password
class CustomSetPasswordForm(SetPasswordForm):
       new_password1=forms.CharField(label="New password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
       new_password2=forms.CharField(label="New password (again)",widget=forms.PasswordInput(attrs={'class':'form-control'}))