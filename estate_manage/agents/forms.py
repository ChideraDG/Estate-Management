from django import forms
from .models import Agent

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = [
            'name',
            'email',
            'phone_number',
            'profile_picture',
            'bio',
            'alternate_phone_number',
            'country',
            'state',
            'address',
            'date_of_hire',
            'employment_status',
            'number_of_apartments_managed',
            'rating',
            'linkedin_url',
            'twitter_url',
        ]

    def __init__(self, *args, **kwargs):
        super(AgentForm, self).__init__(*args, **kwargs)

        # Add additional styling or attributes if needed
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
