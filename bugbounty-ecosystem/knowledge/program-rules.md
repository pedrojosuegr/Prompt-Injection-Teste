# Regras do Programa — [NOME DO LHE]

> Copie/cole literalmente as regras do programa aqui. Isso é consultado por TODOS os agentes
> antes de qualquer ação. Em caso de dúvida, o agente deve parar e perguntar a você — nunca assumir.

## Escopo (domínios/apps permitidos)

```
*.exemplo.com
app.exemplo.com
api.exemplo.com
```

## Fora de escopo (explícito)

```
blog.exemplo.com (CMS terceiro)
status.exemplo.com
```

## Regras de rate limit / comportamento

- Máximo de requests simultâneos: [preencher]
- Proibido: testes automatizados de força bruta não anunciados? [preencher]
- Proibido: DoS, teste de volumetria
- Proibido: engenharia social, phishing contra funcionários
- Dados de outros usuários: nunca exfiltrar em volume, 1 registro de PoC é suficiente

## Classes de vulnerabilidade aceitas / não aceitas

- Aceitas: [preencher conforme a policy]
- Não aceitas (out of scope por política, não por técnica): ex. clickjacking sem impacto, self-XSS, etc.

## Severidade / triagem esperada

- Tabela de recompensa por severidade, se pública
- SLA de resposta do programa

## Contato / disclosure

- Canal oficial pra reportar
- Regras de disclosure pública (prazo, se permitido)
