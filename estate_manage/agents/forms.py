from django import forms
from .models import Agent

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = [
            'bio',
            'alternate_phone_number',
            'country',
            'state',
            'address',
            'employment_status',
            'linkedin_url',
            'twitter_url',
            'profile_picture',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your bio', 'rows': 3}),
            'alternate_phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter alternate phone number'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your address', 'rows': 3}),
            'employment_status': forms.Select(attrs={'class': 'form-control'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter LinkedIn URL'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter Twitter URL'}),
        }

    def __init__(self, *args, **kwargs):
        super(AgentForm, self).__init__(*args, **kwargs)

        # Add additional styling or attributes if needed
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
