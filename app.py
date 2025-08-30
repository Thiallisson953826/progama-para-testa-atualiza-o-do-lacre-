import streamlit as st
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

st.set_page_config(page_title="📦 Coleta por Palete")
st.title("📦 Coleta de Palete e Lacres")

# Inicializa variáveis de estado
if "etapa" not in st.session_state:
    st.session_state.etapa = 1
if "emails_adicionais" not in st.session_state:
    st.session_state.emails_adicionais = []

# Funções para avanço de etapa automático
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

# Etapa 3: Lacres com validação
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

# Etapa 4: Envio de e-mails
if st.session_state.etapa == 4:
    email_opcoes = {
        "TLC - thiallisson@live.com": "thiallisson@live.com",
        "EHC - eslandialia@hotmail.com": "eslandialia@hotmail.com",
        "WGC - Wolfman13690@gmail.com": "Wolfman13690@gmail.com",
        "EPA - Edvaldo.pereira@armazemparaiba.com.br": "Edvaldo.pereira@armazemparaiba.com.br"
    }

    st.subheader("📧 E-mails de destino")
    emails_destino = st.multiselect("Escolha os e-mails da lista", options=list(email_opcoes.keys()))

    # Campo para adicionar e-mails extras
    novo_email = st.text_input("Ou digite um e-mail manualmente e aperte ENTER", key="email_livre")
    if novo_email:
        if re.match(r"[^@]+@[^@]+\.[^@]+", novo_email):
            if novo_email not in st.session_state.emails_adicionais:
                st.session_state.emails_adicionais.append(novo_email)
                st.success(f"✅ E-mail adicionado: {novo_email}")
                if "email_livre" in st.session_state:
                    st.session_state.email_livre = ""
                st.experimental_rerun()
        else:
            st.error("❌ E-mail inválido. Verifique e tente novamente.")

    # Mostrar e-mails manuais adicionados
    if st.session_state.emails_adicionais:
        st.write("📌 E-mails manuais adicionados:")
        for e in st.session_state.emails_adicionais:
            st.write(f"• {e}")

    # Mostrar lista final de e-mails
    emails_real = [email_opcoes[nome] for nome in emails_destino] + st.session_state.emails_adicionais
    if emails_real:
        st.write("📬 Lista final de e-mails que receberão a coleta:")
        for e in emails_real:
            st.write(f"• {e}")

    # Botão de envio
    if st.button("Enviar"):
        loja = st.session_state.get("loja", "").strip()
        palete = st.session_state.get("palete", "").strip()
        lacres_raw = st.session_state.get("lacres", "")
        lacre_list = [l.strip() for l in lacres_raw.replace('\n', ',').split(',') if l.strip()]
        lacre_unicos = list(dict.fromkeys(lacre_list))

        if not emails_real:
            st.warning("⚠️ Nenhum e-mail selecionado ou digitado!")
        else:
            SMTP_SERVER = st.secrets["smtp_server"]
            SMTP_PORT = st.secrets["smtp_port"]
            USER = st.secrets["username"]
            PASSWORD = st.secrets["password"]

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

                # Limpa os dados após envio
                st.session_state.etapa = 1
                st.session_state.emails_adicionais = []
                st.session_state.loja_input = ""
                st.session_state.palete_input = ""
                st.session_state.lacres_input = ""
            except Exception as e:
                st.error(f"❌ Erro ao enviar: {e}")
