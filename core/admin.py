# Dentro de core/admin.py

from django.contrib import admin
from .models import (
    Genero,
    Empresa,
    TipoFuncao,
    Artista,
    Filme,
    ElencoFilme,
    Serie,
    Temporada,
    Episodio,
    ElencoEpisodio,
)

# --- Classes Inline (usadas acima) ---

class ElencoFilmeInline(admin.TabularInline):
    model = ElencoFilme
    extra = 1

class ElencoEpisodioInline(admin.TabularInline):
    model = ElencoEpisodio
    extra = 1

# --- Personalização do Admin ---

@admin.register(Artista)
class ArtistaAdmin(admin.ModelAdmin):
    # Adiciona uma barra de busca que procura nos campos especificados
    search_fields = ['nome_principal', 'outros_nomes']

@admin.register(Filme)
class FilmeAdmin(admin.ModelAdmin):
    # Permite adicionar/editar o elenco diretamente na página do filme
    inlines = [ElencoFilmeInline]
    # Adiciona a busca por títulos
    search_fields = ['titulo_original', 'outros_titulos']
    # Melhora a visualização da lista
    list_display = ('titulo_original', 'data_estreia', 'duracao', 'visualizacoes')
    list_filter = ('generos', 'data_estreia')

@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin):
    # Adiciona a busca por títulos
    search_fields = ['titulo_original', 'outros_titulos']
    # Melhora a visualização da lista
    list_display = ('titulo_original', 'status', 'visualizacoes')
    list_filter = ('status', 'generos')

@admin.register(Episodio)
class EpisodioAdmin(admin.ModelAdmin):
    # Permite adicionar/editar o elenco diretamente na página do episódio
    inlines = [ElencoEpisodioInline]
    # Adiciona a busca por título do episódio e título da série relacionada
    search_fields = ['titulo', 'temporada__serie__titulo_original']
    list_display = ('titulo', 'temporada', 'data_exibicao')
    list_filter = ('temporada__serie', 'data_exibicao')

# --- Registro dos modelos mais simples (que não precisam de personalização avançada) ---
admin.site.register(Genero)
admin.site.register(Empresa)
admin.site.register(TipoFuncao)
admin.site.register(Temporada)

# Não precisamos mais destes, pois foram registrados com o @admin.register acima
# admin.site.register(Artista, ArtistaAdmin)
# admin.site.register(Filme, FilmeAdmin)
# admin.site.register(Serie, SerieAdmin)
# admin.site.register(Episodio, EpisodioAdmin)