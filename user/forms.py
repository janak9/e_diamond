from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model
from user.models import User as user_model
User = get_user_model()


class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control radius-both'
            visible.field.widget.attrs['placeholder'] = visible.field.label

    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'gender', 'profile_pic', )

    def clean(self):
        # data from the form is fetched using super function
        super(ProfileForm, self).clean()

        phone = self.cleaned_data.get('phone')
        if (len(phone) != 10 and len(phone) != 0):
            self._errors['phone'] = self.error_class(['phone must be of 10 digit'])

    # def __init__(self, *args, **kwargs):
    #     super(ProfileForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         if visible.field.label != "Gender":
    #             visible.field.widget.attrs['class'] = 'form-control radius-both'
    #         visible.field.widget.attrs['placeholder'] = visible.field.label

    # first_name = forms.CharField(max_length=30, label="First Name")
    # last_name = forms.CharField(max_length=30, label='Last Name')
    # email = forms.EmailField(widget = forms.TextInput(attrs={'readonly':'readonly'}), label="Email")
    # phno = forms.CharField(max_length=15, required=False, label="Contact No")
    # dob = forms.DateField(widget = forms.DateInput(attrs={'type':'date'}), required=False, label="Date Of Birth")
    # gender = forms.ChoiceField(choices=user_model.GENDER_TYPE, widget=forms.RadioSelect(), label="Gender")
    # address = forms.CharField(widget = forms.Textarea(attrs={'rows':4}), required=False, label="Address")
    # profile_pic = forms.ImageField(required=False, label="Profile Pic")
