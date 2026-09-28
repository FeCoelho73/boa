"""Reconexão pelo WhatsApp: importa seus contatos, escreve uma mensagem pessoal para cada um
e gera o lote do dia com botões que abrem o WhatsApp já com o texto pronto (você só aperta Enviar).

Por que não dispara sozinho: envio automático em massa pelo número pessoal leva a banimento
e soa como robô — o oposto de reconexão. Aqui o trabalho chato é automático; o envio é um toque seu.

Seus contatos ficam FORA do repositório (que é público), na pasta:  <sua pasta de usuário>/ademicon-dados/

Passo a passo (PowerShell, dentro da pasta boa):
  1. Exporte os contatos do celular:
       Android: contacts.google.com > Exportar > "Google CSV"  (arquivo contacts.csv)
       iPhone:  icloud.com/contacts > selecionar todos > Exportar vCard (arquivo .vcf)
  2. py ademicon/ferramentas/reconexao.py importar "C:\\Users\\fecoe\\Downloads\\contacts.csv"
  3. (Opcional, recomendado) abra ademicon-dados\\contatos.csv no Excel e preencha, para quem importa:
       grupo      -> escola | faculdade | trabalho | familia | futebol | igreja | academia | vizinho | cliente
       memoria    -> lembrança curta começando com do/da/de (ex.: "do churrasco na casa do Beto", "da época do futsal")
       prioridade -> 1 (alta) a 3 (baixa)
       pular      -> x  (para quem não deve receber)
  4. py ademicon/ferramentas/reconexao.py lote --quantidade 25
       -> abre uma página com 25 cartões; cada botão abre o WhatsApp com a mensagem pronta.
  5. Quando responderem, siga o roteiro de conversa em ademicon/analise/07-reconexao-whatsapp.md
"""

import argparse
import csv
import datetime
import html
import pathlib
import random
import re
import urllib.parse
import webbrowser

DADOS = pathlib.Path.home() / "ademicon-dados"
BASE = DADOS / "contatos.csv"
CAMPOS = ["nome", "telefone", "grupo", "memoria", "prioridade", "pular", "status", "data_lote", "observacoes"]

# Mensagens de reconexão: SEM falar de trabalho, consórcio ou venda. Só retomar a amizade.
MENSAGENS = {
    "com_memoria": [
        "Fala, {nome}! Tava lembrando {memoria} e pensei em você na hora 😄 Quanto tempo! Como você tá?",
        "{nome}, hoje me lembrei {memoria} e na hora pensei em você. Como estão as coisas por aí?",
        "Oi {nome}! Lembrei agora {memoria} 😂 Faz tempo demais que a gente não se fala. Tudo bem com você?",
    ],
    "escola": [
        "Fala, {nome}! Tava vendo umas fotos da época da escola e lembrei de você 😄 Quanto tempo! Como você tá?",
        "{nome}, quanto tempo! Lembrei da turma da escola hoje e você veio na cabeça. Como tá a vida?",
    ],
    "faculdade": [
        "Fala, {nome}! Lembrei da época da faculdade e pensei em você. Quanto tempo! Como você tá?",
        "{nome}, sumido(a)! Tava lembrando da galera da facul hoje. Como estão as coisas?",
    ],
    "trabalho": [
        "Oi {nome}! Lembrei de você hoje, da época em que a gente trabalhava junto. Como você tá? Ainda por lá?",
        "Fala, {nome}! Quanto tempo desde aquela época de trabalho junto. Como tá a vida?",
    ],
    "familia": [
        "Oi {nome}! Tava pensando em você e na família. Faz tempo que a gente não conversa. Como vocês estão?",
    ],
    "futebol": [
        "Fala, {nome}! Lembrei da época da bola e pensei em você 😄 Ainda joga? Como você tá?",
    ],
    "igreja": [
        "Oi {nome}! Lembrei de você hoje, faz tempo que a gente não se fala. Como você e a família estão?",
    ],
    "academia": [
        "Fala, {nome}! Lembrei de você da época da academia. Quanto tempo! Como você tá?",
    ],
    "vizinho": [
        "Oi {nome}! Lembrei de você e da época em que a gente era vizinho. Como vocês estão?",
    ],
    "cliente": [
        "Oi {nome}, tudo bem? Faz tempo que a gente não se fala e lembrei de você hoje. Como estão as coisas por aí?",
    ],
    "padrao": [
        "Fala, {nome}! Quanto tempo! Lembrei de você hoje. Como você tá?",
        "Oi {nome}! Faz tempo demais que a gente não se fala. Tudo bem com você?",
        "{nome}, lembrei de você agora e resolvi mandar um oi. Como estão as coisas?",
    ],
}


def normalizar_telefone(bruto):
    digitos = re.sub(r"\D", "", bruto or "")
    if digitos.startswith("00"):
        digitos = digitos[2:]
    if digitos.startswith("0"):
        digitos = digitos.lstrip("0")
    if len(digitos) in (10, 11):  # DDD + número brasileiro
        digitos = "55" + digitos
    if digitos.startswith("55") and len(digitos) == 12:  # fixo brasileiro: não tem WhatsApp, em geral
        return ""
    return digitos if len(digitos) >= 12 else ""


def ler_base():
    if not BASE.exists():
        return []
    with BASE.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def salvar_base(linhas):
    DADOS.mkdir(parents=True, exist_ok=True)
    with BASE.open("w", encoding="utf-8-sig", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=CAMPOS, extrasaction="ignore")
        escritor.writeheader()
        for linha in linhas:
            escritor.writerow({c: linha.get(c, "") for c in CAMPOS})


def contatos_google_csv(caminho):
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        for linha in csv.DictReader(f):
            nome = " ".join(
                p for p in (linha.get("First Name") or linha.get("Given Name") or "",
                            linha.get("Last Name") or linha.get("Family Name") or "") if p
            ) or linha.get("Name") or linha.get("File As") or ""
            for coluna, valor in linha.items():
                if coluna and "Phone" in coluna and "Value" in coluna and valor:
                    for numero in valor.split(":::"):
                        yield nome.strip(), numero.strip()


def contatos_vcf(caminho):
    nome = ""
    with open(caminho, encoding="utf-8", errors="ignore") as f:
        for linha in f:
            linha = linha.strip()
            if linha.startswith("BEGIN:VCARD"):
                nome = ""
            elif linha.startswith("FN"):
                nome = linha.split(":", 1)[-1]
            elif linha.startswith("TEL"):
                yield nome, linha.split(":", 1)[-1]


def importar(caminho):
    caminho = pathlib.Path(caminho)
    origem = contatos_vcf(caminho) if caminho.suffix.lower() == ".vcf" else contatos_google_csv(caminho)
    base = ler_base()
    existentes = {l["telefone"] for l in base}
    nomes = {l["nome"].strip().lower() for l in base}
    novos = 0
    for nome, numero in origem:
        telefone = normalizar_telefone(numero)
        if not nome or not telefone or telefone in existentes or nome.strip().lower() in nomes:
            continue
        base.append({"nome": nome, "telefone": telefone, "prioridade": "2"})
        existentes.add(telefone)
        nomes.add(nome.strip().lower())
        novos += 1
    salvar_base(base)
    print(f"{novos} contatos novos importados. Total: {len(base)}. Arquivo: {BASE}")
    print("Dica: preencha grupo, memoria e prioridade no Excel para mensagens mais pessoais.")


def primeiro_nome(nome):
    return (nome.split() or [nome])[0].capitalize()


def escrever_mensagem(contato):
    nome = primeiro_nome(contato["nome"])
    memoria = (contato.get("memoria") or "").strip()
    if memoria:
        modelo = random.choice(MENSAGENS["com_memoria"])
        return modelo.format(nome=nome, memoria=memoria)
    grupo = (contato.get("grupo") or "").strip().lower()
    return random.choice(MENSAGENS.get(grupo, MENSAGENS["padrao"])).format(nome=nome)


def gerar_lote(quantidade):
    base = ler_base()
    if not base:
        print("Base vazia. Rode primeiro: reconexao.py importar <arquivo de contatos>")
        return
    pendentes = [l for l in base if not l.get("status") and (l.get("pular") or "").strip().lower() != "x"]
    pendentes.sort(key=lambda l: (l.get("prioridade") or "2", not l.get("memoria"), not l.get("grupo")))
    lote = pendentes[:quantidade]
    hoje = datetime.date.today().isoformat()

    cartoes = []
    for contato in lote:
        mensagem = escrever_mensagem(contato)
        link = f"https://wa.me/{contato['telefone']}?text={urllib.parse.quote(mensagem)}"
        cartoes.append(
            f"<div class='c'><b>{html.escape(contato['nome'])}</b> <small>{html.escape(contato.get('grupo') or '')}</small>"
            f"<p>{html.escape(mensagem)}</p><a href='{link}' target='_blank'>Abrir no WhatsApp</a></div>"
        )
        contato["status"] = "mensagem enviada"
        contato["data_lote"] = hoje

    pagina = DADOS / f"lote-{hoje}.html"
    pagina.write_text(
        "<!doctype html><meta charset='utf-8'><title>Reconexão " + hoje + "</title>"
        "<style>body{font-family:sans-serif;max-width:640px;margin:20px auto;padding:0 16px}"
        ".c{border:1px solid #ccc;border-radius:10px;padding:12px;margin:10px 0}"
        "a{display:inline-block;background:#25D366;color:#fff;padding:8px 14px;border-radius:8px;text-decoration:none}"
        "p{margin:8px 0}</style>"
        f"<h2>Reconexão — {hoje} ({len(lote)} pessoas)</h2>"
        "<p>Revise, ajuste se quiser e envie. Não fale de trabalho agora: o objetivo é só retomar a conversa.</p>"
        + "".join(cartoes),
        encoding="utf-8",
    )
    salvar_base(base)
    print(f"Lote com {len(lote)} pessoas: {pagina}")
    print(f"Restam {len(pendentes) - len(lote)} contatos na fila.")
    webbrowser.open(pagina.as_uri())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reconexão pelo WhatsApp")
    sub = parser.add_subparsers(dest="comando", required=True)
    p_importar = sub.add_parser("importar", help="importa contatos (Google CSV ou .vcf)")
    p_importar.add_argument("arquivo")
    p_lote = sub.add_parser("lote", help="gera o lote do dia")
    p_lote.add_argument("--quantidade", type=int, default=25)
    args = parser.parse_args()
    if args.comando == "importar":
        importar(args.arquivo)
    else:
        gerar_lote(args.quantidade)
