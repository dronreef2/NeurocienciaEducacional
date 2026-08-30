# Pré-registros OSF

5 pré-registros prontos para submissão ao [Open Science Framework](https://osf.io/).

## Arquivos

| Arquivo | Projeto | Formato | Metadata Rica |
|---|---|---|---|
| `P01-osf.json` | IA e MToM (qualitativo) | OSF v2 | — |
| `P02-osf.json` | Gamificação e FE (ECR 2×4) | Flat custom | 8 campos (`P02-osf.metadata.json`) |
| `P03-osf.json` | EEG Tela vs Papel | Flat custom | 8 campos (`P03-osf.metadata.json`) |
| `P04-osf.json` | IA e FE (SEM) | OSF v2 | — |
| `P05-osf.json` | COORTE-INF (LGCM) | OSF v2 | — |

> **Por que 2 formatos?** OSF v2 é o schema aceito pela API. O formato flat (P02, P03) preserva
> detalhes ricos (hipóteses, design, plano de análise) que a API não aceita, e esses são salvos
> em arquivos `*.metadata.json` companion para upload como **arquivo suplementar** da registration.

## Como submeter

### 1. Obtenha um token OSF

Acesse [osf.io/settings/tokens/](https://osf.io/settings/tokens/) e crie um token com escopo `osf.full_write`.

### 2. Configure o token

**macOS/Linux:**
```bash
export OSF_TOKEN="seu-token-aqui"
```

**Windows PowerShell:**
```powershell
$env:OSF_TOKEN = "seu-token-aqui"
```

### 3. Valide antes de submeter

```bash
python3 analise/Python/scripts/osf_submit.py --validate
```

Saída esperada:
```
🔍 Validando 5 pré-registros...
  ✅ P01-osf.json  [formato: v2, metadata rica: 0 campos]
  ✅ P02-osf.json  [formato: flat, metadata rica: 8 campos]
  ✅ P03-osf.json  [formato: flat, metadata rica: 8 campos]
  ✅ P04-osf.json  [formato: v2, metadata rica: 0 campos]
  ✅ P05-osf.json  [formato: v2, metadata rica: 0 campos]

✅ Todos os 5 pré-registros são válidos!
```

### 4. Submeta todos

```bash
python3 analise/Python/scripts/osf_submit.py --all
```

Ou um por vez:
```bash
python3 analise/Python/scripts/osf_submit.py --prereg P01
```

### 5. Modos úteis

```bash
# Simular (não submete, só valida)
python3 analise/Python/scripts/osf_submit.py --all --dry-run

# Diretório customizado
python3 analise/Python/scripts/osf_submit.py --all --dir /outro/path
```

## Após a submissão

Cada pré-registro submetido gera um arquivo `*.submitted.json` com:

```json
{
  "submitted_at": "2026-08-30T15:30:00",
  "registration_id": "abc12",
  "url": "https://osf.io/abc12",
  "title": "...",
  "rich_metadata_file": "P02-osf.metadata.json"
}
```

**Próximo passo manual:** faça upload dos `*.metadata.json` (P02, P03) como **arquivo suplementar** da registration no OSF — eles contêm as hipóteses, design e plano de análise completos.

## Testes

```bash
python3 analise/Python/tests/test_osf_submit_stdlib.py
```

Cobre: detecção de formato, validação de schema, conversão flat→v2, extração de metadata rica, dry-run, submissão real (mockada).

## Dependências

- `requests` (recomendado) — fallback para `urllib` se ausente
- `pyyaml` (não necessário, JSON é nativo)
- Python 3.8+
