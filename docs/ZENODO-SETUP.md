# 🆔 Configurar DOI Zenodo

> **Zenodo** atribui DOIs automaticamente para cada release do GitHub.
> **Setup:** 5 minutos, 1 click.

---

## 🎯 Por que Zenodo?

- ✅ DOI permanente (citable)
- ✅ Arquivamento longo prazo (CERN)
- ✅ Integração automática com GitHub
- ✅ Versões: cada tag vira um novo DOI
- ✅ Metadados ricos (autores, ORCID, etc.)

## 🔧 Setup (uma vez)

### Passo 1: Conectar GitHub ↔ Zenodo

```
1. Vá para https://zenodo.org/
2. Login (use sua conta GitHub)
3. Vá para https://zenodo.org/account/settings/github/
4. Procure "dronreef2/NeurocienciaEducacional" na lista
5. Toggle ON ✅ (autoriza Zenodo a arquivar)
6. Pronto! Cada release vira um DOI automaticamente.
```

### Passo 2: Configurar metadados (opcional)

Já criamos `.zenodo.json` na raiz do repo. Ele define:
- Autores
- Afiliação
- ORCID
- Palavras-chave
- Licença
- Comunidades

**Edite `.zenodo.json`** com seus dados reais (especialmente ORCID e afiliação).

### Passo 3: Adicionar seu ORCID

1. Crie conta em https://orcid.org/ (se não tem)
2. Adicione seu ORCID no `.zenodo.json`:
   ```json
   {
     "creators": [
       {
         "name": "Seu Nome",
         "affiliation": "UFRN",
         "orcid": "0000-0000-0000-0000"
       }
     ]
   }
   ```

### Passo 4: Criar a primeira release

```bash
# Localmente
git tag v1.0.0
git push --tags

# Ou via GitHub
# Vá em Releases → "Create a new release" → tag: v1.0.0
```

**Workflow automático:**
1. GitHub Action trigga
2. Cria a release
3. Zenodo detecta
4. Arquiva o repositório
5. Atribui DOI
6. Adiciona o DOI na release do GitHub

### Passo 5: Encontrar o DOI

Acesse sua release no GitHub:
```
https://github.com/dronreef2/NeurocienciaEducacional/releases/tag/v1.0.0
```

O badge "DOI: 10.5281/zenodo.XXXXXXX" vai aparecer (gerado automaticamente).

Ou direto no Zenodo:
```
https://zenodo.org/record/XXXXXXX
```

## 📚 Como citar Zenodo

### BibTeX
```bibtex
@software{neurociencia_edu_2026_v1,
  author = {{Programa de Pesquisa em Neurociência Educacional} and Naschold, Angela Maria Chuvas},
  title = {Programa de Pesquisa em Neurociência Educacional (v1.0.0)},
  version = {1.0.0},
  year = {2026},
  url = {https://github.com/dronreef2/NeurocienciaEducacional},
  doi = {10.5281/zenodo.XXXXXXX}
}
```

### APA
```
Programa de Pesquisa em Neurociência Educacional. (2026).
Programa de Pesquisa em Neurociência Educacional (Version 1.0.0) [Computer software].
https://doi.org/10.5281/zenodo.XXXXXXX
```

## 🆘 Troubleshooting

### ❌ Zenodo não está arquivando
- Verifique se toggle está ON em https://zenodo.org/account/settings/github/
- Tente criar uma nova release (force refresh)

### ❌ DOI não aparece na release
- Pode levar até 1 hora
- Verifique Zenodo dashboard
- Force-push a tag: `git push --tags --force`

### ❌ Quer adicionar ORCID
- Vá em https://orcid.org/signin
- Conecte com Zenodo

## 📚 Referências

- [Zenodo GitHub Integration](https://docs.zenodo.org/#github)
- [ORCID](https://orcid.org/)
- [DOI System](https://www.doi.org/)

---

**Última atualização:** 2026-07-31
