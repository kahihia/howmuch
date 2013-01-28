from django import forms
from django.forms import ModelForm, Textarea, TextInput, Select

from howmuch.article.models import Article, Assignment

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ('owner','date','title_url')
        widgets = {
        'price' : TextInput(attrs = {'class' : 'span7'}),
        'title' : TextInput(attrs = {'class' : 'span7'}),
        'description' : Textarea(attrs = {'class' : 'span7'}),
        'quantity' : TextInput(attrs = {'class' : 'span7'}),
        'category' : Select(attrs = {'class' : 'span7'}),
        'state' : Select(attrs = {'class' : 'span7'}),
        'addressDelivery' : Select (attrs={'class' : 'span7'}),
        }

class OfferForm(forms.Form):
    quantity = forms.IntegerField(
        widget = forms.TextInput(attrs = {'class' : ''}))
    cprice = forms.IntegerField(
        widget = forms.TextInput(attrs = {'class' : ''}))
    message = forms.CharField(
        widget = forms.Textarea(attrs = {'class' : ''}))
    picture1 = forms.ImageField(
        widget = forms.ClearableFileInput(attrs = {'class' : ''}))
    picture2 = forms.ImageField(required=False,
        widget = forms.ClearableFileInput(attrs = {'class' : ''}))
    picture3 = forms.ImageField(required=False, 
        widget = forms.ClearableFileInput(attrs = {'class' : ''}))
    picture4 = forms.ImageField(required=False, 
        widget = forms.ClearableFileInput(attrs = {'class' : ''}))
    picture5 = forms.ImageField(required=False, 
        widget = forms.ClearableFileInput(attrs = {'class' : ''}))

class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        exclude = ('owner', 'article', 'date', 'status', )


