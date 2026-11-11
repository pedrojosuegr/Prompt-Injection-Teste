# Fluxo do engajamento — LHE [NOME]

> Este é o "instructions.md" principal: o roteiro que você cola na conversa do Claude Code
> pra ele orquestrar os três subagentes na ordem certa. Os subagentes individuais
> (recon-agent, exploitation-agent, report-agent) já têm suas próprias regras em
> `.claude/agents/`; isso aqui é só a coreografia entre eles.

## Pré-requisitos (fazer ANTES do dia 14)

1. Preencher `knowledge/threat-model.md` com hipóteses reais do alvo
2. Preencher `knowledge/program-rules.md` com as regras literais do programa
3. Rodar `python3 scripts/init_db.py` pra garantir que os bancos existem
4. Testar as ferramentas de linha de comando que as skills de recon usam (subfinder, httpx, ffuf, waybackurls/gau, trufflehog) — instalar o que faltar

## Fluxo no dia do evento

### 1. Recon
```
Use o recon-agent para mapear [alvo], priorizando as hipóteses do threat model.
```
Acompanhe o resumo final dele. Preste atenção especial em tudo marcado `flag_for_human: true` — isso é o que vale sua atenção manual em paralelo, enquanto o exploitation-agent trabalha sobre o resto.

### 2. Exploitation
```
Use o exploitation-agent para testar os achados de recon, priorizando as hipóteses de alta prioridade do threat model.
```
Ele lê `data/recon.db` sozinho — não precisa copiar/colar nada. Ao final, ele te dá a lista de candidatos ordenados por severidade.

### 3. Validação manual (você, sempre)
Para cada finding em `data/findings.db` com `status = needs_manual_validation`:
- Reproduza manualmente o payload/request registrado
- Se confirmado: `UPDATE vuln_findings SET status = 'validated', validation_notes = '...' WHERE id = '...'`
- Se falso positivo: `UPDATE vuln_findings SET status = 'false_positive', validation_notes = '...' WHERE id = '...'`

Pode fazer isso direto via sqlite3 CLI:
```bash
sqlite3 data/findings.db "SELECT id, vuln_class, asset, severity_estimate FROM vuln_findings WHERE status = 'needs_manual_validation';"
```

### 4. Sua abordagem manual em paralelo
Enquanto os agentes trabalham, revise os achados de recon com `flag_for_human: true` que ainda não viraram finding de exploitation — isso é o que os bots podem ter deixado passar (lógica de negócio sutil, chained bugs, etc). É aqui que sua experiência de pentest/CTF entra mais forte.

### 5. Report
```
Use o report-agent para gerar os relatórios dos findings validados.
```
Ele só pega `status = validated` — revise cada markdown gerado em `reports/output/` antes de submeter ao programa.

## Loop contínuo durante o evento

Isso não é linear uma vez só — repita o ciclo recon → exploitation → validação conforme o engajamento avança (ex: depois de achar uma funcionalidade nova no feature-mapping, pode valer rodar recon de novo só naquela área, depois exploitation de novo).
