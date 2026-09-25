from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@mail.ru'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 (999) 999-99-99'}),
            'message': forms.Textarea(attrs={'placeholder': 'Введите ваше сообщение...', 'rows': 4}),
        }
