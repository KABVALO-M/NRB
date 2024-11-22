from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Citizen, DeceasedCitizen

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        # Remove help texts
        for field in self.fields.values():
            field.help_text = ""  # Set help text to empty string
        
        # Add Tailwind CSS classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-opacity-50 focus:ring-indigo-200'
            })
            # Add placeholder for better UX
            field.widget.attrs['placeholder'] = f"Enter {field.label}"

        # Customize password fields
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Enter Password'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password'
        })
        

class CitizenForm(forms.ModelForm):
    class Meta:
        model = Citizen
        fields = ['full_name', 'date_of_birth', 'address', 'gender', 'phone_number']
        widgets = {
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female')]),  # Dropdown for gender
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})  # Date input for date_of_birth
        }

    def __init__(self, *args, **kwargs):
        super(CitizenForm, self).__init__(*args, **kwargs)

        # Remove help texts (if any)
        for field in self.fields.values():
            field.help_text = ""  # Set help text to empty string

        # Add Tailwind CSS classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-opacity-50 focus:ring-indigo-200'
            })
            # Add placeholder for better UX
            field.widget.attrs['placeholder'] = f"Enter {field.label}"

        # Customize individual fields
        self.fields['full_name'].widget.attrs.update({
            'placeholder': 'Enter Full Name'
        })
        self.fields['date_of_birth'].widget.attrs.update({
            'placeholder': 'Select Date of Birth'  # Placeholder text for the date field
        })
        self.fields['address'].widget.attrs.update({
            'placeholder': 'Enter Address'
        })
        self.fields['phone_number'].widget.attrs.update({
            'placeholder': 'Enter Phone Number'
        })
        self.fields['gender'].widget.attrs.update({
            'class': 'block w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-opacity-50 focus:ring-indigo-200'
        })
        
        
class DeceasedCitizenForm(forms.ModelForm):
    national_id = forms.CharField(max_length=8, label='National ID', required=True)
    full_name = forms.CharField(max_length=255, label='Full Name', required=False, disabled=True)
    date_of_birth = forms.DateField(label='Date of Birth', required=False, disabled=True,
                                     widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], label='Gender', required=False, disabled=True)
    date_of_death = forms.DateField(label='Date of Death', required=True,
                                     widget=forms.DateInput(attrs={'type': 'date'}))
    cause_of_death = forms.CharField(widget=forms.Textarea, label='Cause of Death', required=True)

    class Meta:
        model = DeceasedCitizen
        fields = ['national_id', 'full_name', 'date_of_birth', 'gender', 'date_of_death', 'cause_of_death']

    def __init__(self, *args, **kwargs):
        super(DeceasedCitizenForm, self).__init__(*args, **kwargs)

        # Apply Tailwind CSS classes to form fields
        self.fields['national_id'].widget.attrs.update({
            'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
        })
        self.fields['full_name'].widget.attrs.update({
            'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
        })
        self.fields['date_of_birth'].widget.attrs.update({
            'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
        })
        self.fields['gender'].widget.attrs.update({
            'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
        })
        self.fields['date_of_death'].widget.attrs.update({
            'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500'
        })
        self.fields['cause_of_death'].widget.attrs.update({
            'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
            'rows': 3  # Optional: set rows for textarea
        })