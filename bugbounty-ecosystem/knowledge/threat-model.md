# Threat Model — [NOME DO ALVO]

> Preencha isso ANTES do dia do evento, com base em informação pública.
> Cada hipótese tem um ID (TM-XXX) que os findings de recon/exploitation podem referenciar.

## 1. Perfil do alvo

- **Tipo de negócio:** (ex: fintech, e-commerce, SaaS B2B, marketplace...)
- **Dado sensível que manipula:** (ex: dados financeiros, PII, credenciais, dados de saúde...)
- **Stack conhecida:** (via Wappalyzer/BuiltWith/headers — preencher o que souber)
- **Arquitetura aparente:** (monolito, microserviços, SPA + API, mobile-first...)
- **Multi-tenant?** (se sim, isolamento entre contas/organizações é prioridade alta)

## 2. Histórico do programa

- **Reports públicos já disclosed (Hacktivity/Hackerone/Bugcrowd):**
  - [ ] Liste classes de vuln já aceitas nesse programa — indica o que os triadores validam fácil
- **Reputação/notas do programa:** (paga bem por qual severidade, tempo de resposta, etc)

## 3. Hipóteses priorizadas

Formato: ID | Hipótese | Justificativa | Prioridade (alta/média/baixa)

| ID | Hipótese | Justificativa | Prioridade |
|---|---|---|---|
| TM-001 | IDOR em endpoints de faturas/transações | Fintech, manipula recursos financeiros por ID | alta |
| TM-002 | SSRF em funcionalidade de webhook/import de URL | Se houver campo "callback URL" ou similar | média |
| TM-003 | Broken access control entre tenants | Sistema multi-tenant confirmado | alta |
| TM-004 | ... | ... | ... |

## 4. Superfícies de maior interesse (a validar no recon)

- [ ] Painel admin / área interna exposta
- [ ] API versionada antiga ainda acessível (v1 enquanto o app usa v2)
- [ ] Funcionalidade de upload de arquivo
- [ ] Integração com serviços terceiros (pagamento, storage, email)
- [ ] Subdomínios de staging/dev esquecidos

## 5. Fora de escopo / cuidado redobrado

- Liste aqui o que as regras do programa proíbem explicitamente (ver `program-rules.md`)
- Qualquer ação destrutiva, mesmo que o escopo permita o alvo
