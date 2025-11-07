from django.forms import ModelForm, ValidationError, Textarea, TextInput, Select, CheckboxInput
from MainApp.models import Snippet


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