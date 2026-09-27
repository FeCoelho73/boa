"""Raspador de pesquisa para o projeto Ademicon.

Coleta:
  1. Comentários de vídeos do YouTube sobre consórcio (sem login).
  2. Texto das páginas de produto do site da Ademicon.

Saída: ademicon/pesquisa/raw/*.json e *.txt — depois é só pedir ao Claude para analisar.

Uso (na raiz do repositório):
  pip install yt-dlp youtube-comment-downloader requests beautifulsoup4
  python3 ademicon/ferramentas/raspar.py            # tudo
  python3 ademicon/ferramentas/raspar.py youtube    # só comentários
  python3 ademicon/ferramentas/raspar.py site       # só site Ademicon

Requer acesso de rede a youtube.com e ademicon.com.br.
"""

import json
import pathlib
import sys

SAIDA = pathlib.Path(__file__).resolve().parent.parent / "pesquisa" / "raw"

VIDEOS = {
    "primo-pobre-consorcio-vale-a-pena": "https://www.youtube.com/watch?v=-ec5K1B1rmo",
    "resposta-primo-pobre-consorcio": "https://www.youtube.com/watch?v=pMl5zBtOpiQ",
    "rebatendo-criticas-consorcio-golpe": "https://www.youtube.com/watch?v=VO1I8FWeE0A",
    "vale-a-pena-investir-no-consorcio": "https://www.youtube.com/watch?v=RzcagXWwoAE",
}

PAGINAS_ADEMICON = [
    "https://www.ademicon.com.br/",
    "https://www.ademicon.com.br/consorcio-de-imoveis",
    "https://www.ademicon.com.br/consorcio-de-veiculos",
    "https://www.ademicon.com.br/consorcio-de-servicos",
    "https://www.ademicon.com.br/ademicon-credito",
    "https://www.ademicon.com.br/credito/cota-equity/",
    "https://www.ademicon.com.br/a-ademicon",
    "https://ademiconusa.com/",
]

LIMITE_COMENTARIOS = 1000


def _comentarios_yt_dlp(url):
    import yt_dlp

    opcoes = {
        "skip_download": True,
        "getcomments": True,
        "quiet": True,
        "extractor_args": {"youtube": {"max_comments": [str(LIMITE_COMENTARIOS), "all", "100"], "comment_sort": ["top"]}},
    }
    with yt_dlp.YoutubeDL(opcoes) as ydl:
        info = ydl.extract_info(url, download=False)
    return [
        {"texto": c.get("text"), "curtidas": c.get("like_count"), "resposta": c.get("parent") != "root"}
        for c in (info.get("comments") or [])
    ]


def _comentarios_downloader(url):
    from youtube_comment_downloader import SORT_BY_POPULAR, YoutubeCommentDownloader

    comentarios = []
    for c in YoutubeCommentDownloader().get_comments_from_url(url, sort_by=SORT_BY_POPULAR):
        comentarios.append({"texto": c.get("text"), "curtidas": c.get("votes"), "resposta": c.get("reply")})
        if len(comentarios) >= LIMITE_COMENTARIOS:
            break
    return comentarios


def raspar_youtube():
    for nome, url in VIDEOS.items():
        comentarios = []
        for metodo in (_comentarios_yt_dlp, _comentarios_downloader):
            try:
                comentarios = metodo(url)
            except Exception as erro:  # biblioteca ausente, vídeo removido, rede bloqueada etc.
                print(f"[youtube] {nome}: {metodo.__name__} falhou ({erro})")
                continue
            if comentarios:
                break
        destino = SAIDA / f"youtube-{nome}.json"
        destino.write_text(json.dumps(comentarios, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[youtube] {nome}: {len(comentarios)} comentários -> {destino}")


def raspar_site():
    import requests
    from bs4 import BeautifulSoup

    cabecalho = {"User-Agent": "Mozilla/5.0 (pesquisa de mercado)"}
    for url in PAGINAS_ADEMICON:
        try:
            resposta = requests.get(url, headers=cabecalho, timeout=30)
            resposta.raise_for_status()
        except Exception as erro:
            print(f"[site] {url}: falhou ({erro})")
            continue
        sopa = BeautifulSoup(resposta.text, "html.parser")
        for tag in sopa(["script", "style", "noscript"]):
            tag.decompose()
        texto = "\n".join(linha.strip() for linha in sopa.get_text("\n").splitlines() if linha.strip())
        nome = url.split("//", 1)[1].strip("/").replace("/", "_") or "home"
        destino = SAIDA / f"site-{nome}.txt"
        destino.write_text(f"URL: {url}\n\n{texto}", encoding="utf-8")
        print(f"[site] {url}: {len(texto)} caracteres -> {destino}")


if __name__ == "__main__":
    SAIDA.mkdir(parents=True, exist_ok=True)
    alvo = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    if alvo in ("tudo", "youtube"):
        raspar_youtube()
    if alvo in ("tudo", "site"):
        raspar_site()
