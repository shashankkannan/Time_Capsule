from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(
        label='Search',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search...',
            'class': 'search-input',
            'aria-label': 'Search'
        })
    )
    unsealed_date = forms.DateField(
        label='Unsealed Date',
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'date-input',
            'placeholder': 'YYYY-MM-DD',
        })
    )
    sealed_date = forms.DateField(
        label='Sealed Date',
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'date-input',
            'placeholder': 'YYYY-MM-DD',
        })
    )
    is_public = forms.BooleanField(
        label='Public',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox-input',
        })
    )
