# Hungarian Algorithm Implementation

Este repositório contém uma implementação do Algoritmo Húngaro para resolver o problema de matching máximo em grafos bipartidos ponderados, junto com um gerador de instâncias para testes.

## Estrutura do Projeto

```
.
├── hungarian.py      # Implementação do Algoritmo Húngaro
├── generator.py      # Gerador de instâncias
├── instances/        # Diretório para instâncias geradas
└── results/          # Diretório para resultados do algoritmo
```

## Gerador de Instâncias

O gerador de instâncias (`generator.py`) cria grafos bipartidos aleatórios com pesos nas arestas.

### Uso do Gerador

```bash
python generator.py n1 n2 [opções]
```

### Parâmetros Obrigatórios:
- `n1`: Número de vértices na primeira partição
- `n2`: Número de vértices na segunda partição

### Parâmetros Opcionais:
- `--min-weight`: Peso mínimo das arestas (padrão: 1.0)
- `--max-weight`: Peso máximo das arestas (padrão: 100.0)
- `--density`: Densidade do grafo (0 a 1) (padrão: 0.7)
- `--num-instances`: Número de instâncias a gerar (padrão: 1)
- `--output-dir`: Diretório para salvar as instâncias (padrão: 'instances')

### Exemplos de Uso do Gerador:

```bash
# Gerar uma única instância
python generator.py 5 5 --min-weight 1 --max-weight 10 --density 0.6

# Gerar 5 instâncias diferentes
python generator.py 10 10 --min-weight 1 --max-weight 100 --density 0.8 --num-instances 5

# Especificar diretório personalizado
python generator.py 7 7 --output-dir "meus_testes"
```

## Algoritmo Húngaro

O algoritmo húngaro (`hungarian.py`) encontra o matching perfeito de peso máximo em um grafo bipartido ponderado.

### Uso do Algoritmo

```bash
python hungarian.py arquivo_entrada [opções]
```

### Parâmetros:
- `arquivo_entrada`: Caminho para o arquivo de entrada contendo o grafo (obrigatório)
- `--output-dir`: Diretório para salvar o resultado (padrão: 'results')
- `--output-file`: Nome do arquivo de saída (padrão: nome_do_arquivo_entrada_results.txt)

### Exemplos de Uso do Algoritmo:

```bash
# Uso básico
python hungarian.py instances/grafo.txt

# Especificar diretório de saída
python hungarian.py instances/grafo.txt --output-dir "meus_resultados"

# Especificar nome do arquivo de saída
python hungarian.py instances/grafo.txt --output-file "resultado_final.txt"

# Especificar ambos
python hungarian.py instances/grafo.txt --output-dir "meus_resultados" --output-file "final.txt"
```

### Formato do Arquivo de Entrada

```
n1 n2 m
v1 v2 peso
v1 v2 peso
...
```
Onde:
- Primeira linha: 
  - `n1`: Número de vértices na primeira partição
  - `n2`: Número de vértices na segunda partição
  - `m`: Número de arestas
- Linhas seguintes:
  - `v1`: Vértice da primeira partição (0 a n1-1)
  - `v2`: Vértice da segunda partição (0 a n2-1)
  - `peso`: Peso da aresta

### Formato do Arquivo de Saída

O arquivo de resultado contém:
- Tempo de execução em segundos
- Peso total do matching encontrado
- Lista de pares de vértices que formam o matching

### Exemplo de Execução Completa

1. Primeiro, gere uma instância:
```bash
python generator.py 5 5 --min-weight 1 --max-weight 10 --density 0.7
```

2. Execute o algoritmo húngaro na instância gerada:
```bash
python hungarian.py instances/bipartite_n1_5_n2_5_d_70_1.txt --output-dir "resultados_teste"
```

## Dicas de Uso

1. Para testes pequenos:
```bash
python generator.py 3 3 --density 0.5 --min-weight 1 --max-weight 5
python hungarian.py instances/bipartite_n1_3_n2_3_d_50_1.txt
```

2. Para testes maiores:
```bash
python generator.py 50 50 --density 0.3 --num-instances 3
```

3. Para batch testing:
```bash
mkdir -p resultados_batch
for file in instances/*; do
    python hungarian.py "$file" --output-dir "resultados_batch"
done
```

## Script de Experimentos

O script `teste.py` permite executar experimentos com múltiplas configurações de tamanhos de grafos, densidades e faixas de pesos, automatizando a geração de instâncias, execução do algoritmo húngaro e coleta de resultados.

### Uso do Script de Experimentos

```bash
python teste.py
```

O script utiliza configurações pré-definidas que podem ser alteradas diretamente no código. Por padrão, ele realiza os seguintes passos:

1. Gera grafos bipartidos para diferentes combinações de:
   - Tamanhos (`sizes`): Listas de tuplas (n1, n2)
   - Densidades (`densities`): Listas de valores (0 a 1)
   - Faixas de peso (`weight_ranges`): Listas de tuplas (peso mínimo, peso máximo)
2. Executa o algoritmo húngaro em cada instância gerada.
3. Salva os resultados detalhados e estatísticas resumidas em um arquivo Excel no formato `hungarian_experiments_<timestamp>.xlsx`.

### Exemplos de Configuração

No arquivo `teste.py`, as configurações padrão incluem:

```python
sizes = [
    (50, 50),
    (100, 100),
    (250, 250),
]

densities = [0.2, 0.3, 0.4, 0.6, 0.7, 0.8]

weight_ranges = [
    (1, 10),
    (1, 100),
    (1, 1000)
]
```

Para alterar, edite esses valores diretamente no script conforme necessário. O parâmetro `instances_per_config` define quantas instâncias serão geradas para cada combinação de configuração (padrão: 3).

### Resultado do Script

Após a execução, o script:
- Cria instâncias temporárias em um diretório local.
- Gera um arquivo Excel com os resultados detalhados e resumos estatísticos para cada combinação de peso.
- Remove os arquivos temporários após a execução.

## Considerações

- O gerador cria grafos não necessariamente completos, controlados pelo parâmetro `density`
- O algoritmo húngaro encontrará um matching máximo se ele existir
- Para grafos muito grandes, considere usar valores menores de densidade
- O tempo de execução aumenta com o tamanho do grafo e número de arestas

## Requisitos

- Python 3.6 ou superior
- NumPy
- Pandas
- XlsxWriter