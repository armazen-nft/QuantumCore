# QuantumCore
# OpenFM Computer (P2P)

Um **Computador FM moderno, open source e peer-to-peer**, capaz de transmitir e receber dados digitais usando **áudio ou rádio FM**, inspirado no histórico sistema de distribuição de software via rádio dos anos 1980.

O **OpenFM Computer** permite que qualquer computador se torne um **nó de transmissão e recepção de dados broadcast**, funcionando mesmo em ambientes **offline ou com infraestrutura mínima**.

Ele utiliza **modulação FSK, pacotes verificáveis e retransmissão P2P**, permitindo que arquivos e dados se propaguem entre nós de forma distribuída.

---

# Visão geral

O OpenFM Computer transforma áudio analógico em um **canal digital de dados**.

Isso permite:

* transmitir arquivos via áudio
* enviar dados via rádio FM
* criar redes P2P offline
* distribuir software ou conhecimento por broadcast

Cada nó da rede pode atuar como:

* transmissor
* receptor
* cache
* retransmissor

Isso cria uma **rede distribuída baseada em broadcast**.

---

# Principais características

* transmissão de dados via áudio ou FM
* modulação digital simples (FSK)
* pacotes verificáveis com CRC
* retransmissão peer-to-peer
* funcionamento offline
* arquitetura modular
* código simples e auditável

Possíveis usos:

* distribuição offline de software
* redes comunitárias
* transmissão de dados em áreas remotas
* pesquisa em comunicação digital
* experimentos educacionais

---

# Arquitetura do sistema

Fluxo geral de transmissão:

```
arquivo
 ↓
compressão
 ↓
segmentação em pacotes
 ↓
codificação de erro
 ↓
modulação FSK
 ↓
áudio / rádio FM
 ↓
demodulação
 ↓
verificação
 ↓
reconstrução do arquivo
```

Cada nó pode armazenar pacotes e **retransmiti-los para ampliar o alcance da rede**.

---

# Estrutura do repositório

```
openfm-computer/

README.md
LICENSE
requirements.txt

/docs
   protocol.md
   architecture.md

/core
   encoder.py
   decoder.py
   packet.py
   fec.py

/modem
   modulator.py
   demodulator.py

/network
   node.py
   peer_discovery.py
   retransmit.py

/audio
   audio_tx.py
   audio_rx.py

/examples
   send_file.py
   receive_file.py
   p2p_node.py
```

---

# Requisitos

* Python 3.10+
* NumPy
* SciPy
* SoundDevice

Instalação:

```bash
pip install -r requirements.txt
```

---

# Instalação

Clone o repositório:

```bash
git clone https://github.com/your-org/openfm-computer
cd openfm-computer
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

# Uso básico

## Transmitir um arquivo

```
python examples/send_file.py arquivo.zip
```

Isso converterá o arquivo em pacotes e os transmitirá via áudio.

---

## Receber dados

```
python examples/receive_file.py
```

O sistema escutará o canal de áudio e reconstruirá os pacotes recebidos.

---

## Executar um nó P2P

```
python examples/p2p_node.py
```

O nó irá:

1. escutar transmissões
2. armazenar pacotes
3. retransmitir pacotes novos

Criando assim uma rede **peer-to-peer por broadcast**.

---

# Modos de operação

## 1. Áudio direto

Computador → alto-falante → microfone de outro computador.

Ideal para testes.

---

## 2. Rádio FM

Computador → transmissor FM → rádio receptor → computador.

Permite alcance de vários quilômetros.

---

## 3. SDR (Software Defined Radio)

Computador → SDR → antena.

Modo mais flexível e avançado.

---

# Protocolo de pacotes

Cada transmissão é dividida em pacotes independentes.

Formato básico:

```
HEADER
VERSION
NODE_ID
PACKET_ID
TOTAL_PACKETS
PAYLOAD_SIZE
CRC
PAYLOAD
```

Tamanho padrão de payload:

```
256 bytes
```

Isso melhora robustez em canais ruidosos.

---

# Modulação

O sistema utiliza **FSK (Frequency Shift Keying)**.

```
bit 0 → 1200 Hz
bit 1 → 2400 Hz
baud → 1200
```

Esse esquema é:

* simples
* robusto
* compatível com canais analógicos

---

# Rede P2P

Cada nó da rede executa um ciclo simples:

```
escutar sinal
↓
decodificar pacotes
↓
armazenar dados
↓
retransmitir pacotes novos
```

Isso permite que dados se propaguem pela rede mesmo sem infraestrutura central.

---

# Possíveis aplicações

* distribuição offline de software
* redes comunitárias de dados
* comunicação de emergência
* experimentos acadêmicos
* distribuição de datasets
* transmissão educacional

---

# Melhorias planejadas

* Reed-Solomon error correction
* LDPC forward error correction
* modulação OFDM
* suporte direto a SDR
* criptografia de pacotes
* compressão avançada
* sincronização automática de nós
* transmissão de grafos semânticos

---

# Contribuindo

Contribuições são bem-vindas.

Você pode ajudar com:

* melhorias no modem
* algoritmos de correção de erro
* suporte a novos hardwares
* documentação
* testes de campo

Abra uma **issue** ou envie um **pull request**.

---

# Licença

Este projeto é distribuído sob a licença **MIT**.

Veja o arquivo LICENSE para detalhes.

---

# Inspirado por

O OpenFM Computer é inspirado pelo histórico **Computador FM**, utilizado nos anos 1980 para transmitir programas de computador via rádio FM.

A proposta deste projeto é **reviver e expandir essa ideia usando tecnologias modernas**, criando um sistema aberto de distribuição digital via broadcast.

---

# Status do projeto

Protótipo funcional.

O objetivo é evoluir o sistema para uma **rede de dados distribuída baseada em broadcast e retransmissão peer-to-peer**.

---

# Autor

Projeto open source criado para experimentação em comunicação digital distribuída.

Contribuições da comunidade são encorajadas.


---

## Forks e propostas

- `FORK_MELISSA.md`: proposta conceitual de comunicação por rádio e arquitetura distribuída para IA pública (visão de pesquisa, segurança e ética).
