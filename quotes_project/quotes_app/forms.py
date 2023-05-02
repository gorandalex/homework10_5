from django import forms

from .models import Quote, Tag, Author


class AddAuthorForm(forms.ModelForm):
    fullname = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    born_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-date'}))
    born_location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class AddQuoteForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.order_by('fullname').all())
    quote = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter comma-separated tags'}))

    class Meta:
        model = Quote
        fields = ['author', 'quote', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = Author.objects.order_by('fullname')

    def clean_tags(self):
        tag_names = [t.strip() for t in self.cleaned_data['tags'].split(',')]
        tags = []
        for name in tag_names:
            if name:
                tag, _ = Tag.objects.get_or_create(name=name)
                tags.append(tag)
        return tags

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance
