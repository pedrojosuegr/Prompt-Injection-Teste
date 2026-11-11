---
name: js-analysis
description: Baixa arquivos JavaScript do alvo e extrai endpoints, parâmetros, chaves/segredos expostos e indícios de funcionalidades internas.
---

# JS Analysis

## Objetivo
Extrair de arquivos JS do alvo informações que não aparecem navegando normalmente: endpoints de API não documentados, nomes de parâmetros, chaves/tokens vazados, rotas internas/admin referenciadas no código.

## Passos

1. Coletar URLs de arquivos `.js` servidos pelo alvo (via crawling leve ou `httpx` + grep no HTML por `<script src=`).
2. Baixar cada arquivo JS para análise local (`curl` ou `wget`, respeitando rate limit).
3. Rodar extração de padrões:
   - Endpoints: regex por `["'](\/api\/[a-zA-Z0-9_\-\/{}]+)["']` e variações
   - Segredos: regex por padrões comuns de API keys (`AKIA[0-9A-Z]{16}`, `sk_live_`, `Bearer [A-Za-z0-9\-_]+\.`, etc) — ferramentas como `trufflehog filesystem <dir>` ajudam bastante aqui
   - Se o JS for minificado, usar um beautifier antes (`js-beautify`) pra facilitar leitura humana depois

4. Para cada endpoint/segredo relevante encontrado, registrar `recon_finding`:
   - `type: "js_endpoint"` ou `"js_secret"`
   - `asset`: o endpoint extraído ou a URL do arquivo JS onde o segredo foi achado
   - `evidence`: a linha exata do JS (trecho, não o arquivo inteiro)
   - **Segredos têm prioridade alta**: `flag_for_human: true` sempre, `confidence: high` se o padrão bate claramente com uma chave real

## Cuidado
- JS de bibliotecas de terceiros (React, jQuery, analytics) gera muito ruído — filtre por arquivos que parecem ser do bundle próprio do app (geralmente nomeados `main.*.js`, `app.*.js`, ou no path `/static/js/` próprio do domínio).
- Nunca teste um segredo encontrado (ex: tentar autenticar com uma API key) sem antes avisar o humano — isso já cruza pra exploitation.
