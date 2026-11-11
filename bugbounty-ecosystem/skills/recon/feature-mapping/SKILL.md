---
name: feature-mapping
description: Navega as funcionalidades do app (autenticadas e não-autenticadas) e descreve o que cada uma faz, para dar contexto de negócio aos agentes de exploitation.
---

# Feature Mapping

## Objetivo
Produzir um mapa legível de "o que o app faz" — não tecnicamente (isso é `route-enum`), mas funcionalmente: quais ações um usuário pode tomar, onde há transação de dado sensível, onde há relação entre usuários/contas.

## Passos

1. Se houver credenciais de teste fornecidas pelo programa, usar o app autenticado normalmente, navegando por cada seção principal.
2. Para cada funcionalidade relevante, anotar:
   - O que ela faz (ex: "edição de perfil", "upload de comprovante", "convite de membro para organização")
   - Se envolve manipulação de recurso por ID (candidato natural a IDOR)
   - Se envolve input que é refletido em algum lugar (candidato a XSS)
   - Se envolve o sistema buscando uma URL fornecida pelo usuário (candidato a SSRF)
3. Dar atenção especial a funcionalidades que tocam as hipóteses do `threat-model.md` — se o threat model aponta "multi-tenant" como prioridade alta, mapear tudo que envolve troca de contexto entre organizações/contas.

## Gravando

Registrar um `recon_finding` do tipo `"functionality"` por feature relevante, com `description` explicando o fluxo e `tags` indicando a classe de vuln candidata (ex: `["idor-candidate"]`, `["xss-candidate"]`, `["ssrf-candidate"]`) — isso é o que o `exploitation-agent` usa pra priorizar qual skill rodar em qual asset.

## Cuidado
- Esse mapeamento é o elo entre "o que existe" (route-enum) e "o que vale a pena atacar" (exploitation) — capriche na descrição funcional, não só técnica.
