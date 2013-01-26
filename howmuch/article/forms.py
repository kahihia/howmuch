from django import forms
from django.forms import ModelForm, Textarea, TextInput, Select

from howmuch.article.models import Article, Assignment

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ('owner','date','title_url')

class OfferForm(forms.Form):
    cprice = forms.IntegerField(
        widget = forms.TextInput(attrs = {'class' : 'InputForm'}))
    message = forms.CharField(
        widget = forms.Textarea(attrs = {'class' : 'InputForm TextareaForm'}))
    picture1 = forms.ImageField(
        widget = forms.ClearableFileInput(attrs = {'class' : 'InputFile', 'onChange' : "readURL(this,'image1')"}))
    picture2 = forms.ImageField(required=False,
        widget = forms.ClearableFileInput(attrs = {'class' : 'InputFile', 'onChange' : "readURL(this,'image2')"}))
    picture3 = forms.ImageField(required=False, 
        widget = forms.ClearableFileInput(attrs = {'class' : 'InputFile', 'onChange' : "readURL(this,'image3')"}))
    picture4 = forms.ImageField(required=False, 
        widget = forms.ClearableFileInput(attrs = {'class' : 'InputFile', 'onChange' : "readURL(this,'image4')"}))
    picture5 = forms.ImageField(required=False, 
        widget = forms.ClearableFileInput(attrs = {'class' : 'InputFile', 'onChange' : "readURL(this,'image5')"}))

class AssignmentForm(ModelForm):
    
    class Meta:
        model = Assignment
        exclude = ('owner', 'article', 'date', 'status', )
        widgets = {
            'comment' : Textarea(attrs={'class' : 'InputForm TextareaForm', 'cols' : 60, 'rows' : 10}),
            }

