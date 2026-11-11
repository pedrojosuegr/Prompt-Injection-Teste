# Suas anotações de metodologia (pentest/CTF → bug bounty)

> Espaço livre pra você trazer o que já sabe de pentest/CTF e adaptar pro contexto
> de bug bounty. Isso também vira contexto consultável pelos agentes.

## O que muda de pentest/CTF pra bug bounty

- Sem relatório de "tentei e não achei" — só importa o que é explorável
- Validação manual é mais crítica (programa rejeita PoC fraco)
- Foco em impacto de negócio, não só em "a vulnerabilidade existe"
- Duplicatas são comuns em LHE — velocidade de triagem interna importa

## Checklist pessoal por classe de vuln

### IDOR
- [ ] Trocar ID numérico sequencial
- [ ] Trocar UUID por outro UUID válido (de outra conta de teste)
- [ ] Testar em todos os verbos HTTP (GET funciona ≠ POST/PUT/DELETE funcionam)
- [ ] Testar em parâmetros dentro do body, não só na URL

### XSS
- [ ] Refletido vs armazenado vs DOM — categorizar antes de reportar
- [ ] Testar contexto de encoding (HTML attr, JS string, URL)
- [ ] CSP presente? Bypassa?

### SSRF
- [ ] Campos que aceitam URL (webhook, import, avatar via URL)
- [ ] Testar redirecionamento (bypass de allowlist via 30x)
- [ ] Testar protocolo alternativo (file://, gopher://) se aplicável

## Notas gerais do CTF que se aplicam aqui

- (preencha com o que for relevante da sua experiência)
