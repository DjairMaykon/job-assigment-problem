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

## Considerações

- O gerador cria grafos não necessariamente completos, controlados pelo parâmetro `density`
- O algoritmo húngaro encontrará um matching máximo se ele existir
- Para grafos muito grandes, considere usar valores menores de densidade
- O tempo de execução aumenta com o tamanho do grafo e número de arestas

## Requisitos

- Python 3.6 ou superior
- NumPy