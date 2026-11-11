#!/usr/bin/env python3
"""
Inicializa data/recon.db e data/findings.db a partir dos schemas em schemas/.
Rode uma vez no início do engajamento: python3 scripts/init_db.py
"""
import sqlite3
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, "data")

RECON_DB = os.path.join(DATA_DIR, "recon.db")
FINDINGS_DB = os.path.join(DATA_DIR, "findings.db")

RECON_SCHEMA = """
CREATE TABLE IF NOT EXISTS recon_findings (
    id TEXT PRIMARY KEY,
    source_agent TEXT NOT NULL,
    type TEXT NOT NULL,
    asset TEXT NOT NULL,
    description TEXT NOT NULL,
    evidence TEXT,
    confidence TEXT NOT NULL,
    related_to_threat_model TEXT,  -- JSON array serializado como string
    flag_for_human INTEGER NOT NULL DEFAULT 0,
    tags TEXT,                     -- JSON array serializado como string
    timestamp TEXT NOT NULL
);

-- full-text search sobre description/evidence, pra busca tipo RAG simples
CREATE VIRTUAL TABLE IF NOT EXISTS recon_findings_fts USING fts5(
    id UNINDEXED,
    asset,
    description,
    evidence,
    tags,
    content='recon_findings',
    content_rowid='rowid'
);

CREATE TRIGGER IF NOT EXISTS recon_findings_ai AFTER INSERT ON recon_findings BEGIN
    INSERT INTO recon_findings_fts(rowid, id, asset, description, evidence, tags)
    VALUES (new.rowid, new.id, new.asset, new.description, new.evidence, new.tags);
END;
"""

FINDINGS_SCHEMA = """
CREATE TABLE IF NOT EXISTS vuln_findings (
    id TEXT PRIMARY KEY,
    source_agent TEXT NOT NULL,
    vuln_class TEXT NOT NULL,
    asset TEXT NOT NULL,
    description TEXT NOT NULL,
    recon_finding_ids TEXT,     -- JSON array serializado como string
    payload_used TEXT,
    evidence TEXT,
    severity_estimate TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'needs_manual_validation',
    validation_notes TEXT,
    timestamp TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_vuln_status ON vuln_findings(status);
CREATE INDEX IF NOT EXISTS idx_vuln_class ON vuln_findings(vuln_class);
"""


def init_db(path, schema, label):
    conn = sqlite3.connect(path)
    conn.executescript(schema)
    conn.commit()
    conn.close()
    print(f"[ok] {label} -> {path}")


if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    init_db(RECON_DB, RECON_SCHEMA, "recon.db")
    init_db(FINDINGS_DB, FINDINGS_SCHEMA, "findings.db")
    print("\nPronto. Agentes podem gravar/ler via sqlite3 CLI ou Python.")
