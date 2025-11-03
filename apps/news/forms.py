from django import forms

from .models import News, NewsCategory


class NewsForm(forms.ModelForm):
    """Form for creating and editing news/events"""

    class Meta:
        model = News
        fields = [
            "title",
            "content",
            "excerpt",
            "category",
            "featured_image",
            "image_caption",
            "event_date",
            "event_location",
            "event_end_date",
            "status",
            "publish_date",
            "is_featured",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Digite o título da notícia/evento",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 10,
                    "placeholder": "Conteúdo completo...",
                }
            ),
            "excerpt": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Resumo curto (até 300 caracteres)",
                    "maxlength": 300,
                }
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
            "featured_image": forms.FileInput(
                attrs={"class": "form-control", "accept": "image/*"}
            ),
            "image_caption": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Legenda da imagem (opcional)",
                }
            ),
            "event_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "event_location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Local do evento (opcional)",
                }
            ),
            "event_end_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "publish_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "is_featured": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "title": "Título",
            "content": "Conteúdo",
            "excerpt": "Resumo",
            "category": "Categoria",
            "featured_image": "Imagem Destacada",
            "image_caption": "Legenda da Imagem",
            "event_date": "Data do Evento",
            "event_location": "Local do Evento",
            "event_end_date": "Data Final do Evento",
            "status": "Status",
            "publish_date": "Data de Publicação",
            "is_featured": "Destacar",
        }
        help_texts = {
            "excerpt": "Deixe em branco para gerar automaticamente do conteúdo",
            "event_date": "Obrigatório apenas para eventos",
            "event_location": "Obrigatório apenas para eventos",
            "publish_date": "Data e hora em que a notícia será publicada",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make event fields not required by default
        self.fields["event_date"].required = False
        self.fields["event_location"].required = False
        self.fields["event_end_date"].required = False

        # Add help text for featured checkbox
        self.fields["is_featured"].help_text = (
            "Marque para destacar esta notícia na página inicial"
        )

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        event_date = cleaned_data.get("event_date")
        event_location = cleaned_data.get("event_location")

        # Validate event-specific fields if category is Event
        if category and category.name == NewsCategory.EVENT:
            if not event_date:
                self.add_error(
                    "event_date", "Data do evento é obrigatória para eventos."
                )
            if not event_location:
                self.add_error(
                    "event_location", "Local do evento é obrigatório para eventos."
                )

        # Validate excerpt length
        excerpt = cleaned_data.get("excerpt")
        if excerpt and len(excerpt) > 300:
            self.add_error("excerpt", "O resumo não pode ter mais de 300 caracteres.")

        return cleaned_data
