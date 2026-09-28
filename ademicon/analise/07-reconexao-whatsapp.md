# 07 — Reconexão pelo WhatsApp (amigos e conhecidos)

> Método do líder: **reconectar primeiro, vender nunca na primeira conversa.** "Ser intencional, não interesseiro." "O brasileiro adora comprar, mas não gosta que vendam para ele." "A gente só sabe da vida de alguém perguntando."
> Ferramenta: [`../ferramentas/reconexao.py`](../ferramentas/reconexao.py) — importa os contatos, escreve a 1ª mensagem personalizada e monta o lote do dia com botões do WhatsApp.

---

## 1. As 4 fases da conversa

| Fase | Objetivo | Quem fala mais | Duração |
|---|---|---|---|
| **1. Reabrir** | Mandar um oi genuíno, lembrando de onde vocês se conhecem | Você (1 mensagem) | Dia 1 |
| **2. Reconectar** | Perguntar da vida: família, filhos, trabalho, casa, planos. **Revisitar a lembrança em comum.** | **Ele** (você pergunta, ele conta) | 1–5 dias |
| **3. Gancho "lembrei de você"** | Só quando **ele perguntar** "e você, o que tá fazendo?" | Você, curto | Quando surgir |
| **4. Convite** | Café ou 15 minutos para explicar pessoalmente | Você | Mesma conversa |

**Regra de ouro**: você **não** fala de trabalho até ele perguntar. Se ele não perguntar em 3–5 dias de conversa, tudo bem: a amizade foi retomada, e a fase 3 acontece naturalmente mais pra frente (ou ele vê seus stories).

---

## 2. Fase 1 — Primeira mensagem (o script gera automático)
Exemplos que o `reconexao.py` produz:
- "Fala, João! Tava lembrando do churrasco na casa do Beto e pensei em você na hora 😄 Quanto tempo! Como você tá?"
- "Fala, Maria! Lembrei da época da faculdade e pensei em você. Quanto tempo! Como você tá?"

**Dica**: 10 segundos preenchendo a coluna *memória* na planilha multiplicam a taxa de resposta. Uma lembrança específica mostra que não é mensagem em massa.

**Melhor ainda**: mande **áudio** de 15–20 s para os mais próximos, falando a mesma coisa. Áudio = gente de verdade.

---

## 3. Fase 2 — Perguntas de reconexão (use 3 a 5, não todas)
**Vida pessoal**
- "E aí, casou? Tem filhos? Quantos anos eles têm já?"
- "Ainda mora no mesmo lugar?"
- "E seus pais, como estão?"

**Lembrança em comum**
- "Você ainda fala com o pessoal da [turma/time/empresa]?"
- "Lembra de [história]? Até hoje eu dou risada disso."

**Trabalho e planos** (é aqui que aparece a dor, sem você forçar)
- "E o trabalho, ainda tá na [empresa]? Tá gostando?"
- "E os planos pros próximos anos? Casa própria, trocar de carro, alguma coisa grande vindo?"
- "Pagando aluguel ainda ou já comprou o seu canto?"

> **Anote tudo na coluna observações da planilha**: casado, filhos, aluguel, financiamento, carro, empresa, planos. Isso vira o código R/C/D do [sistema de prospecção](06-sistema-de-prospeccao.md).

---

## 4. Fase 3 — Quando ele perguntar "e você?" / "qual a intenção?"
> "Nada não, irmão, só pensei em você mesmo. Sabe por quê? Tô trabalhando numa empresa aqui e, numa das coisas que eu vi, lembrei de você na hora."

Se ele perguntar "o que você tá fazendo?":
> "Cara, é difícil explicar por mensagem e eu não quero te explicar pela metade. Bora marcar um café? A gente volta a se ver e eu te conto. Tenho certeza que vai fazer diferença pra você."

**Por que funciona**: "lembrei de você" levanta o ego; "difícil explicar por mensagem" gera curiosidade; o café mantém a amizade no centro.

---

## 5. Fase 4 — Convite e agenda
- **Presencial (café/almoço)** para amigos próximos e quem mora perto.
- **Videochamada de 15 min** para quem está longe ou sem tempo: "15 minutinhos, pode ser no seu horário de almoço."
- Proponha **dois horários concretos**: "Quinta 19h ou sábado 10h, qual fica melhor?"
- Na reunião: siga o **diagnóstico de 15 minutos** e a **árvore de decisão** do [sistema de prospecção](06-sistema-de-prospeccao.md).

---

## 6. O que NUNCA fazer
- ❌ Mandar "oi, sumido" e na mensagem seguinte já falar de consórcio.
- ❌ Mandar link, tabela ou simulação sem ele pedir.
- ❌ Copiar e colar a mesma mensagem para todo mundo (o script varia os textos; ajuste se quiser).
- ❌ Mais de ~30 conversas novas por dia pelo número pessoal (o WhatsApp pode restringir o número).
- ❌ Insistir: se não responder, **uma** retomada leve 7–10 dias depois ("Vi [algo] e lembrei de você de novo 😄"). Depois disso, deixa.

---

## 7. Ritmo e métricas
| Métrica | Meta semanal (início) |
|---|---|
| Mensagens de reconexão enviadas | 100–150 (20–30 por dia útil) |
| Taxa de resposta | > 50% (com memória preenchida) |
| Conversas que chegam na fase 3 | 15–25% |
| Cafés/reuniões marcados | 8–12 |

---

## 8. Rotina diária (15–20 minutos)
1. `py ademicon/ferramentas/reconexao.py lote --quantidade 25`
2. Na página que abrir: revisar, trocar para áudio nos mais próximos, e apertar **Abrir no WhatsApp → Enviar** em cada um.
3. Responder quem respondeu ontem (fase 2), anotando as informações na planilha.
4. Marcar os cafés/reuniões de quem chegou na fase 3.

## 9. Passo a passo de instalação (uma vez)
No PowerShell:
```powershell
cd $HOME\boa
git pull --no-rebase --no-edit origin claude/fervent-ramanujan-m05uby
```
Exporte os contatos:
- **Android**: abra contacts.google.com → Exportar → "Google CSV".
- **iPhone**: icloud.com/contacts → selecionar todos → Exportar vCard.

Importe (troque pelo caminho do seu arquivo):
```powershell
py ademicon/ferramentas/reconexao.py importar "$HOME\Downloads\contacts.csv"
```
Abra `ademicon-dados\contatos.csv` (na sua pasta de usuário) no Excel e preencha **grupo**, **memoria** (começando com do/da/de) e **prioridade** para as pessoas mais importantes. Marque **x** na coluna **pular** para quem não deve receber.

> Seus contatos ficam em `C:\Users\fecoe\ademicon-dados\`, **fora do repositório**, porque o repositório é público.
