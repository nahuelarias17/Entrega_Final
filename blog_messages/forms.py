from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ComposeForm(forms.Form):
    recipient = forms.CharField()
    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # se agrega None por defecto si no se provee un valor para 'user'
        super(ComposeForm, self).__init__(*args, **kwargs)
        self.fields['recipient'].widget.attrs.update({'class': 'form-control'})
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})
        self.fields['body'].widget.attrs.update({'class': 'form-control'})
        self.fields['recipient'].widget.attrs.update({'autofocus': 'autofocus'})

    def clean_recipient(self):
        username = self.cleaned_data['recipient']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Invalid recipient')
        return username


class ReplyForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ReplyForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update({'class': 'form-control', 'rows': '5'})


class MessageDeleteForm(forms.Form):
    pass
