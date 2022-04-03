from django import forms
from webinar_factory.users.models import User
from webinar_factory.core.models import Tag, Webinar

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

class WebinarForm(forms.ModelForm):
    organizer = forms.ModelChoiceField(
        queryset=User.objects.all(),
        disabled=True, widget=forms.HiddenInput()
    )
    class Meta:
        model = Webinar
        fields = '__all__'
