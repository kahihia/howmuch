from django import forms
from django.forms import ModelForm, Textarea, TextInput, Select

from howmuch.article.models import Article, Assignment

QUANTITY_CHOICES = (
    (1,'UNO'),
    (2,'ENTRE 2 y 5'),
    (5,'ENTRE 5 y 10'),
    (10,'MAS DE 10'),
    )

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ('owner','tags','date','pictures','title_url', 'comments', 'followers', 'is_active')
        widgets = {
        'price' : TextInput(attrs = {'class' : 'text width-100'}),
        'title' : TextInput(attrs = {'class' : 'text width-100'}),
        'description' : Textarea(attrs = {'class' : 'width-100', 'style':'height:10em'}),
        'quantity' : Select(attrs = {'class' : 'width-100'}),
        'category' : Select(attrs = {'class' : 'width-100'}),
        'state' : Select(attrs = {'class' : 'width-100'}),
        }

class OfferForm(forms.Form):
    quantity = forms.ChoiceField(
        widget = forms.Select(attrs = {'class' : 'span12'}),
        choices = QUANTITY_CHOICES)
    cprice = forms.IntegerField(
        widget = forms.TextInput(attrs = {'class' : 'span12'}))
    message = forms.CharField(
        widget = forms.Textarea(attrs = {'class' : 'span12'}))
    picture1 = forms.ImageField(
        widget = forms.ClearableFileInput(attrs = {'class' : 'input-file', 
            'onChange' : "readURL(this,'image1')"}))
    picture2 = forms.ImageField(required=False,
        widget = forms.ClearableFileInput(attrs = {'class' : 'input-file', 
            'onChange' : "readURL(this,'image2')"}))
    picture3 = forms.ImageField(required=False, 
        widget = forms.ClearableFileInput(attrs = {'class' : 'input-file', 
            'onChange' : "readURL(this,'image3')"}))
    picture4 = forms.ImageField(required=False, 
        widget = forms.ClearableFileInput(attrs = {'class' : 'input-file', 
            'onChange' : "readURL(this,'image4')"}))
    picture5 = forms.ImageField(required=False, 
        widget = forms.ClearableFileInput(attrs = {'class' : 'input-file', 
            'onChange' : "readURL(this,'image5')"}))

class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        exclude = ('owner', 'article', 'date', 'status', )


