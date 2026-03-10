# Protocolo QuantumCore (v2026)

## Fluxo completo: FEC + SDR TX/RX

```mermaid
flowchart TD
    A[Dados originais<br>(arquivo ou mensagem)] --> B[FEC Reed-Solomon<br>encode (32 símbolos)]
    B --> C[Packet 258 bytes<br>Header + FEC payload + CRC32]
    C --> D[Modulador FSK 1200 baud<br>(1200/2400 Hz)]
    D --> E[IQ FM Modulator<br>(baseband para SDR)]
    E --> F[SDR TX<br>HackRF One]
    F --> G[Canal RF<br>(87.5 MHz exemplo)]
    G --> H[SDR RX<br>RTL-SDR]
    H --> I[Demodulador FSK<br>Goertzel + preamble]
    I --> J[Unpack + FEC decode<br>(correção automática)]
    J --> K[Dados recuperados<br>100% íntegros]

    style A fill:#0f0,color:#000
    style K fill:#0f0,color:#000
```

## Detalhes técnicos

- **FEC:** Reed-Solomon (corrige até 16 erros por bloco)
- **Modulação:** FSK áudio → FM IQ (transmissão direta na frequência)
- **Pacote:** 258 bytes (header 6 + payload FEC + CRC)
- **Anti-storm:** TTL + cache SHA256 no `network/node.py`
- **SDR:** HackRF TX / RTL-SDR RX (ou áudio fallback)

- **Taxa:** ~1200 baud (~100-150 bytes/s úteis após FEC)
- **Próximos:** OFDM, criptografia, web dashboard avançado.

---

### Como testar AGORA

```bash
# 1. Teste SDR TX direto (HackRF conectado)
python sdr/sdr_tx.py

# 2. Interface web (abra no navegador)
python web/app.py

# 3. Em outro terminal: envie algo com CLI
python examples/cli.py --mode tx --file teste.txt
```
