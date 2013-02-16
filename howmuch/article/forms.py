from django import forms
from django.forms import ModelForm, Textarea, TextInput, Select

from howmuch.article.models import Article, Assignment

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ('owner','date','title_url', 'comments', 'followers', 'is_active')
        widgets = {
        'price' : TextInput(attrs = {'class' : 'width-350'}),
        'title' : TextInput(attrs = {'class' : 'width-350'}),
        'description' : Textarea(attrs = {'class' : 'width-350'}),
        'quantity' : TextInput(attrs = {'class' : 'width-350'}),
        'category' : Select(attrs = {'class' : 'width-350'}),
        'state' : Select(attrs = {'class' : 'width-350'}),
        'addressDelivery' : Select (attrs={'class' : 'width-350'}),
        }

class OfferForm(forms.Form):
    quantity = forms.IntegerField(
        widget = forms.TextInput(attrs = {'class' : 'span12'}))
    cprice = forms.IntegerField(
        widget = forms.TextInput(attrs = {'class' : 'span12'}))
    message = forms.CharField(
        widget = forms.Textarea(attrs = {'class' : 'span12'}))
    picture1 = forms.ImageField(
        widget = forms.ClearableFileInput(attrs = {'class' : 'input-file', 'onChange' : "readURL(this,'image1')"}))
    picture2 = forms.ImageField(required=False,
        widget = forms.ClearableFileInput(attrs = {'class' : 'input-file', 'onChange' : "readURL(this,'image2')"}))
    picture3 = forms.ImageField(required=False, 
        widget = forms.ClearableFileInput(attrs = {'class' : 'input-file', 'onChange' : "readURL(this,'image3')"}))
    picture4 = forms.ImageField(required=False, 
        widget = forms.ClearableFileInput(attrs = {'class' : 'input-file', 'onChange' : "readURL(this,'image4')"}))
    picture5 = forms.ImageField(required=False, 
        widget = forms.ClearableFileInput(attrs = {'class' : 'input-file', 'onChange' : "readURL(this,'image5')"}))

class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        exclude = ('owner', 'article', 'date', 'status', )


