from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

RATING_CHOICES = (
    (1, '1 star'),
    (2, '2 stars'),
    (3, '3 stars'),
    (4, '4 stars'),
    (5, '5 stars'),
)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class MenuSearchForm(forms.Form):
    restaurant = forms.ModelChoiceField(queryset=Restaurant.objects.all(), empty_label="Select a restaurant")

    def search(self):
        restaurant = self.cleaned_data['restaurant']
        menus = MenuItem.objects.filter(restaurant=restaurant)
        return menus
    
class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=RATING_CHOICES)
    class Meta:
        model = RestaurantReview
        fields = ['name', 'email', 'rating', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Your review'}),
        }
