import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

st.title("Coleta de Palete e Lacres")

palete = st.text_input("Palete")
lacre1 = st.text_input("Lacre 1")
lacre2 = st.text_input("Lacre 2")
sigla = st.text_input("Sigla da Loja")
email_destino = st.text_input("E-mail para envio")

if st.button("Enviar"):
    if not (palete and lacre1 and lacre2 and sigla and email_destino):
        st.warning("Preencha todos os campos!")
    else:
        SMTP_SERVER = st.secrets["smtp_server"]
        SMTP_PORT = st.secrets["smtp_port"]
        USER = st.secrets["username"]
        PASSWORD = st.secrets["password"]

        msg = MIMEMultipart()
        msg["Subject"] = f"Coleta {palete} - {sigla}"
        msg["From"] = USER
        msg["To"] = email_destino

        corpo = f"""
Palete: {palete}
Lacre 1: {lacre1}
Lacre 2: {lacre2}
Loja: {sigla}
Hora: {datetime.now():%d/%m/%Y %H:%M:%S}
"""

        msg.attach(MIMEText(corpo, "plain"))

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(USER, PASSWORD)
            server.sendmail(USER, email_destino, msg.as_string())
            server.quit()
            st.success("E-mail enviado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao enviar: {e}")
