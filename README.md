# Sistema de Cotações de Moedas (Câmbio) - TCP Cliente-Servidor

Sistema distribuído cliente-servidor usando Sockets TCP para provedor de cotações de moedas com suporte a múltiplas requisições  simultâneas.

## 📋 Requisitos

- Python 3.7 ou superior
- Nenhuma biblioteca externa necessária (apenas bibliotecas padrão)

## 🚀 Como Executar

### 1. Iniciar o Servidor

Abra um terminal e execute:

```bash
python server.py
```

O servidor iniciará na porta 5000 por padrão e começará a aceitar conexões.

**Saída esperada:**

```
[SERVIDOR] Iniciado em localhost:5000
[SERVIDOR] Aguardando conexões...
```

### 2. Iniciar o Cliente

Em outro terminal, execute:

```bash
python client.py
```

**Opcional:** Especificar host e porta:

```bash
python client.py localhost 5000
```

## 📝 Comandos Disponíveis

### LIST [moeda_base]

Lista todas as moedas e suas cotações em relação a uma moeda base (padrão: USD).

**Exemplos:**

```
>>> LIST
>>> LIST BRL
>>> LIST EUR
```

### RATE <origem> <destino>

Retorna a taxa de câmbio atual entre duas moedas específicas.

**Exemplos:**

```
>>> RATE USD BRL
>>> RATE EUR USD
>>> RATE BRL JPY
```

### CONVERT <origem> <destino> <valor>

Converte um valor de uma moeda para outra.

**Exemplos:**

```
>>> CONVERT USD BRL 100
>>> CONVERT BRL EUR 500
>>> CONVERT JPY USD 10000
```

### QUIT

Encerra a conexão com o servidor.

```
>>> QUIT
```

## 💱 Moedas Disponíveis

O sistema suporta as seguintes moedas:

- **USD** - Dólar Americano
- **BRL** - Real Brasileiro
- **EUR** - Euro
- **GBP** - Libra Esterlina
- **JPY** - Iene Japonês
- **CAD** - Dólar Canadense
- **AUD** - Dólar Australiano
- **CHF** - Franco Suíço
- **CNY** - Yuan Chinês
- **MXN** - Peso Mexicano

## 🔄 Funcionalidades

### Servidor

- ✅ Armazena taxas de câmbio em memória
- ✅ Atualização periódica automática das cotações (a cada 5 segundos)
- ✅ Suporte a múltiplas conexões concorrentes usando threads
- ✅ Thread-safe com uso de locks para acesso às cotações
- ✅ Garantia de entrega com TCP
- ✅ Tratamento de erros robusto

### Cliente

- ✅ Interface interativa via linha de comando
- ✅ Suporte a todos os comandos especificados
- ✅ Conexão confiável via TCP
- ✅ Tratamento de erros e desconexões

## 🧪 Testando Múltiplas Conexões

Para testar a concorrência, abra vários terminais e execute o cliente em cada um:

**Terminal 1:**

```bash
python client.py
>>> LIST USD
```

**Terminal 2:**

```bash
python client.py
>>> RATE USD BRL
```

**Terminal 3:**

```bash
python client.py
>>> CONVERT BRL USD 1000
```

Todos os clientes serão atendidos simultaneamente pelo servidor.

## 📊 Exemplo de Sessão Completa

```
$ python client.py
Conectado ao servidor localhost:5000

==================================================
SISTEMA DE COTAÇÕES DE MOEDAS
==================================================

Comandos disponíveis:
  LIST [moeda_base]          - Lista todas as cotações
  RATE <origem> <destino>    - Taxa de câmbio
  CONVERT <origem> <destino> <valor> - Converter valor
  QUIT                       - Sair

Exemplos:
  LIST USD
  RATE BRL USD
  CONVERT USD BRL 100
==================================================

>>> LIST USD
Cotações em relação a USD:
----------------------------------------
AUD: 1.5300
BRL: 4.9500
CAD: 1.3600
CHF: 0.8800
CNY: 7.2400
EUR: 0.9200
GBP: 0.7900
JPY: 149.5000
MXN: 17.1200
USD: 1.0000
----------------------------------------

>>> RATE USD BRL
TAXA: 1 USD = 4.9500 BRL

>>> CONVERT USD BRL 100
CONVERSÃO: 100.00 USD = 495.00 BRL

>>> QUIT
BYE

Conexão encerrada.
```

## 🔧 Estrutura do Projeto

```
.
├── server.py          # Servidor de cotações
├── client.py          # Cliente interativo
└── README.md          # Este arquivo
```

## ⚙️ Detalhes Técnicos

### Protocolo TCP

- Garantia de entrega de dados
- Ordenação de pacotes
- Controle de fluxo
- Ideal para dados financeiros onde precisão é crítica

### Concorrência

- Cada cliente é atendido em uma thread separada
- Lock (mutex) protege acesso às cotações durante leitura/escrita
- Thread daemon atualiza cotações periodicamente

### Simulação de Mercado

- Cotações variam aleatoriamente entre -1% e +1% a cada 5 segundos
- Simula volatilidade real do mercado de câmbio

## 🛡️ Tratamento de Erros

O sistema trata diversos cenários:

- Comandos inválidos
- Moedas não encontradas
- Valores inválidos para conversão
- Desconexões inesperadas
- Erros de rede

## 📚 Referências

- Socket Programming em Python: https://docs.python.org/3/library/socket.html
- Threading em Python: https://docs.python.org/3/library/threading.html

---

**Desenvolvido como projeto de Introdução aos Sistemas Distribuídos e Redes de Computadores**
