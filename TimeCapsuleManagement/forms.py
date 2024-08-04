from django import forms
from .models import Capsule, Comment


class CapsuleForm(forms.ModelForm):
    VISIBILITY_CHOICES = [
        (False, 'Private'),
        (True, 'Public'),
    ]
    is_public = forms.ChoiceField(
        choices=VISIBILITY_CHOICES,
        widget=forms.Select(
            attrs={'class': 'form-input'}
        ),
        initial=False
    )

    STATUS = [
        (True, 'Published'),
        (False, 'Unpublished')
    ]
    is_published = forms.ChoiceField(
        choices=STATUS,
        widget=forms.Select(
            attrs={'class': 'form-input'}
        ),
        initial=False
    )

    class Meta:
        model = Capsule
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 6}),
            'unsealing_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-input'}
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        label_suffix = ''
        widgets = {
            'content': forms.Textarea(attrs={'rows':0})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['placeholder'] = 'Add comments'