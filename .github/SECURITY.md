# 🔒 Política de Segurança

> **Versão:** 1.0
> **Última atualização:** 2026-07-30

## 🛡️ Versões suportadas

| Versão | Suporte | Status |
|---|---|---|
| 1.0.x (atual) | ✅ | Ativa |
| 0.x (legacy) | ❌ | EOL |

## 🚨 Reportar uma vulnerabilidade

Se você descobriu uma vulnerabilidade de segurança **NÃO** abra uma issue pública.

**Em vez disso, entre em contato diretamente:**
- **Email:** angela.naschold@ufrn.br
- **Assunto:** `[SECURITY] Programa de Pesquisa — <descrição breve>`

Você receberá uma resposta em até **72 horas** com:
- Confirmação do recebimento
- Plano de investigação
- Timeline para correção (se aplicável)

## 🔐 Boas práticas de segurança neste projeto

### Para contribuidores

1. **NUNCA** commite chaves SSH, API keys, tokens ou senhas
2. Use `.gitignore` para excluir arquivos sensíveis (já configurado)
3. Dados de pesquisa (`.csv`, `.set`, `.bdf`, etc.) **não** devem ser versionados
4. Use **IDs anônimos** (C01, C02, ...) ao invés de nomes
5. Em caso de dúvida, consulte a [LGPD](https://www.gov.br/cidadnia/pt-br/acesso-a-informacao/lgpd)

### Para usuários da plataforma

- Documentação completa em `docs/POLITICA-DADOS.md`
- Dados sensíveis ficam em `dados/` (gitignored)
- Veja `docs/POLITICA-AUTORIA.md` para co-autoria

## 🛠️ Ferramentas automatizadas

Este projeto usa:
- **GitHub Secret Scanning** (bloqueia push de secrets conhecidos)
- **GitHub Dependabot** (atualiza dependências com vulnerabilidades)
- **detect-secrets** (pre-commit hook)
- **detect-private-key** (pre-commit hook)

## 📋 Histórico de vulnerabilidades

*Nenhuma vulnerabilidade reportada até o momento.*

---

**Mantenedor:** Equipe do Programa de Pesquisa
**Contato:** angela.naschold@ufrn.br
