import streamlit as st
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="📦 Coleta por Palete")
st.title("📦 Coleta de Palete e Lacres")

# Inicializa variáveis de estado
if "etapa" not in st.session_state:
    st.session_state.etapa = 1

# Funções para mudança de etapa automática
def avancar_etapa_1():
    if st.session_state.loja_input.strip():
        st.session_state.loja = st.session_state.loja_input.strip()
        st.session_state.etapa = 2

def avancar_etapa_2():
    if st.session_state.palete_input.strip():
        st.session_state.palete = st.session_state.palete_input.strip()
        st.session_state.etapa = 3

# Etapa 1: Loja
if st.session_state.etapa == 1:
    st.text_input("Digite a Loja e aperte ENTER", key="loja_input", on_change=avancar_etapa_1)

# Etapa 2: Palete
elif st.session_state.etapa == 2:
    st.text_input("Bipar Palete e aperte ENTER", key="palete_input", on_change=avancar_etapa_2)

# Etapa 3: Lacres com validação imediata
elif st.session_state.etapa == 3:
    lacres_input = st.text_area("Bipar os Lacres (um por linha ou separados por vírgula)", key="lacres_input")

    if lacres_input:
        lacre_list = [l.strip() for l in lacres_input.replace('\n', ',').split(',') if l.strip()]
        lacre_unicos = list(dict.fromkeys(lacre_list))

        if len(lacre_list) != len(lacre_unicos):
            st.error("⚠️ Existem lacres duplicados! Remova os repetidos antes de continuar.")
        else:
            st.session_state.lacres = lacres_input
            st.session_state.etapa = 4

# Etapa final: Envio do e-mail
if st.session_state.etapa == 4:
    email_opcoes = {
        "EHC - eslandialia@hotmail.com": "eslandialia@hotmail.com",
        "WGC - Wolfman13690@gmail.com": "Wolfman13690@gmail.com",
        "EPA - Edvaldo.pereira@armazemparaiba.com.br": "Edvaldo.pereira@armazemparaiba.com.br"
    }

    emails_destino = st.multiselect("Escolha os e-mails para envio", options=list(email_opcoes.keys()))

    if st.button("Enviar"):
        loja = st.session_state.get("loja", "").strip()
        palete = st.session_state.get("palete", "").strip()
        lacres_raw = st.session_state.get("lacre_input", st.session_state.get("lacres", ""))

        lacre_list = [l.strip() for l in lacres_raw.replace('\n', ',').split(',') if l.strip()]
        lacre_unicos = list(dict.fromkeys(lacre_list))

        if not emails_destino:
            st.warning("⚠️ Nenhum e-mail selecionado!")
        else:
            # Configurações do Outlook/Office365
            SMTP_SERVER = "smtp.office365.com"
            SMTP_PORT = 587
            USER = st.secrets["username"]      # exemplo: "csaidcpmr@armazemparaiba.com.br"
            PASSWORD = st.secrets["password"]  # sua senha real ou App Password

            emails_real = [email_opcoes[nome] for nome in emails_destino]

            msg = MIMEMultipart()
            msg["Subject"] = f"Coleta {palete} - {loja}"
            msg["From"] = USER
            msg["To"] = ", ".join(emails_real)

            corpo = f"""
📦 Palete: {palete}
🔒 Lacres: {', '.join(lacre_unicos)}
🏬 Loja: {loja}
🕒 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
"""

            msg.attach(MIMEText(corpo, "plain"))

            try:
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()
                server.login(USER, PASSWORD)
                server.sendmail(USER, emails_real, msg.as_string())
                server.quit()
                st.success("✅ E-mail enviado com sucesso!")
            except Exception as e:
                st.error(f"❌ Erro ao enviar: {e}")
