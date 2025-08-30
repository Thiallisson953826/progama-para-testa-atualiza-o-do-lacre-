
# Aplicação Streamlit - Coleta de Palete e Lacres

Este é um aplicativo simples feito em Streamlit para coletar dados de palete, lacres e sigla da loja e enviar por e-mail usando SMTP do Outlook/Hotmail.

---

## Como usar

1. Configure suas credenciais de e-mail no arquivo `secrets.toml` (veja abaixo).
2. Execute o app localmente com `streamlit run app.py` ou faça deploy no Streamlit Cloud.
3. Na tela do app, preencha os campos e digite o e-mail de destino para enviar.

---

## Configuração do secrets.toml

Crie uma pasta `.streamlit` e dentro dela o arquivo `secrets.toml` com o conteúdo:

```
smtp_server = "smtp.office365.com"
smtp_port = 587
username = "seu-email@outlook.com"
password = "sua-senha-ou-senha-de-app"
```

**Nota:**  
- Se sua conta Outlook tem 2FA, gere uma senha de app no painel da Microsoft.  
- Nunca compartilhe seu `secrets.toml` publicamente.

---

## Deploy no Streamlit Cloud

1. Faça login em https://share.streamlit.io com sua conta GitHub.
2. Crie um repositório no GitHub e envie os arquivos.
3. No Streamlit Cloud, crie um novo app apontando para o repositório.
4. Configure os "Secrets" com as credenciais de e-mail na aba Settings.
5. Faça o deploy e use o app online!

---

## Dependências

- streamlit

