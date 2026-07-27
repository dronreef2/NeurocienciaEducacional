# 🔒 Política de Dados do Programa de Pesquisa

> **Versão:** v0.1 (2026-07-26)
> **Aplica-se a:** todos os 5 projetos do programa.
> **Aprovação necessária:** Comitê de Ética (CEP/UFRN) + orientadora.

---

## 1. Princípios

1. **Privacidade por padrão** — coletar só o necessário.
2. **Anonimização como regra** — identificadores removidos na análise.
3. **Consentimento explícito** — TCLE + TALE sempre que envolver participantes.
4. **Segurança física e digital** — armazenamento em locais controlados.
5. **Transparência** — dados podem ser compartilhados (com restrições) com a comunidade científica.
6. **Conformidade legal** — LGPD (Lei 13.709/2018) + Resoluções CNS 466/2012 e 510/2016.

---

## 2. Classificação dos dados

### 🟢 Dados públicos (podem ser compartilhados)
- Papers publicados (texto)
- Materiais didáticos desenvolvidos (com licença CC BY 4.0)
- Códigos de análise (R, Python) — sob licença MIT
- README do projeto (texto)

### 🟡 Dados restritos (uso interno da equipe)
- Dados brutos anonimizados (`.csv`, `.xlsx`) — só equipe do projeto
- Transcrições de entrevistas (anonimizadas) — só equipe
- Questionários preenchidos (anonimizados) — só equipe
- Áudios (anonimizados) — só equipe

### 🔴 Dados sensíveis (acesso máximo restrito)
- TCLEs assinados (com nome, RG, contato) — **apenas pesquisadora principal + orientadora**
- TALEs assinados
- Vídeos com imagem de crianças
- Qualquer dado com identificação pessoal (PII)

---

## 3. Onde armazenar

| Tipo de dado | Local | Backup |
|---|---|---|
| 🔴 Sensíveis (TCLEs, etc.) | HD externo criptografado (BitLocker) na residência da pesquisadora | Backup mensal em HD separado, mesmo local |
| 🟡 Restritos (dados anonimizados) | Google Drive UFRN institucional (compartilhado só com equipe) | Versionamento automático do Google |
| 🟡 Códigos de análise | GitHub (repositório do programa, pasta `analise/`) | GitHub |
| 🟢 Públicos | GitHub (pastas visíveis) + Zenodo (DOI para papers) | GitHub + Zenodo |

**ATENÇÃO:** o `.gitignore` do projeto **bloqueia** qualquer arquivo com dados (`.csv`, `.xlsx`, `.set`, `.edf`, etc.). Isso garante que **nenhum dado** vai pro GitHub por acidente.

---

## 4. Procedimentos obrigatórios

### Antes da coleta
- [ ] Aprovação do CEP vigente
- [ ] TCLE assinado pelos pais/responsáveis
- [ ] TALE assinado pela criança
- [ ] Carta de anuência da escola
- [ ] HD externo criptografado disponível
- [ ] Backup do HD externo verificado

### Durante a coleta
- [ ] Identificação da criança por **código** (C01, C02...) — NUNCA pelo nome
- [ ] Áudios/vídeos salvos no HD criptografado, não na nuvem
- [ ] Caderno de campo sem PII
- [ ] Nenhuma foto publicada sem autorização específica (separada do TCLE)

### Após a coleta
- [ ] Transcrição: substituir nomes reais por nomes fictícios
- [ ] Questionários: digitalizar, anonimizar, deletar papel original (após 5 anos)
- [ ] TCLEs: arquivo separado, **nunca** em pasta de análise
- [ ] Backup duplo: HD externo + Google Drive UFRN

### Antes da publicação
- [ ] Confirmar anonimização (busca por nomes próprios)
- [ ] Confirmar que todos os coautores revisaram
- [ ] Confirmar conformidade com a LGPD
- [ ] Verificar conformidade com as restrições do CEP
- [ ] Depósito de dados brutos no **Zenodo** (com DOI, acesso restrito se necessário)

---

## 5. Compartilhamento de dados com outros pesquisadores

- **Padrão:** dados anonimizados podem ser compartilhados com outros pesquisadores mediante:
  1. Solicitação formal (e-mail) com justificativa
  2. Aprovação da pesquisadora principal + orientadora
  3. Assinatura de termo de uso de dados (a criar)
  4. Prazo de uso definido
- **Exceção:** dados do P05 (coorte) podem ter restrições específicas definidas no TCLE.

---

## 6. Direitos dos participantes (LGPD)

- **Acesso:** o participante pode pedir acesso aos seus dados a qualquer momento.
- **Correção:** dados incorretos podem ser corrigidos.
- **Exclusão:** o participante pode pedir exclusão dos seus dados **antes da publicação**. Depois de publicado, a exclusão pode não ser possível (anonimização reversa).
- **Portabilidade:** dados podem ser fornecidos em formato aberto (CSV).
- **Revogação do consentimento:** a qualquer momento, sem prejuízo.

**Procedimento:** o pedido deve ser feito por escrito à pesquisadora principal (e-mail). Resposta em até 30 dias.

---

## 7. Plano de descarte (5 anos)

- **5 anos após o fim do projeto:** destruir todos os dados digitais (criptografia → deleção) e físicos (trituradora de papel).
- **Papers publicados:** mantidos indefinidamente (parte do registro científico).
- **Códigos:** mantidos no GitHub indefinidamente (sob licença MIT).
- **Materiais didáticos:** mantidos no GitHub sob CC BY 4.0.

---

## 8. Incidentes de segurança

Em caso de **vazamento, perda ou acesso não autorizado**:
1. Comunicar à pesquisadora principal em até 24h
2. Comunicar à orientadora
3. Avaliar se é necessário notificar o CEP
4. Avaliar se é necessário notificar a ANPD (Autoridade Nacional de Proteção de Dados) — casos graves
5. Notificar participantes afetados (se for o caso)
6. Documentar o incidente em `docs/incidentes/[AAAA-MM-DD]-incidente.md`

---

## 9. Revisões desta política

- **v0.1** (2026-07-26): versão inicial
- **Próxima revisão:** 2026-12 (após aprovação do CEP do P01)

---

> **Aprovada por:** [orientadora — a ser assinado após aprovação]
> **Data de vigência:** [a definir]
