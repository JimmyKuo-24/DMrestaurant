from django import forms
from .models import Profile, Reservation, TimeSlot, Cuisine, Order

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phone', 'is_gourmet', 'is_cook']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['time_slot', 'number_of_people']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['time_slot'].queryset = TimeSlot.objects.filter(available=True)

class OrderForm(forms.ModelForm):
    cuisine = forms.ModelChoiceField(queryset=Cuisine.objects.all(), empty_label="Please select one cuisine")
    class Meta:
        model = Order
        fields = ['cuisine', 'quantity']
