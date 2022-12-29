from django import forms 
from .models import Post


class PostForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
	class Meta:
		model = Post 
		fields = ['content',]