# Dentro do arquivo core/models.py (Versão Corrigida)

# Importa as ferramentas necessárias do Django para criar nossos modelos.
from django.db import models

# --- Modelos para listas de opções ---

class Genero(models.Model):
    """ Modelo para armazenar os gêneros de filmes e séries. Ex: Ação, Comédia. """
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Empresa(models.Model):
    """ Modelo para armazenar empresas (produtoras, distribuidoras, emissoras). """
    nome = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nome

class TipoFuncao(models.Model):
    """ Modelo para armazenar os tipos de função na equipe. Ex: Diretor, Roteirista, Dublador. """
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

# --- Modelos Principais ---

class Artista(models.Model):
    """ Modelo para armazenar as informações dos artistas. """
    nome_principal = models.CharField(max_length=200, verbose_name="Nome Principal")
    outros_nomes = models.CharField(max_length=500, blank=True, null=True, verbose_name="Outros Nomes")
    biografia = models.TextField(blank=True, null=True, verbose_name="Biografia")
    # Adicione a linha abaixo
    foto = models.ImageField(upload_to='artistas_fotos/', blank=True, null=True, verbose_name="Foto")
    data_nascimento = models.DateField(blank=True, null=True, verbose_name="Data de Nascimento")
    naturalidade = models.CharField(max_length=150, blank=True, null=True, verbose_name="Naturalidade")
    data_obito = models.DateField(blank=True, null=True, verbose_name="Data do Óbito")

    def __str__(self):
        return self.nome_principal

class Filme(models.Model):
    """ Modelo para armazenar as informações dos filmes. """
    titulo_original = models.CharField(max_length=255, verbose_name="Título Original (Idioma)")
    outros_titulos = models.CharField(max_length=500, blank=True, null=True, verbose_name="Outros Títulos (Idioma)")
    sinopse = models.TextField(blank=True, null=True)
    data_estreia = models.DateField(blank=True, null=True, verbose_name="Estreia")
    observacao_estreia = models.CharField(max_length=255, blank=True, null=True, verbose_name="Observação")
    classificacao_indicativa = models.CharField(max_length=50, blank=True, null=True, verbose_name="Classificação")
    duracao = models.CharField(max_length=10, blank=True, null=True, help_text="Formato: 00h00min", verbose_name="Duração")
    paises_origem = models.CharField(max_length=255, blank=True, null=True, verbose_name="País de Origem")
    idioma_original = models.CharField(max_length=50, blank=True, null=True, verbose_name="Idioma de Origem")
    site_oficial = models.URLField(blank=True, null=True, verbose_name="Site oficial")
    link_trailer = models.URLField(blank=True, null=True, verbose_name="Trailer (Player de Vídeo)")
    poster = models.ImageField(upload_to='posters/filmes/', blank=True, null=True, verbose_name="Pôsteres Principais")
    visualizacoes = models.IntegerField(default=0, verbose_name="Visualizações")
 
    # Relações com outras tabelas
    generos = models.ManyToManyField(Genero, blank=True)
    producao = models.ManyToManyField(Empresa, related_name="filmes_produzidos", blank=True, verbose_name="Produção (Empresas)")
    distribuicao = models.ManyToManyField(Empresa, related_name="filmes_distribuidos", blank=True, verbose_name="Distribuição (Empresa)")
    elenco = models.ManyToManyField(Artista, through='ElencoFilme', blank=True, verbose_name="Elenco e Equipe Técnica")

    def __str__(self):
        return self.titulo_original

class ElencoFilme(models.Model):
    """ Tabela de ligação entre Filme, Artista e a sua função. """
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE, verbose_name="Adicionar Artista")
    funcao = models.ForeignKey(TipoFuncao, on_delete=models.PROTECT, verbose_name="Tipo")
    personagem = models.CharField(max_length=200, blank=True, null=True, verbose_name="Personagem")

    def __str__(self):
        return f"{self.artista.nome_principal} como {self.personagem or self.funcao.nome} em {self.filme.titulo_original}"

class Serie(models.Model):
    """ Modelo para armazenar as informações gerais das séries. """
    STATUS_CHOICES = [
        ('em_exibicao', 'Em Exibição'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
        ('piloto', 'Piloto'),
    ]
    titulo_original = models.CharField(max_length=255, verbose_name="Título Original (Idioma)")
    outros_titulos = models.CharField(max_length=500, blank=True, null=True, verbose_name="Outros títulos (Idioma)")
    sinopse = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='em_exibicao')
    classificacao_indicativa = models.CharField(max_length=50, blank=True, null=True, verbose_name="Classificação")
    paises_origem = models.CharField(max_length=255, blank=True, null=True, verbose_name="País de Origem")
    idioma_original = models.CharField(max_length=50, blank=True, null=True, verbose_name="Idioma de Origem")
    site_oficial = models.URLField(blank=True, null=True, verbose_name="Site oficial")
    link_trailer = models.URLField(blank=True, null=True, verbose_name="Trailer (Player de Vídeo)")
    poster = models.ImageField(upload_to='posters/series/', blank=True, null=True)
    visualizacoes = models.IntegerField(default=0, verbose_name="Visualizações")
    # Relações
    generos = models.ManyToManyField(Genero, blank=True)
    producao = models.ManyToManyField(Empresa, related_name="series_produzidas", blank=True, verbose_name="Produção (Empresas)")
    emissora = models.ManyToManyField(Empresa, related_name="series_exibidas", blank=True)

    def __str__(self):
        return self.titulo_original

class Temporada(models.Model):
    """ Modelo para armazenar as temporadas de uma série. """
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, related_name="temporadas")
    numero = models.PositiveIntegerField(verbose_name="Número")
    titulo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Título (Idioma)")
    outros_titulos = models.CharField(max_length=500, blank=True, null=True, verbose_name="Outros títulos (Idioma)")
    poster = models.ImageField(upload_to='posters/temporadas/', blank=True, null=True, verbose_name="Imagem (Pôster)")

    class Meta:
        unique_together = ('serie', 'numero')
        ordering = ['serie', 'numero']

    def __str__(self):
        return f"{self.serie.titulo_original} - Temporada {self.numero}"

class Episodio(models.Model):
    """ Modelo para armazenar os episódios de uma temporada. """
    temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, related_name="episodios")
    numero = models.PositiveIntegerField(verbose_name="Número")
    titulo = models.CharField(max_length=255, verbose_name="Título (Idioma)")
    outros_titulos = models.CharField(max_length=500, blank=True, null=True, verbose_name="Outros títulos (Idioma)")
    sinopse = models.TextField(blank=True, null=True)
    imagem = models.ImageField(upload_to='imagens/episodios/', blank=True, null=True)
    data_exibicao = models.DateField(blank=True, null=True, verbose_name="Data de Exibição")
    duracao = models.PositiveIntegerField(blank=True, null=True, help_text="Duração em minutos", verbose_name="Duração (min)")
    elenco = models.ManyToManyField(Artista, through='ElencoEpisodio', blank=True)
    
    class Meta:
        unique_together = ('temporada', 'numero')
        ordering = ['temporada', 'numero']

    def __str__(self):
        return f"T{self.temporada.numero:02d}E{self.numero:02d} - {self.titulo}"

class ElencoEpisodio(models.Model):
    """ Tabela de ligação entre Episódio, Artista e a sua função. """
    episodio = models.ForeignKey(Episodio, on_delete=models.CASCADE)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE, verbose_name="Adicionar Artista")
    funcao = models.ForeignKey(TipoFuncao, on_delete=models.PROTECT, verbose_name="Tipo")
    personagem = models.CharField(max_length=200, blank=True, null=True, verbose_name="Personagem")

    def __str__(self):
        return f"{self.artista.nome_principal} como {self.personagem or self.funcao.nome} em {self.episodio}"