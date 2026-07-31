# Snakemake Profiles

> **Snakemake profiles** permitem usar o mesmo Snakefile em diferentes ambientes
> (laptop, servidor, cluster) sem modificar o workflow.

## 📁 Perfis disponíveis

| Perfil | Ambiente | Uso |
|---|---|---|
| `local/` | Laptop/desktop | Default, paraleliza em cores locais |
| `slurm/` | Cluster SLURM | HPCs como Santos Dumont (LNCC), BORG (UFRN) |
| `sge/` | Cluster SGE | HPCs antigos |
| `cluster_generic/` | Cluster genérico | Customizável para qualquer scheduler |

## 🚀 Como usar

```bash
# Local (default)
snakemake --profile analise/Snakemake/profiles/local/

# SLURM
snakemake --profile analise/Snakemake/profiles/slurm/

# SGE
snakemake --profile analise/Snakemake/profiles/sge/

# Com profile customizado
snakemake --profile analise/Snakemake/profiles/cluster_generic/
```

## 📋 Estrutura de um profile

```
profiles/
├── local/
│   └── config.yaml       # Configurações do profile
└── slurm/
    ├── config.yaml
    └── status.py         # Script para checar status dos jobs
```

## 🔧 Configuração por profile

### `local/config.yaml`
```yaml
cores: 4                  # número de cores locais
resources:
  mem_mb: 8000           # memória por job
use-conda: true
rerun-triggers: mtime
```

### `slurm/config.yaml`
```yaml
executor: slurm
jobs: 100                 # max jobs simultâneos
resources:
  mem_mb: 8000
  time: "02:00:00"        # 2 horas
  partition: "default"
use-conda: true
```

## 📊 Comparação

| | Local | SLURM | SGE |
|---|---|---|---|
| Setup | Imediato | Precisa SSH no cluster | Idem |
| Paralelização | cores | jobs no cluster | jobs no cluster |
| Falha recovery | Auto | Re-submit | Re-submit |
| Para datasets grandes (>1 TB) | ❌ | ✅ | ✅ |

## 🏛️ Clusters UFRN suportados

### Santos Dumont (LNCC/MCTIC)
```yaml
# Em slurm/config.yaml
cluster:
  status: "sacct -j {jobid} --format=State --noheader"
  cancel: "scancel {jobid}"
  submit: "sbatch --mem={resources.mem_mb}M --time={resources.time} script.sh"
```

### BORG (UFRN — interna)
```yaml
# Similar ao SLURM
```

## 🛠️ Como criar novo profile

1. Copie um profile existente:
```bash
cp -r profiles/local profiles/meu_cluster
```

2. Edite `config.yaml`:
```yaml
executor: <seu_scheduler>
# outras configs
```

3. Se necessário, customize `submit/script.sh` e `status.py`

## 📚 Referências

- [Snakemake Profiles](https://snakemake.readthedocs.io/en/stable/executing/cli.html#profiles)
- [Snakemake SLURM](https://snakemake.readthedocs.io/en/stable/executing/slurm.html)
- [Snakemake Examples](https://github.com/snakemake/snakemake/tree/main/tests/test_profile)

---

**Última atualização:** 2026-07-31
