# AGENTS.md — Diretório `dados_sinteticos/`

> Instruções para IAs trabalhando com dados sintéticos.
> **Versão:** 1.0 — 2026-09-19

---

## 📂 Conteúdo

```
dados_sinteticos/
├── AGENTS.md                              ← este arquivo
├── catalog.yaml                           ← metadata de 6 datasets
├── P01_diarios_sinteticos.csv             ← 51 linhas (3 crianças × 17 dias)
├── P02_dados_sinteticos.csv               ← 200 linhas (N=200, ECR)
├── P03_eeg_papel.npy                      ← (30, 32, 500) shape
├── P03_eeg_tela.npy                       ← idem
├── P04_dados_sinteticos.csv               ← 400 linhas (N=400, SEM)
└── P05_dados_longitudinais_sinteticos.csv ← 1000 linhas (200 crianças × 5 ondas)
```

---

## 🚨 Regras

1. **Gerador:** `np.random.seed(42)` para reprodutibilidade
2. **Anonimização:** NUNCA usar nomes reais de crianças
3. **LGPD-safe:** podem ser versionados e publicados (não são dados reais)
4. **Catalog:** `catalog.yaml` é a fonte da verdade — atualizar quando adicionar/remover datasets
5. **Uso:** dados sintéticos são para teste, desenvolvimento, demonstração. NÃO usar em manuscritos/publicações (usar dados reais pós-CEP)

---

## 🎯 Schema do catalog

```yaml
version: 1
datasets:
  P01_diarios_sinteticos:
    path: dados_sinteticos/P01_diarios_sinteticos.csv
    projeto: P01
    tipo: csv
    n_rows: 255
    seed: 42
    anonimizado: true
    responsible: "[seu-email]@ufrn.br"
```

---

## 🔗 Comandos

```bash
# CLI
python3 -m neurociencia_edu catalog list
python3 -m neurociencia_edu catalog show P01_diarios_sinteticos
python3 -m neurociencia_edu validate P01_diarios_sinteticos
```

---

**Última atualização:** 2026-09-19
