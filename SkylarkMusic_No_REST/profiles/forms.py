from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from SkylarkMusic_No_REST.profiles.mixins import CustomFormURLField


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = ''
        self.fields['username'].help_text = ''
        self.fields['password1'].widget.attrs['placeholder'] = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].widget.attrs['placeholder'] = ''
        self.fields['password2'].help_text = ''


class EditProfileForm(forms.ModelForm):
    current_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Current Password"}),
        required=False
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"placeholder": "New Password"}),
        required=False
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm New Password"}),
        required=False
    )

    age = forms.IntegerField(
        label="Age",
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={"placeholder": "Enter your age"}),
    )

    country = forms.CharField(
        label="Country",
        required=False,
        widget=forms.TextInput(),
    )

    city = forms.CharField(
        label="City",
        required=False,
        widget=forms.TextInput(),
    )

    profile_picture = CustomFormURLField(
        label="Profile Picture",
        required=False,
        widget=forms.URLInput(attrs={"placeholder": "Profile Picture URL"})
    )

    bio = forms.CharField(
        label="Biography",
        required=False,
        widget=forms.Textarea(attrs={"placeholder": "Writhe something about yourself"}),
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email",)

        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
        }

        help_texts = {'username': None, }

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password1 != new_password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        current_password = self.cleaned_data.get("current_password")
        new_password1 = self.cleaned_data.get("new_password1")
        if current_password and new_password1:
            if not user.check_password(current_password):
                raise forms.ValidationError("Invalid current password.")
            user.set_password(new_password1)

        if commit:
            user.save()
            skylarkuser = user.skylarkuser
            for field_name, field_value in self.cleaned_data.items():
                if hasattr(user, field_name):
                    setattr(user, field_name, field_value)
                elif hasattr(skylarkuser, field_name):
                    setattr(skylarkuser, field_name, field_value)
            skylarkuser.save()
        return user
