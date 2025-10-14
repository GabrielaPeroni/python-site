from django import forms
from django.forms import inlineformset_factory

from .models import Category, Place, PlaceImage


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = [
            "name",
            "description",
            "address",
            "contact_phone",
            "contact_email",
            "contact_website",
            "categories",
            "latitude",
            "longitude",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent",
                    "placeholder": "Nome do lugar",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent",
                    "placeholder": "Descreva o lugar em detalhes...",
                    "rows": 6,
                }
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent",
                    "placeholder": "Endereço completo",
                    "rows": 3,
                }
            ),
            "contact_phone": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent",
                    "placeholder": "(21) 99999-9999",
                }
            ),
            "contact_email": forms.EmailInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent",
                    "placeholder": "contato@exemplo.com",
                }
            ),
            "contact_website": forms.URLInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent",
                    "placeholder": "https://exemplo.com",
                }
            ),
            "categories": forms.CheckboxSelectMultiple(
                attrs={"class": "form-checkbox"}
            ),
            "latitude": forms.NumberInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent",
                    "placeholder": "-22.9068",
                    "step": "any",
                }
            ),
            "longitude": forms.NumberInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent",
                    "placeholder": "-43.1729",
                    "step": "any",
                }
            ),
        }
        help_texts = {
            "categories": "Selecione uma ou mais categorias que descrevem seu lugar",
            "latitude": "Opcional - coordenada de latitude para localização no mapa",
            "longitude": "Opcional - coordenada de longitude para localização no mapa",
            "contact_phone": "Opcional - telefone de contato",
            "contact_email": "Opcional - email de contato",
            "contact_website": "Opcional - website ou página do lugar",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active categories
        self.fields["categories"].queryset = Category.objects.filter(
            is_active=True
        ).order_by("display_order")

        # Make some fields required
        self.fields["name"].required = True
        self.fields["description"].required = True
        self.fields["address"].required = True
        self.fields["categories"].required = True

    def clean(self):
        cleaned_data = super().clean()
        latitude = cleaned_data.get("latitude")
        longitude = cleaned_data.get("longitude")

        # If one coordinate is provided, both should be provided
        if (latitude is not None and longitude is None) or (
            latitude is None and longitude is not None
        ):
            raise forms.ValidationError(
                "Se você fornecer coordenadas, deve fornecer tanto latitude quanto longitude."
            )

        return cleaned_data


class PlaceImageForm(forms.ModelForm):
    class Meta:
        model = PlaceImage
        fields = ["image", "caption", "is_primary", "display_order"]
        widgets = {
            "image": forms.FileInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent",
                    "accept": "image/*",
                }
            ),
            "caption": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent",
                    "placeholder": "Descrição da imagem (opcional)",
                }
            ),
            "is_primary": forms.CheckboxInput(
                attrs={"class": "form-checkbox h-4 w-4 text-gray-900"}
            ),
            "display_order": forms.NumberInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent",
                    "min": "0",
                    "value": "0",
                }
            ),
        }
        help_texts = {
            "caption": "Opcional - descrição ou legenda da imagem",
            "is_primary": "Marque se esta é a imagem principal do lugar",
            "display_order": "Ordem de exibição (números menores aparecem primeiro)",
        }


# Create a formset for handling multiple images
PlaceImageFormSet = inlineformset_factory(
    Place,
    PlaceImage,
    form=PlaceImageForm,
    fields=["image", "caption", "is_primary", "display_order"],
    extra=3,  # Show 3 empty forms by default
    can_delete=True,
    max_num=10,  # Maximum 10 images per place
    validate_max=True,
)
