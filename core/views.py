# Dentro de core/views.py
# Dentro de core/views.py

from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from .models import Filme, Serie, Artista, ElencoFilme, ElencoEpisodio, Episodio
from django.contrib.auth.decorators import login_required

def home_view(request):
    # --- LÓGICA DOS ADICIONADOS RECENTEMENTE (AGORA COMPLETA) ---
    filmes_recentes = Filme.objects.all().order_by('-id')[:5]
    series_recentes = Serie.objects.all().order_by('-id')[:5]

    # --- LÓGICA DOS ANIVERSARIANTES ---
    hoje = date.today()
    aniversariantes_do_dia = Artista.objects.filter(
        data_nascimento__month=hoje.month,
        data_nascimento__day=hoje.day
    )

    # --- LÓGICA DOS MAIS ACESSADOS ---
    filmes_mais_acessados = Filme.objects.order_by('-visualizacoes')[:5]
    series_mais_acessadas = Serie.objects.order_by('-visualizacoes')[:5]
    contagem_filmes = Filme.objects.count()
    contagem_series = Serie.objects.count()

    # --- CONTEXTO COMPLETO ---
    context = {
        'filmes': filmes_recentes, # Agora 'filmes' recebe a lista correta
        'series': series_recentes, # Agora 'series' recebe a lista correta
        'aniversariantes': aniversariantes_do_dia,
        'filmes_populares': filmes_mais_acessados,
        'series_populares': series_mais_acessadas,
        'contagem_filmes': contagem_filmes,
        'contagem_series': contagem_series,
    }
    
    return render(request, 'core/home.html', context)

# ... (o resto das suas views, como filme_detalhe_view, etc. continua aqui) ...

# Em core/views.py, na função filme_detalhe_view
def filme_detalhe_view(request, filme_id):
    filme = get_object_or_404(Filme, pk=filme_id)

    # --- LÓGICA PARA INCREMENTAR O CONTADOR ---
    filme.visualizacoes += 1 # Adiciona 1 ao valor atual
    filme.save() # Salva o objeto com o novo valor no banco de dados
    # --- FIM DA LÓGICA ---

    context = { 'filme': filme }
    return render(request, 'core/filme_detalhe.html', context)


# Em core/views.py, na função serie_detalhe_view
def serie_detalhe_view(request, serie_id):
    serie = get_object_or_404(Serie, pk=serie_id)

    # --- LÓGICA PARA INCREMENTAR O CONTADOR ---
    serie.visualizacoes += 1 # Adiciona 1 ao valor atual
    serie.save() # Salva o objeto com o novo valor no banco de dados
    # --- FIM DA LÓGICA ---

    context = { 'serie': serie }
    return render(request, 'core/serie_detalhe.html', context)



# Em core/views.py, na função artista_detalhe_view

def artista_detalhe_view(request, artista_id):
    artista = get_object_or_404(Artista, pk=artista_id)
    participacoes_filmes = ElencoFilme.objects.filter(artista=artista)
    series_ids = ElencoEpisodio.objects.filter(
        artista=artista
    ).values_list('episodio__temporada__serie__id', flat=True).distinct()
    series_participadas = Serie.objects.filter(pk__in=series_ids)

    filmografia_combinada = []

    for participacao in participacoes_filmes:
        if participacao.filme.data_estreia:
            filmografia_combinada.append({
                'tipo': 'filme',
                'objeto': participacao.filme,
                'data': participacao.filme.data_estreia
            })

    for serie in series_participadas:
        primeiro_episodio = Episodio.objects.filter(temporada__serie=serie).order_by('data_exibicao').first()

        # Buscamos a lista de participações e a contagem
        participacoes_em_episodios = ElencoEpisodio.objects.filter(
            artista=artista, 
            episodio__temporada__serie=serie
        ).select_related('episodio') # Usamos select_related para otimizar a consulta

        contagem_episodios = participacoes_em_episodios.count()

        if primeiro_episodio and primeiro_episodio.data_exibicao:
            filmografia_combinada.append({
                'tipo': 'serie',
                'objeto': serie,
                'data': primeiro_episodio.data_exibicao,
                'contagem_episodios': contagem_episodios,
                'participacoes': participacoes_em_episodios, # <-- ADICIONAMOS A LISTA AQUI
            })

    filmografia_ordenada = sorted(
        filmografia_combinada, 
        key=lambda item: item['data'], 
        reverse=True
    )

    context = {
        'artista': artista,
        'filmografia': filmografia_ordenada,
    }
    return render(request, 'core/artista_detalhe.html', context)

def episodio_detalhe_view(request, episodio_id):
    # Busca o episódio pelo ID ou mostra uma página de "Não Encontrado"
    episodio = get_object_or_404(Episodio, pk=episodio_id)

    context = {
        'episodio': episodio
    }
    return render(request, 'core/episodio_detalhe.html', context)