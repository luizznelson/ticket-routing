import pandas as pd
import numpy as np

np.random.seed(42)
n = 10000

urgencias = ['Baixa', 'Média', 'Alta', 'Crítica']
clientes = [f'Cliente {chr(65+i)}' for i in range(12)]  # Cliente A-L
tipos_servico = ['Internet', 'Telefone', 'TV', 'Nuvem', 'Data Center']
origem = ['Autoatendimento', 'Telefone', 'WhatsApp', 'Email', 'App']
responsavel = ['Equipe 1', 'Equipe 2', 'Equipe 3']

df = pd.DataFrame({
    'id': np.arange(1, n+1),
    'urgencia': np.random.choice(urgencias, n, p=[0.28, 0.39, 0.22, 0.11]),
    'cliente': np.random.choice(clientes, n),
    'tipo_servico': np.random.choice(tipos_servico, n, p=[0.45, 0.2, 0.15, 0.12, 0.08]),
    'origem': np.random.choice(origem, n, p=[0.25, 0.27, 0.19, 0.13, 0.16]),
    'tempo_espera': np.random.randint(2, 200, n),  # minutos
    'descricao': np.random.choice([
        'Instabilidade', 'Lentidão', 'Falha total', 'Solicitação de upgrade', 'Problema recorrente', 'Solicitação de reembolso',
        'Queda de sinal', 'Erro de cobrança', 'Mudança de endereço', 'Reclamação atendimento'], n),
    'status': np.random.choice(['Aberto', 'Em andamento', 'Resolvido'], n, p=[0.35, 0.18, 0.47])
})

df.to_csv('data/tickets.csv', index=False)
