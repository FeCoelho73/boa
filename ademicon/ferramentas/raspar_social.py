"""Coleta comentários do Instagram e do Facebook usando o SEU navegador (com o seu login).

Como funciona:
  1. Abre um Chromium com um perfil salvo em ademicon/ferramentas/.perfil-navegador
     (o login fica guardado para as próximas vezes; a pasta não vai para o GitHub).
  2. Na primeira vez, você faz login no Instagram/Facebook na janela que abrir e aperta Enter no terminal.
  3. Para cada perfil, pega os últimos posts; para cada post, abre, carrega mais comentários e salva o texto.

Saída: ademicon/pesquisa/raw/instagram-*.json e facebook-*.json

Instalação (uma vez, no PowerShell, dentro da pasta boa):
  py -m pip install playwright
  py -m playwright install chromium

Uso:
  py ademicon/ferramentas/raspar_social.py                  # alvos padrão abaixo
  py ademicon/ferramentas/raspar_social.py --posts 5        # menos posts por perfil
  py ademicon/ferramentas/raspar_social.py --url https://www.instagram.com/p/XXXX/   # um post específico
  py ademicon/ferramentas/raspar_social.py --automatico     # sem pausa de login (agendamento)
"""

import argparse
import json
import pathlib
import re
import time

from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent
SAIDA = RAIZ.parent / "pesquisa" / "raw"
PERFIL_NAVEGADOR = RAIZ / ".perfil-navegador"

# Perfis cujos últimos posts serão lidos.
PERFIS_INSTAGRAM = [
    "ademicon",                        # oficial
    "mairaaespecialistaemconsorcio",   # consultora-influenciadora (~95 mil)
    "hardcopy_oficial",                # referência de copy
    "primopobre",                      # finanças populares
]
PAGINAS_FACEBOOK = [
    "https://www.facebook.com/ConsorcioAdemicon",   # oficial (~128 mil seguidores)
]
# Posts específicos que sempre entram.
POSTS_FIXOS = [
    "https://www.instagram.com/p/DdF3cDrAyJt/",   # post do Hard Copy enviado no início
    "https://www.instagram.com/p/DTdJYS2jn0o/",   # Ademicon no BBB 2026
]

MAX_CLIQUES_MAIS_COMENTARIOS = 25


def esperar_login(pagina):
    for url in ("https://www.instagram.com/", "https://www.facebook.com/"):
        pagina.goto(url)
        time.sleep(3)
    input(
        "\n>>> Se ainda não estiver logado, faça login no Instagram e no Facebook na janela aberta.\n"
        ">>> Quando terminar (ou se já estiver logado), aperte Enter aqui...\n"
    )


def links_do_perfil_instagram(pagina, usuario, quantidade):
    pagina.goto(f"https://www.instagram.com/{usuario}/")
    time.sleep(5)
    links = []
    for _ in range(6):
        for href in pagina.eval_on_selector_all("a[href]", "els => els.map(e => e.getAttribute('href'))"):
            if href and re.match(r"^/(?:[\w.]+/)?(p|reel)/[\w-]+/?$", href):
                url = "https://www.instagram.com" + href
                if url not in links:
                    links.append(url)
        if len(links) >= quantidade:
            break
        pagina.mouse.wheel(0, 3000)
        time.sleep(2)
    return links[:quantidade]


def links_da_pagina_facebook(pagina, url, quantidade):
    pagina.goto(url)
    time.sleep(6)
    links = []
    for _ in range(8):
        for href in pagina.eval_on_selector_all("a[href]", "els => els.map(e => e.href)"):
            if href and re.search(r"facebook\.com/.+/(posts|videos|reel)/", href):
                limpo = href.split("?")[0]
                if limpo not in links:
                    links.append(limpo)
        if len(links) >= quantidade:
            break
        pagina.mouse.wheel(0, 4000)
        time.sleep(3)
    return links[:quantidade]


def clicar_carregar_mais(pagina, textos):
    for _ in range(MAX_CLIQUES_MAIS_COMENTARIOS):
        clicou = False
        for texto in textos:
            botao = pagina.get_by_role("button", name=re.compile(texto, re.I))
            if botao.count():
                try:
                    botao.first.click(timeout=2000)
                    clicou = True
                    time.sleep(2)
                except Exception:
                    pass
        pagina.mouse.wheel(0, 2500)
        time.sleep(1)
        if not clicou:
            break


def coletar_textos(pagina, seletor):
    textos = pagina.eval_on_selector_all(seletor, "els => els.map(e => e.innerText.trim())")
    vistos, resultado = set(), []
    for t in textos:
        if len(t) < 3 or t in vistos:
            continue
        vistos.add(t)
        resultado.append(t)
    return resultado


def comentarios_instagram(pagina, url):
    pagina.goto(url)
    time.sleep(5)
    clicar_carregar_mais(pagina, [r"carregar mais coment", r"load more comments", r"ver mais coment", r"view more comments", r"ver respostas", r"view replies"])
    legenda_e_comentarios = coletar_textos(pagina, "article span[dir='auto'], div[role='dialog'] span[dir='auto'], main ul span[dir='auto']")
    return legenda_e_comentarios


def comentarios_facebook(pagina, url):
    pagina.goto(url)
    time.sleep(6)
    clicar_carregar_mais(pagina, [r"ver mais coment", r"view more comments", r"mais relevantes", r"respostas", r"replies"])
    return coletar_textos(pagina, "div[role='article'] div[dir='auto']")


def salvar(prefixo, url, textos):
    nome = re.sub(r"[^\w-]+", "-", url.split("//", 1)[1]).strip("-")[:90]
    destino = SAIDA / f"{prefixo}-{nome}.json"
    destino.write_text(json.dumps({"url": url, "textos": textos}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{prefixo}] {len(textos):4d} textos  <- {url}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--posts", type=int, default=8, help="posts por perfil/página")
    parser.add_argument("--url", action="append", help="post específico (pode repetir)")
    parser.add_argument("--automatico", action="store_true", help="não pausa para login (usar depois do primeiro login)")
    args = parser.parse_args()

    SAIDA.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        contexto = p.chromium.launch_persistent_context(str(PERFIL_NAVEGADOR), headless=False, locale="pt-BR")
        pagina = contexto.pages[0] if contexto.pages else contexto.new_page()
        if not args.automatico:
            esperar_login(pagina)

        alvos_ig = list(args.url or [])
        alvos_fb = [u for u in alvos_ig if "facebook.com" in u]
        alvos_ig = [u for u in alvos_ig if "instagram.com" in u]
        if not args.url:
            alvos_ig += POSTS_FIXOS
            for usuario in PERFIS_INSTAGRAM:
                try:
                    alvos_ig += links_do_perfil_instagram(pagina, usuario, args.posts)
                except Exception as erro:
                    print(f"[instagram] perfil {usuario}: falhou ({erro})")
            for url in PAGINAS_FACEBOOK:
                try:
                    alvos_fb += links_da_pagina_facebook(pagina, url, args.posts)
                except Exception as erro:
                    print(f"[facebook] página {url}: falhou ({erro})")

        for url in dict.fromkeys(alvos_ig):
            try:
                salvar("instagram", url, comentarios_instagram(pagina, url))
            except Exception as erro:
                print(f"[instagram] {url}: falhou ({erro})")
        for url in dict.fromkeys(alvos_fb):
            try:
                salvar("facebook", url, comentarios_facebook(pagina, url))
            except Exception as erro:
                print(f"[facebook] {url}: falhou ({erro})")

        contexto.close()
    print("\nPronto. Agora rode: git add -A ; git commit -m \"comentarios instagram facebook\" ; git push")


if __name__ == "__main__":
    main()
