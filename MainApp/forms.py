from django.forms import PasswordInput, CharField, ModelForm, Textarea, TextInput, Select, CheckboxInput
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from MainApp.models import Comment, Snippet


class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        # Описываем поля, которые будем заполнять в форме
        fields = ['name', 'lang', 'code', 'is_public']
        # exclude = ['creation_date']
        labels = {"name": "", "lang": "", "code": "", "is_public": "Публичный"}
        widgets = {
            "name": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Название сниппета",
                "style": "max-width: 300px"
            }),
            "lang": Select(attrs={  
                "class": "form-control",
                "style": "max-width: 300px"
            }),
            "code": Textarea(attrs={
                "placeholder": "Код сниппета",
                "rows": 5,
                "class": "form-control",
                "style": "width: 50% !important; resize: vertical !important;"
            }),
            "is_public": CheckboxInput(attrs={
                "class": "form-check-input ms-3"
            }),
        }

    def clean_name(self):
        """Метод для проверки длины имени сниппета (поле <name>)"""
        snippet_name = self.cleaned_data.get("name")
        if snippet_name is not None and len(snippet_name) > 3:
            return snippet_name
        raise ValidationError("Snippet's name too short!")
    
class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

    password1 = CharField(label="password", widget=PasswordInput)
    password2 = CharField(label="password confirm", widget=PasswordInput)

    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")
        if pass1 and pass2 and pass1 == pass2:
            return pass2
        raise ValidationError("Пароли не совпадают или пустые")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CommentForm(ModelForm):
   class Meta:
       model = Comment
       fields = ["text"]
       labels = {"text": ""}
       widgets = {
           "text": Textarea(attrs={
               "class": "form-control",
               "rows": 5,
               "placeholder": "Комментарий для сниппета",
               "style": "max-width: 300px",
           })
       }
