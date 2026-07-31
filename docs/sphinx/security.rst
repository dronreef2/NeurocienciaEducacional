=========
Segurança
=========

Reportar vulnerabilidades
==========================

**NÃO** abra issue pública.

Entre em contato diretamente:
**angela.naschold@ufrn.br**

Assunto: ``[SECURITY] <descrição>``

Resposta em até 72 horas.

Boas práticas
=============

- **NUNCA** commitar chaves SSH, API keys, tokens
- Dados de pesquisa **NÃO** devem ser versionados
- Use IDs anônimos (C01, C02, ...) ao invés de nomes
- Respeite a LGPD_

.. _LGPD: https://www.gov.br/cidadania/pt-br/acesso-a-informacao/lgpd

Ferramentas automatizadas
=========================

- GitHub Secret Scanning
- GitHub Dependabot
- ``detect-secrets`` (pre-commit)
- ``detect-private-key`` (pre-commit)
