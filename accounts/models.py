from django.db import models
from contatos.models import Contato
from django import forms


class FormContato(forms.ModelForm):
    class Meta:
        # Cria um formulario
        model = Contato
        # Server para excluir campos do form
        exclude = ()
