from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField
)
from django.contrib.auth import password_validation
from django.contrib.sessions.models import Session

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + \
            ('edad', 'cargo', 'is_staff', 'groups')

    username = UsernameField(
        label=("Usuario"), widget=forms.TextInput(attrs={'autofocus': True}))
    password1 = forms.CharField(
        label=("Contraseña"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Confirmacion de contraseña"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )

    def save(self, commit=True):
        #       print(self.cleaned_data["groups"])
        # my_group = Group.objects.get(name='my_group_name')
        # my_group.user_set.add(your_user)
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        for group in self.cleaned_data.get("groups", []):
            group.user_set.add(user)

        return user
        # is_staff=forms.BooleanField(required=True)
    # UserCreationForm.groups.add(group = Group(name="employer"))


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=("Usuario"), max_length=254)
    password = forms.CharField(
        label=("Contraseña"), widget=forms.PasswordInput)

    def confirm_login_allowed(self, user):
        '''
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        '''
        for objs in Session.objects.all():
            # print(objs.session_data)
            uid = objs.get_decoded().get('_auth_user_id')
            print(uid)
            if(uid):
                if(int(uid) == user.id):
                    objs.delete()

        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )
        else:
            print("PENDEJETE")
