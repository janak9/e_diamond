from django.forms import modelformset_factory
from django import forms
from main_admin.models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('src', )

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    src = forms.ImageField()

ImageFormset = modelformset_factory(Image, form=ImageForm, extra=1)
