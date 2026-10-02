# MFL Bank — AI Security Lab
# Author: @freyley.leyva

import os
import requests
import streamlit as st


# =========================================================
# CONFIGURACIÓN
# =========================================================

API = os.getenv("API_URL", "http://api:8000")

st.set_page_config(
    page_title="MFL Bank — AI Security Lab",
    page_icon="🏦",
    layout="wide"
)


# =========================================================
# IDENTIDADES FICTICIAS DEL LABORATORIO
# =========================================================

USERS = {
    "Alex Rivera": {
        "user_id": "MFL-001",
        "role": "customer"
    },
    "Sam Torres": {
        "user_id": "MFL-002",
        "role": "customer"
    },
    "Sofía Méndez": {
        "user_id": "MFL-SUPPORT-01",
        "role": "support"
    },
    "Morgan Lee": {
        "user_id": "MFL-ADMIN-01",
        "role": "admin"
    }
}


# =========================================================
# ENCABEZADO
# =========================================================

st.title("🏦 MFL Bank")

st.caption(
    "AI Security Lab · BUILD → BREAK → DEFEND → PROVE "
    "· Entorno 100% ficticio · @freyley.leyva"
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("👤 Identidad ficticia")

    selected_user = st.selectbox(
        "Usuario",
        list(USERS.keys())
    )

    user = USERS[selected_user]

    st.write(f"**ID:** `{user['user_id']}`")
    st.write(f"**Rol:** `{user['role']}`")

    st.divider()

    st.header("🛡️ Security Mode")

    secure = st.toggle(
        "Hardened mode",
        value=False,
        help="Activa los controles defensivos del laboratorio"
    )

    if secure:
        st.success("🔵 HARDENED")
    else:
        st.error("🔴 VULNERABLE")

    st.divider()

    st.markdown("### 🔎 Explorer")

    st.markdown("[FastAPI / Swagger](http://localhost:8000/docs)")
    st.markdown("[Qdrant](http://localhost:6333/dashboard)")
    st.markdown("[Jaeger](http://localhost:16686)")


# =========================================================
# ESTADO DEL CHAT
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hola. Soy el asistente virtual de MFL Bank. "
                "¿En qué puedo ayudarte?"
            )
        }
    ]


# =========================================================
# ÁREA PRINCIPAL
# =========================================================

col_chat, col_lab = st.columns([3, 1])


# =========================================================
# CHAT
# =========================================================

with col_chat:

    st.subheader("💬 MFL Assistant")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "Pregunta algo a MFL Bank..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        # -------------------------------------------------
        # Por ahora conservamos compatibilidad con API v0.1
        # -------------------------------------------------

        try:

            with st.spinner("MFL Assistant está pensando..."):

                response = requests.post(
                    f"{API}/ask",
                    json={
                        "question": question,
                        "role": user["role"],
                        "secure_mode": secure
                    },
                    timeout=240
                )

                response.raise_for_status()

                data = response.json()

                answer = data["answer"]

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            with st.chat_message("assistant"):

                st.markdown(answer)

                st.caption(
                    f"request_id: {data['request_id']}"
                )

                with st.expander("📚 Fuentes recuperadas"):
                    st.json(data["sources"])

        except requests.exceptions.Timeout:

            st.error(
                "El modelo local tardó demasiado en responder."
            )

        except requests.exceptions.RequestException as exc:

            st.error(
                f"No fue posible comunicarse con MFL API: {exc}"
            )


# =========================================================
# PANEL DEL LABORATORIO
# =========================================================

with col_lab:

    st.subheader("🧪 Laboratorio")

    if secure:

        st.info(
            """
            🔵 **DEFEND**

            Los controles defensivos están activos.

            Intenta repetir los ataques.
            """
        )

    else:

        st.warning(
            """
            🔴 **BREAK**

            La aplicación está en modo vulnerable.

            ¿Qué puedes conseguir que haga?
            """
        )

    st.divider()

    st.markdown("### Identidad activa")

    st.code(
        f"""user_id = {user["user_id"]}
role = {user["role"]}"""
    )

    st.divider()

    if st.button(
        "📚 Ingestar Knowledge Base",
        use_container_width=True
    ):

        try:

            response = requests.post(
                f"{API}/ingest",
                timeout=240
            )

            response.raise_for_status()

            st.success("Knowledge Base actualizada.")

            st.json(response.json())

        except requests.exceptions.RequestException as exc:

            st.error(
                f"No fue posible realizar la ingesta: {exc}"
            )