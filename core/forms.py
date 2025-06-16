# Dentro de core/forms.py (novo arquivo)

from django import forms
from .models import Genero, Artista

class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero  # Diz ao Django para criar um formulário a partir do modelo Genero
        fields = ['nome'] # Especifica quais campos do modelo devem aparecer no formulário
        

class ArtistaForm(forms.ModelForm):
    class Meta:
        model = Artista
        # Incluímos todos os campos que queremos no formulário
        fields = [
            'nome_principal', 
            'outros_nomes', 
            'foto', 
            'biografia', 
            'data_nascimento', 
            'naturalidade', 
            'data_obito'
        ]
        # Este 'widgets' é um extra para melhorar a experiência do usuário
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'data_obito': forms.DateInput(attrs={'type': 'date'}),
        }