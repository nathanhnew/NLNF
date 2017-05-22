from django import forms
from blog.models import Post,Comment
#from ckeditor.widgets import CKEditorWidget
#from ckeditor_uploader.widgets import CKEditorUploadingWidget

class PostForm(forms.ModelForm):

	class Meta():
		model = Post
		fields = ('author', 'title', 'text')

		widgets = {
			#'media':CKEditorUploadingWidget(),
			'title':forms.TextInput(attrs={'class':'textinputclass'}),
			#'text':CKEditorWidget(),
		}

class CommentForm(forms.ModelForm):

	class Meta():
		model = Comment
		fields = ('author', 'text')

		widgets = {
			'author':forms.TextInput(attrs={'class':'textinputclass'}),
			'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea'}),
		}