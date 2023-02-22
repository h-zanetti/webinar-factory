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

class WebinarFilters(forms.Form):
    name = forms.CharField(label='Nome do Evento', max_length=75, required=False)
    speaker = forms.CharField(label='Palestrante', max_length=75, required=False)
    start_dt = forms.DateTimeField(label='Início', widget=forms.TextInput(attrs={'type': 'datetime-local'}), required=False)
    end_dt = forms.DateTimeField(label='Fim', widget=forms.TextInput(attrs={'type': 'datetime-local'}), required=False)
    price_min = forms.FloatField(label='Preço mínimo', required=False, widget=forms.NumberInput(attrs={'stpe': '0.01'}))
    price_max = forms.FloatField(label='Preço máximo', required=False, widget=forms.NumberInput(attrs={'stpe': '0.01'}))
    tags = forms.ModelMultipleChoiceField(label='Categorias',
                                          queryset=Tag.objects.all(),
                                          widget=forms.CheckboxSelectMultiple,
                                          required=False)

    def clean(self):
        cleaned_data = super().clean()
        start_dt = cleaned_data.get('start_dt')
        end_dt = cleaned_data.get('end_dt')

        if start_dt and end_dt and start_dt >= end_dt:
            raise forms.ValidationError("A data de início deve ser anterior à data de término.")

        return cleaned_data
