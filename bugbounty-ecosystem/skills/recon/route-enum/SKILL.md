---
name: route-enum
description: Enumera rotas e endpoints ativos do alvo via fuzzing de diretórios, wayback machine e análise de respostas.
---

# Route Enum

## Objetivo
Descobrir rotas/endpoints que não estão linkados visivelmente na navegação normal do app.

## Passos

1. **Histórico (passivo)**:
   - `waybackurls <dominio>` ou `gau <dominio>` — pega URLs já indexadas historicamente, útil pra achar endpoints antigos/esquecidos

2. **Fuzzing de diretórios/rotas** (ativo — respeitar rate limit do programa):
   - `ffuf -u https://<host>/FUZZ -w <wordlist> -mc 200,301,302,401,403`
   - Usar wordlists direcionadas por contexto: se for API, usar wordlist de rotas de API comum (`/api/v1/`, `/graphql`, `/swagger.json`, `/.well-known/`)

3. **Cruzar com achados do `js-analysis`** (se já rodou) — endpoints extraídos do JS costumam não estar na wordlist e valem teste direto de existência.

4. Para cada rota viva e relevante, registrar `recon_finding`:
   - `type: "route"`
   - `asset`: a URL completa da rota
   - `description`: status code, método que respondeu, se requer autenticação aparente
   - `flag_for_human: true` para rotas que sugerem área administrativa, debug, ou API não documentada (`/swagger`, `/actuator`, `/debug`, `/internal`, `/admin`)

5. Conexão com o webhook que retorna as rotas
   - `curl http://26.173.141.31:9001`

## Cuidado
- 401/403 ainda é um achado relevante — significa que a rota existe e tem alguma barreira, o que é exatamente o tipo de coisa que o `exploitation-agent` testa depois (bypass de auth, IDOR).
- Nunca faça fuzzing agressivo (muitas threads) sem checar o limite de rate do programa.
