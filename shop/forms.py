from django import forms
from django.core.exceptions import ValidationError


class CommentForm(forms.Form):
    rating = forms.IntegerField(
        required=True,
        label="Your Rating",
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'rating',
            'min': '1',
            'max': '5',
            'type': 'hidden',
            'value': 1
        })
    )

    content = forms.CharField(
        required=True,
        label="Your Review",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'content',
            'rows': 5,
            'cols': 30,
            'name': 'content',
            'placeholder': 'Typing here...'
        })
    )

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not (1 <= rating <= 5):
            raise ValidationError("Mahsulotni 1 dan 5gacha baholang")
        return rating
