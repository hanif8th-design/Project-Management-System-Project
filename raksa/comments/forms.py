from django import forms
from comments.models import Comment

class CommentForm(forms.ModelForm):

    comment = forms.CharField(widget=forms.Textarea(attrs={'rows':3,'placeholder':'Enter your comment here'}),
    label= False,
    required=True

    )
 
    class Meta:
        model = Comment
        fields = [
            'comment'
        ]

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if len(comment)<10:
            raise forms.ValidationError("Comment must be atleast 10 characters long")
        return comment