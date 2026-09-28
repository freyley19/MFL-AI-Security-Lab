# MFL AI Security Lab UI
# Author: @freyley.leyva
import os, requests, streamlit as st
API=os.getenv("API_URL","http://api:8000")
st.set_page_config(page_title="MFL AI Security Lab",page_icon="🛡️",layout="wide")
st.title("🛡️ MFL AI Security Lab")
st.caption("BUILD → BREAK → DEFEND → PROVE · Laboratorio 100% ficticio · @freyley.leyva")
with st.sidebar:
    st.header("Identidad ficticia")
    role=st.selectbox("Rol",["guest","support","admin"])
    secure=st.toggle("Secure mode",value=False,help="Activa controles defensivos del laboratorio")
    st.divider(); st.markdown("**Explorer**")
    st.markdown("[Swagger](http://localhost:8000/docs)")
    st.markdown("[Qdrant](http://localhost:6333/dashboard)")
    st.markdown("[Jaeger](http://localhost:16686)")
col1,col2=st.columns([2,1])
with col1:
    q=st.text_input("Pregunta a MFL",placeholder="Ej. ¿Cuál es el horario de soporte?")
    if st.button("Preguntar",type="primary") and q:
        try:
            r=requests.post(f"{API}/ask",json={"question":q,"role":role,"secure_mode":secure},timeout=200)
            r.raise_for_status(); data=r.json()
            st.success(data["answer"])
            st.caption(f"request_id: {data['request_id']}")
            with st.expander("Fuentes recuperadas"):
                st.json(data["sources"])
        except Exception as e: st.error(str(e))
with col2:
    st.subheader("Misión actual")
    st.info("🟢 BUILD\n\nPrimero entiende cómo funciona MFL. Después cambiaremos de cachucha.")
    if st.button("Ingestar documentos"):
        try:
            r=requests.post(f"{API}/ingest",timeout=240); r.raise_for_status(); st.json(r.json())
        except Exception as e: st.error(str(e))
