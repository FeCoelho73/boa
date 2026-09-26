# 04 — Como o consultor é pago (comissão escalonada de 3%)

> ✅ Estrutura **dita literalmente no fim da apresentação**: *"1,1% para 10 parcelas; 0,9% pago nas 11, 12 e 13; 0,3% de bônus na 15; e 0,7% vitalício."* Ainda assim, **[CONFIRMAR por escrito]**: o que acontece se o cliente atrasar/cancelar, se é igual para todos os produtos e se a vitalícia é herdável (alguém perguntou "pode deixar para os filhos?").
>
> Por que é parcelada: antes a comissão era paga à vista e **estornada** se o cliente parasse de pagar. O modelo parcelado "obriga a gente a cuidar do cliente" e cria um colchão de renda (se você parar 3 meses, continua recebendo).

## 1. A estrutura (sobre o valor da carta vendida)

| Parcela paga pelo cliente | % da carta por mês | Exemplo: carta de R$ 1.000.000 |
|---|---|---|
| 1ª à 10ª | 0,11% ao mês (1,1% no total) | R$ 1.100/mês por 10 meses = R$ 11.000 |
| 11ª, 12ª e 13ª | 0,30% ao mês ("triplica") (0,9% no total) | R$ 3.000/mês por 3 meses = R$ 9.000 |
| 15ª | 0,30% (bônus) | R$ 3.000 |
| 16ª até o fim do grupo (~205–220 meses) | 0,7% diluído ("vitalícia") | ≈ R$ 35/mês por ~17 anos = R$ 7.000 |
| **Total** | **3,0%** | **R$ 30.000** |

O que foi dito na apresentação, em outras palavras:
- "Vendeu R$ 1 milhão no mês → mês que vem entra R$ 1.100." Se repetir todo mês, soma R$ 1.100 a cada mês.
- "No 11º, 12º, 13º mês a comissão triplica."
- "Depois do 15º mês acaba o comissionamento… mas vem a 0,7 vitalícia até o final do grupo." Com R$ 30–40 mi vendidos/ano, a vitalícia sozinha "já é a escola do filho".

**Relato público** (Glassdoor/Indeed): PJ, 100% comissionado, comissão "fracionada em 13 vezes", sem ajuda de custo — coerente com essa estrutura.

## 2. O efeito "bola de neve" (simulação)

Renda mensal do consultor mantendo um volume de vendas constante todo mês:

| Mês | Vende R$ 1 mi/mês | Vende R$ 2 mi/mês | Vende R$ 3 mi/mês (meta da loja) |
|---|---|---|---|
| 1 | R$ 1.100 | R$ 2.200 | R$ 3.300 |
| 3 | R$ 3.300 | R$ 6.600 | R$ 9.900 |
| 6 | R$ 6.600 | R$ 13.200 | R$ 19.800 |
| 10 | R$ 11.000 | R$ 22.000 | R$ 33.000 |
| 12 | R$ 17.000 | R$ 34.000 | R$ 51.000 |
| 15 | R$ 23.000 | R$ 46.000 | R$ 69.000 |
| 24 | R$ 23.300 | R$ 46.700 | R$ 70.000 |
| 36 | R$ 23.800 | R$ 47.500 | R$ 71.300 |

Cenário "rampa" (R$ 0,5 mi → 1 → 1 → 1,5 → 2 → 2 → R$ 3 mi/mês a partir do 7º mês): mês 6 ≈ R$ 8.800; mês 12 ≈ R$ 31.500; mês 16 ≈ R$ 52.500; mês 24 ≈ R$ 69.600.

**Regra de bolso**: em regime (a partir do 15º mês), **cada R$ 1 milhão vendido por mês ≈ R$ 23 mil de renda mensal**, e a parte vitalícia cresce devagar para sempre.

Script para refazer as contas: [`../fontes/simulador_comissao.py`](../fontes/simulador_comissao.py).

## 3. Implicações estratégicas

1. **Os primeiros 6 meses são de construção.** Mesmo vendendo bem, a renda é baixa no início. Precisa de **reserva financeira** ou outra fonte de renda nesse período.
2. **Ticket alto é tudo.** Uma carta de R$ 1 mi = 10 cartas de R$ 100 mil. Priorizar investidores, PJ, imóvel de alto padrão, multicotas.
3. **Tráfego pago tem payback longo.** Se o custo para conseguir uma venda de R$ 200 mil for R$ 800, a comissão total é R$ 6.000 — ótimo ROI (7,5x) — mas no 1º mês você recebe só R$ 220 dela. **É preciso financiar o caixa do marketing por vários meses.** Começar pequeno e escalar com a renda.
4. **Retenção do cliente = sua renda.** A comissão acompanha as parcelas pagas. Cliente que desiste cedo corta sua renda (e pode gerar estorno). **Vender certo** (capacidade de pagamento real) e **pós-venda** protegem o bolso.
5. **Reunião com o líder no começo**: o novato marca a reunião, o líder (mais experiente) conduz a venda e **100% da comissão fica com o novato** — o líder ganha um percentual pago pela própria Ademicon pela performance da equipe. Use isso nas primeiras semanas: você agenda, o líder fecha, você aprende.
6. **Plano de carreira**: consultor → líder → gestor → licenciado/sócio (abertura de novos escritórios: Brasília, Zona Sul etc.). Ganhos de liderança sobre equipe **[CONFIRMAR regras de override]**. Com seu know-how digital, **gerar leads para uma equipe** pode ser o próximo nível.

## 4. Perguntas para o Fábio sobre remuneração
- [ ] Tabela oficial de comissão (é a mesma para imóvel, auto, pesados, serviços?).
- [ ] A comissão de cada mês depende do cliente pagar aquela parcela? E se atrasar?
- [ ] Regra de **estorno** (até qual parcela?).
- [ ] Cota vendida com lance e contemplada cedo: muda algo na comissão?
- [ ] Existe bônus/campanha por meta (viagens, carros, premiações)?
- [ ] Como funciona o ganho de líder/gestor sobre a equipe?
- [ ] Nota fiscal: preciso de CNPJ (MEI serve? O limite anual do MEI é baixo para essa renda — verificar valor vigente com contador; provavelmente ME no Simples)?
- [ ] A loja fornece leads? Tem verba de marketing compartilhada? Posso anunciar com a marca?
