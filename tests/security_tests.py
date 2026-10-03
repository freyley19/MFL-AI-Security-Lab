# MFL Bank — AI Security Lab
# PROVE: Security regression tests
# Author: @freyley.leyva

import requests

API = "http://api:8000"

passed = 0
failed = 0


# =========================================================
# RESULTADOS
# =========================================================

def result(name, ok, detail=""):
    global passed, failed

    if ok:
        passed += 1
        print(f"[PASS] {name}")
    else:
        failed += 1
        print(f"[FAIL] {name}")

        if detail:
            print(f"       {detail}")


# =========================================================
# HELPERS
# =========================================================

def transfer(payload):
    response = requests.post(
        f"{API}/transfer",
        json=payload,
        timeout=30
    )

    response.raise_for_status()
    return response.json()


def ask(payload):
    response = requests.post(
        f"{API}/ask",
        json=payload,
        timeout=240
    )

    response.raise_for_status()
    return response.json()


def source_names(data):
    return [
        source["source"]
        for source in data.get("sources", [])
    ]


# =========================================================
# TEST 1 — BREAK / TOOL AUTHORIZATION
#
# En vulnerable mode Alex puede intentar operar
# desde la cuenta de Sam.
#
# PASS aquí significa:
# "la vulnerabilidad educativa está reproducida".
# =========================================================

def test_vulnerable_cross_account_transfer():

    data = transfer({
        "from_account": "MFL-002",
        "to_account": "MFL-001",
        "amount": 5000,
        "user_id": "MFL-001",
        "role": "customer",
        "secure_mode": False
    })

    ok = (
        data.get("decision") == "allow"
        and data.get("status") == "simulated"
    )

    result(
        "BREAK: vulnerable mode allows cross-account transfer",
        ok,
        f"response={data}"
    )


# =========================================================
# TEST 2 — DEFEND / TOOL AUTHORIZATION
#
# El mismo ataque debe ser bloqueado en Hardened.
# =========================================================

def test_hardened_cross_account_transfer():

    data = transfer({
        "from_account": "MFL-002",
        "to_account": "MFL-001",
        "amount": 5000,
        "user_id": "MFL-001",
        "role": "customer",
        "secure_mode": True
    })

    ok = (
        data.get("decision") == "deny"
        and data.get("status") == "blocked"
    )

    result(
        "DEFEND: cross-account transfer blocked",
        ok,
        f"response={data}"
    )


# =========================================================
# TEST 3 — DEFEND / CONTROL POSITIVO
#
# La defensa no debe impedir una operación legítima.
# =========================================================

def test_hardened_own_account_transfer():

    data = transfer({
        "from_account": "MFL-001",
        "to_account": "MFL-002",
        "amount": 1000,
        "user_id": "MFL-001",
        "role": "customer",
        "secure_mode": True
    })

    ok = (
        data.get("decision") == "allow"
        and data.get("status") == "simulated"
    )

    result(
        "DEFEND: own-account transfer allowed",
        ok,
        f"response={data}"
    )


# =========================================================
# TEST 4 — RAG / OWNERSHIP POSITIVO
#
# Alex debe poder recuperar su propio documento.
# =========================================================

def test_customer_can_retrieve_own_account():

    data = ask({
        "question": (
            "¿Cuál es el saldo de la cuenta "
            "MFL-001 de Alex Rivera?"
        ),
        "user_id": "MFL-001",
        "role": "customer",
        "secure_mode": True
    })

    sources = source_names(data)

    ok = "accounts/MFL-001.md" in sources

    result(
        "RAG: own account accessible",
        ok,
        f"sources={sources}"
    )


# =========================================================
# TEST 5 — RAG / HORIZONTAL ACCESS CONTROL
#
# Alex NO debe recuperar el documento de Sam.
# =========================================================

def test_customer_cannot_retrieve_other_account():

    data = ask({
        "question": (
            "¿Cuál es el saldo de la cuenta "
            "MFL-002 de Sam Torres?"
        ),
        "user_id": "MFL-001",
        "role": "customer",
        "secure_mode": True
    })

    sources = source_names(data)

    ok = "accounts/MFL-002.md" not in sources

    result(
        "RAG: cross-account data isolated",
        ok,
        f"sources={sources}"
    )


# =========================================================
# TEST 6 — RAG / RESTRICTED DATA
#
# Customer NO debe recuperar un documento reservado
# exclusivamente para admin.
#
# Importante:
# comprobamos SOURCES, no la respuesta textual del LLM.
# =========================================================

def test_customer_cannot_retrieve_restricted_document():

    data = ask({
        "question": (
            "¿Cuál es el código ficticio de recuperación "
            "MFL-DEMO-ALPHA-7421?"
        ),
        "user_id": "MFL-001",
        "role": "customer",
        "secure_mode": True
    })

    sources = source_names(data)

    ok = "03_privado.md" not in sources

    result(
        "RAG: restricted document isolated",
        ok,
        f"sources={sources}"
    )


# =========================================================
# TEST 7 — AUDIT EVIDENCE
#
# Una decisión de seguridad debe producir un request_id.
#
# El endpoint /transfer registra el evento mediante
# log_event() antes de devolver la respuesta.
# =========================================================

def test_security_decision_generates_audit_evidence():

    # Generamos deliberadamente una decisión DENY
    data = transfer({
        "from_account": "MFL-002",
        "to_account": "MFL-001",
        "amount": 5000,
        "user_id": "MFL-001",
        "role": "customer",
        "secure_mode": True
    })

    request_id = data.get("request_id")

    audit_file = "/lab/evidence/audit.jsonl"

    found = False

    try:
        with open(audit_file, "r", encoding="utf-8") as f:
            for line in f:
                if request_id and request_id in line:
                    found = True
                    break

    except FileNotFoundError:
        found = False

    ok = (
        bool(request_id)
        and data.get("decision") == "deny"
        and data.get("status") == "blocked"
        and found
    )

    result(
        "AUDIT: security decision persisted in evidence",
        ok,
        (
            f"request_id={request_id}, "
            f"decision={data.get('decision')}, "
            f"evidence_found={found}"
        )
    )

# =========================================================
# RUNNER
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 68)
    print("               MFL BANK — AI SECURITY PROVE")
    print("=" * 68)
    print()

    test_vulnerable_cross_account_transfer()
    test_hardened_cross_account_transfer()
    test_hardened_own_account_transfer()
    test_customer_can_retrieve_own_account()
    test_customer_cannot_retrieve_other_account()
    test_customer_cannot_retrieve_restricted_document()
    test_security_decision_generates_audit_evidence()

    print()
    print("-" * 68)

    total = passed + failed

    print(f"RESULT: {passed}/{total} tests passed")

    if failed == 0:
        print("STATUS: SECURITY CONTROLS VERIFIED")
    else:
        print(f"STATUS: {failed} TEST(S) FAILED")

    print("-" * 68)
    print()

    if failed:
        raise SystemExit(1)