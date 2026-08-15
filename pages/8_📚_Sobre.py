"""Página 8: Sobre o programa."""
import streamlit as st

st.set_page_config(page_title="Sobre", page_icon="📚", layout="wide")

st.markdown("# 📚 Sobre o Programa")
st.markdown("---")

st.markdown("""
## Programa de Pesquisa em Neurociência Educacional (UFRN/CERES/PPGED)

5 projetos · 2026-2030 · Orientadora Profa. Dra. Ângela M. C. Naschold
""")

st.markdown("""
## 👤 Equipe

| Papel | Pessoa |
|---|---|
| Orientadora | Profa. Dra. Ângela M. C. Naschold (PPGED/UFRN) |
| Pesquisador | [seu nome] (mestrando PPGED) |

## 🎓 Instituições

- **Universidade Federal do Rio Grande do Norte (UFRN)**
  - Centro de Ensino Superior do Seridó (CERES)
  - Programa de Pós-Graduação em Educação (PPGED)

## 🎯 Objetivos

1. **Investigar** como crianças do 2º ao 5º ano do Ensino Fundamental
   desenvolvem cognição de teoria da mente ao usar IA generativa com mediação

2. **Testar** efeitos de gamificação nas funções executivas (P02)

3. **Mapear** diferenças neurofisiológicas na leitura em tela vs papel (P03)

4. **Modelar** mecanismos entre uso de IA e funções executivas (P04)

5. **Acompanhar** desenvolvimento longitudinal das FE (P05)

## 📊 Marcos

- [x] **5 protocolos detalhados** (P01-P05)
- [x] **5 pré-registros OSF**
- [x] **5 manuscritos iniciais** (rascunhos)
- [x] **Piloto P01** (3 crianças, 17 dias)
- [x] **Dados sintéticos** (P01-P05)
- [x] **13 notebooks** analíticos
- [x] **20+ figuras** (300 dpi)
- [x] **Dashboard** Streamlit
- [x] **8 P01 instrumentos** (TCLE, TALE, etc.)
- [x] **Pipeline de análises** (R + Python)
- [ ] Submissão P01 (Computers & Education)
- [ ] Aprovação comitê de ética
- [ ] Coletas de campo (P02-P05)

## 📚 Referências principais

- Creswell, J. W. (2014). *Research Design: Qualitative, Quantitative, and Mixed Methods Approaches*
- Braun, V., & Clarke, V. (2019). *Thematic Analysis: A Practical Guide*
- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences*
- Kline, R. B. (2015). *Principles and Practice of Structural Equation Modeling*
- Preacher, K. J. (2015). *Advances in Mediation Analysis*
- Duncan, T. E., & Duncan, S. C. (2009). *Latent Growth Curve Modeling*

## 📧 Contato

- **Repositório**: [github.com/dronreef2/NeurocienciaEducacional](https://github.com/dronreef2/NeurocienciaEducacional)
- **Issues**: [github.com/dronreef2/NeurocienciaEducacional/issues](https://github.com/dronreef2/NeurocienciaEducacional/issues)
- **Email**: [instituição]

## 📜 Licença

- **Código**: MIT
- **Dados**: CC-BY-4.0
- **Manuscritos**: Direitos dos respectivos periódicos
- **LGPD Compliance**: Todos os dados anonimizados, com consentimento (TCLE/TALE)

## 🚀 Como contribuir

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/nova-analise`)
3. Commit suas mudanças (`git commit -m 'feat: nova análise'`)
4. Push para a branch (`git push origin feature/nova-analise`)
5. Abra um Pull Request

## 🙏 Agradecimentos

- Profa. Dra. Ângela M. C. Naschold (orientação)
- PPGED/UFRN (programa de pós-graduação)
- CERES/UFRN (apoio institucional)
- Escolas parceiras (campo de pesquisa)
- Todos que contribuíam para o programa

---

<div style="text-align: center; color: #888; padding: 20px;">
    Programa de Pesquisa em Neurociência Educacional · 2026-2030<br>
    UFRN · CERES · PPGED
</div>
""", unsafe_allow_html=True)
