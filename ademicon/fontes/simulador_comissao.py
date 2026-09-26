# Simulador da comissão escalonada: 1,1% em 10x, 0,9% nas 11ª-13ª, 0,3% na 15ª, 0,7% vitalícia (apresentação da loja).
# Uso: python3 simulador_comissao.py
# comissão reconstruída por R$ de crédito vendido, por mês após a venda (mês 1 = 1ª parcela)
def sched(m, prazo=205):
    if 1<=m<=10: return 0.0011
    if 11<=m<=13: return 0.003
    if m==15: return 0.003
    if 16<=m<=prazo: return 0.007/(prazo-15)
    return 0
print("total%", sum(sched(m) for m in range(1,300))*100)
def renda(vendas):  # vendas[i] = volume vendido no mês i (1-index)
    out=[]
    for t in range(1,len(vendas)+1):
        out.append(sum(vendas[i-1]*sched(t-i+1) for i in range(1,t+1)))
    return out
for nome,v in [("1M/mes",[1e6]*36),("2M/mes",[2e6]*36),("3M/mes",[3e6]*36),("rampa",[0.5e6,1e6,1e6,1.5e6,2e6,2e6]+[3e6]*30)]:
    r=renda(v); print(nome, [round(r[m-1]) for m in (1,3,6,10,11,12,13,14,15,16,18,24,36)])
