---
name: subdomain-enum
description: Enumera subdomínios do alvo usando fontes passivas e ativas, e identifica quais estão vivos.
---

# Subdomain Enum

## Objetivo
Mapear a maior superfície possível de subdomínios do alvo, respeitando o escopo de `knowledge/program-rules.md`, e identificar quais estão ativos.

## Passos

1. **Enumeração passiva** (não toca o alvo diretamente):
   - `subfinder -d <dominio> -all -silent` (se instalado)
   - crt.sh: `curl -s "https://crt.sh/?q=%25.<dominio>&output=json"` e extrair `name_value`
   - Se `amass` estiver disponível: `amass enum -passive -d <dominio>`

2. **Consolidar e deduplicar** a lista de subdomínios encontrados.

3. **Verificar quais estão vivos** (isso já é ativo, considerar rate limit):
   - `httpx -l subdominios.txt -silent -status-code -title -tech-detect`

4. **Para cada subdomínio vivo**, registrar um `recon_finding` com:
   - `type: "subdomain"`
   - `asset`: o subdomínio completo (ex: `https://staging.exemplo.com`)
   - `description`: status code, título da página, tecnologia detectada
   - `confidence`: "high" se confirmado vivo, "medium" se só na lista passiva
   - `flag_for_human: true` se o subdomínio parecer sensível (staging, dev, admin, api interna, vpn, jenkins, gitlab, etc) — esses geralmente são os achados mais valiosos

## Gravando no banco

```python
import sqlite3, json, uuid
from datetime import datetime, timezone

conn = sqlite3.connect("data/recon.db")
conn.execute("""
    INSERT INTO recon_findings (id, source_agent, type, asset, description, evidence,
                                  confidence, related_to_threat_model, flag_for_human, tags, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    str(uuid.uuid4()), "subdomain-enum", "subdomain", "https://staging.exemplo.com",
    "Subdomínio de staging vivo, status 200, título 'Login - Internal'",
    "httpx output: staging.exemplo.com [200] [Login - Internal] [nginx]",
    "high", json.dumps(["TM-004"]), 1, json.dumps(["staging", "interessante"]),
    datetime.now(timezone.utc).isoformat()
))
conn.commit()
conn.close()
```

## Cuidado
- Nunca inclua no escopo de teste um subdomínio listado como "fora de escopo" em `program-rules.md`, mesmo que apareça na enumeração passiva.
