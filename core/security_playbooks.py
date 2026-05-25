CYBER_PLAYBOOKS = {
    "web_app_breach": {
        "name": "analyzing-web-application-breach",
        "domain": "Web Application Security",
        "framework_mappings": {"mitre_attack": "T1190", "nist_csf": "DE.CM", "mitre_d3fend": "D3-NTA"},
        "prerequisites": ["Web server raw logs accessibility", "Target app visibility"],
        "workflow": [
            "1. Run log analysis to isolate status anomalies (HTTP 500/403).",
            "2. Scan user-agent tags for exploitation tool fingerprints.",
            "3. Audit request layers for structural payload anomalies."
        ],
        "verification": "Ensure patches effectively counter simulated injection attempts."
    }
}

def scan_applicable_playbook(user_query: str) -> dict:
    lowered = user_query.lower()
    if any(x in lowered for x in ["web", "sql", "xss", "website", "breach"]):
        return CYBER_PLAYBOOKS["web_app_breach"]
    return None
