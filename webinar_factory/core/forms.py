from django import forms
from webinar_factory.core.models import Tag, Webinar

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

class WebinarCreationForm(forms.ModelForm):
    class Meta:
        model = Webinar
        fields = '__all__'
