# 🌐 Configuração do GitHub Pages — Passo a Passo

> **Objetivo:** Publicar a documentação Sphinx do programa em
> `https://<seu-usuario>.github.io/NeurocienciaEducacional/`

---

## 📋 TL;DR (3 passos)

1. **GitHub:** Settings → Pages → Source: **GitHub Actions** (mudar!)
2. **Aguardar:** primeiro push em `main` triggera o workflow automaticamente
3. **Acessar:** `https://dronreef2.github.io/NeurocienciaEducacional/`

---

## 🔧 Passo a passo detalhado

### Passo 1: Acessar Settings

```
1. Vá para https://github.com/dronreef2/NeurocienciaEducacional
2. Clique em "Settings" (engrenagem, no topo, à direita)
3. No menu lateral esquerdo, clique em "Pages"
```

### Passo 2: Mudar o Source

Você está vendo isso:
> *Build and deployment → Source → Branch → "Your GitHub Pages site is currently being built from the main branch."*

**Mude para "GitHub Actions":**

```
1. Em "Source", clique no dropdown (atualmente "Deploy from a branch")
2. Selecione "GitHub Actions"
3. Confirme (não precisa salvar — é automático)
```

**Por quê?** O GitHub Actions permite que o nosso workflow `pages.yml`:
- Instale Python + R
- Rode `sphinx-apidoc` para gerar docs Python
- Rode `roxygen2::roxygenise()` para gerar docs R
- Compile tudo com `sphinx-build`
- Faça o deploy

Se ficar em "Branch", ele só publica o conteúdo do `main` (que é o README, sem formatação).

### Passo 3: Verificar permissões do workflow

O workflow já está configurado com as permissões corretas:

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

Mas em alguns casos, você precisa **autorizar Actions a escrever em Pages**:

```
1. Settings → Actions → General
2. Role de "Workflow permissions": "Read and write permissions"
3. ✅ "Allow GitHub Actions to create and approve pull requests"
4. Salvar
```

### Passo 4: Acionar o workflow

**Automático:** o workflow trigga em push para `main` quando você modifica:
- `docs/**`
- `analise/R/R/**`
- `analise/Python/neurociencia_edu/**`

**Manual (primeira vez):**

```
1. Vá para a aba "Actions"
2. No menu lateral, clique em "Build and Deploy GitHub Pages"
3. Clique em "Run workflow" → branch: main → "Run workflow"
```

### Passo 5: Acompanhar

```
1. Actions → workflow em execução
2. Aguarde ~3-5 minutos (build do Sphinx leva tempo)
3. Se tudo der certo, ✅ verde
4. Se der erro ❌, clique para ver os logs
```

### Passo 6: Acessar o site

Depois de deploy bem-sucedido:

🌐 **https://dronreef2.github.io/NeurocienciaEducacional/**

---

## 🎨 Customização

### Domínio customizado (opcional)

```
1. Settings → Pages → Custom domain
2. Digite: docs.neurociencia.edu (ou outro)
3. Configure DNS:
   - CNAME: dronreef2.github.io
4. ✅ "Enforce HTTPS"
```

### Tema

O tema já está configurado como **Read the Docs** (`sphinx_rtd_theme`) no
`docs/sphinx/conf.py`. Para mudar:

```python
html_theme = 'furo'  # Alternativa moderna
# ou
html_theme = 'sphinx_book_theme'  # Alternativa Jupyter Book
```

Reinstale as deps e rebuilde.

---

## 🔍 Troubleshooting

### ❌ Erro "Pages deployment failed"

**Causa mais comum:** permissões.

**Solução:**
1. Settings → Actions → General → Workflow permissions → "Read and write"
2. Settings → Pages → Source → "GitHub Actions"

### ❌ 404 ao acessar a URL

**Causa:** deploy ainda não completou ou URL errada.

**Solução:**
- URL correta: `https://<username>.github.io/<repo>/`
- Verifique: Settings → Pages → "Your site is live at..."

### ❌ Site sem CSS (parece "cru")

**Causa:** `.nojekyll` faltando.

**Solução:** Já adicionado no workflow. Se persistir:
1. Adicione manualmente em `docs/sphinx/_static/.nojekyll`
2. Re-trigger o workflow

### ❌ Erro no Sphinx (build falha)

**Causa:** sintaxe `.rst` quebrada.

**Solução:**
1. Vá em Actions → clique no workflow
2. Veja os logs (especialmente "Build Python docs (Sphinx)")
3. Corrija o erro no arquivo `.rst` correspondente
4. Push novamente

### ❌ "fatal: not a git repository"

**Causa:** workflow rodando em ambiente errado.

**Solução:** Raro, mas pode acontecer se você modificou o `actions/checkout`.

---

## 📊 O que o workflow faz

```yaml
1. Checkout do código
2. Setup Python 3.11
3. Setup R 4.4.1
4. Instala deps: sphinx, sphinx-rtd-theme, myst-parser
5. Instala deps R: tidyverse, lavaan, devtools, roxygen2
6. Gera docs R: roxygen2::roxygenise()
7. Gera docs Python: sphinx-apidoc
8. Builda HTML: sphinx-build
9. Adiciona .nojekyll (CRÍTICO)
10. Setup Pages
11. Upload artifact
12. Deploy via actions/deploy-pages@v4
```

---

## 🎯 Verificação final

Depois de tudo configurado, sua URL deve mostrar:

- ✅ Home page com cards de projetos
- ✅ Sidebar com navegação
- ✅ Tabelas com formatação
- ✅ Imagens renderizadas
- ✅ Search box funcional

Se você ver tudo isso: **parabéns, está no ar!** 🎉

---

## 📞 Ajuda adicional

- **Docs oficiais:** https://docs.github.com/en/pages
- **Sphinx tutorial:** https://www.sphinx-doc.org/en/master/tutorial/
- **Read the Docs theme:** https://sphinx-rtd-theme.readthedocs.io/
- **Issues do repo:** https://github.com/dronreef2/NeurocienciaEducacional/issues

---

**Última atualização:** 2026-07-31
