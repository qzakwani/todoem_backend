from django import forms 
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError


from .models import User

# BUILT FOR ADMIN
class AdminSiteUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class AdminSiteUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Password")
    class Meta:
        model = User
        fields = '__all__'



# forgot password
class ForgotPasswordForm(forms.Form):
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        
    error_messages = {
        "password_mismatch": "The two password fields didn’t match.",
    }
    
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text="6 characters or longer",
        validators=[MinLengthValidator(6, message="password length MUST be 6 characters or more")]
    )
    
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
        return password2

    

    def save(self, commit=True):
        if self.user is not None:
            password = self.cleaned_data["new_password1"]
            self.user.set_password(password)
            if commit:
                self.user.save()
            return self.user
        return None