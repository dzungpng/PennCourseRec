from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import SubmittedDescription

class DescriptionSubmitForm(forms.ModelForm):

    class Meta:
        model = SubmittedDescription
        fields = ('name', 'description',)

    # Setting the styles of the form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn btn-info'))
        self.fields['name'].widget.attrs.update(style='max-width: 40em')
        self.fields['name'].widget.attrs.update(placeholder='Enter Course Name...')
        self.fields['description'].widget.attrs.update(placeholder='Enter Course Description...')
        self.fields['description'].widget.attrs.update(style='max-width: 40em')
