from django import forms
from blog.models import Post,Comment

class PostForm(forms.ModelForm):

	class Meta():
		model = Post
		fields = ('title', 'feature', 'text')
		labels = {
			'title': 'Title',
			'feature': 'Feature Image',
			'text': 'Content',
		}
		widgets = {
			'title':forms.TextInput(attrs={'class':'titleinputclass'}),
			'feature': forms.FileInput(attrs={'class':'featinput'}),
			'text':forms.Textarea(attrs={'class':'contentinput'}),
		}

class CommentForm(forms.ModelForm):

	class Meta():
		model = Comment
		fields = ('author', 'text')

		widgets = {
			'author':forms.TextInput(attrs={'class':'textinputclass'}),
			'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea'}),
		}