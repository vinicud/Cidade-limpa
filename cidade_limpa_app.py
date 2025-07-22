import streamlit as st
import streamlit_authenticator as stauth

# --- USUÁRIOS E SENHAS ---
usernames = ['usuario1']
names = ['Usuário Teste']
passwords = ['123']  # senhas simples só para teste

# Criação do hash das senhas
hashed_passwords = stauth.Hasher(passwords).generate()

# Criando o autenticador
authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    'cidade_limpa',  # nome da aplicação
    'abcdef',        # chave secreta (pode ser qualquer string)
    cookie_expiry_days=30
)

# Login
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:


import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="LixoZero Beta", layout="wide")

st.title("🧹 LixoZero Beta")
st.subheader("Ajude a manter sua cidade limpa!")

menu = st.sidebar.selectbox("Navegação", ["📍 Mapa", "🚨 Reportar Lixo", "🏆 Ranking dos Bairros"])

# Dados simulados (pontos de lixo)
data = pd.DataFrame({
    'bairro': ['Periz de Cima', 'Periz de Baixo', 'Centro', 'Jardim Tropical'],
    'lat': [-2.5123, -2.5167, -2.5105, -2.5180],
    'lon': [-44.2543, -44.2600, -44.2480, -44.2655],
    'status': ['Aguardando coleta', 'Coletado', 'Aguardando coleta', 'Aguardando coleta']
})

if menu == "📍 Mapa":
    st.markdown("### Locais com lixo reportado")
    mapa = folium.Map(location=[-2.5140, -44.2550], zoom_start=14)
    for i, row in data.iterrows():
        color = 'red' if row['status'] == 'Aguardando coleta' else 'green'
        folium.Marker([row['lat'], row['lon']],
                      tooltip=f"{row['bairro']} - {row['status']}",
                      icon=folium.Icon(color=color)).add_to(mapa)
    folium_static(mapa, width=900, height=500)

elif menu == "🚨 Reportar Lixo":
    st.markdown("### Reporte um novo local com lixo:")
    nome = st.text_input("Seu nome")
    bairro = st.text_input("Bairro")
    descricao = st.text_area("Descrição do local")
    if st.button("Enviar"):
        st.success("✅ Obrigado! Sua denúncia foi registrada e será avaliada.")
        # Aqui você poderia salvar isso num banco de dados real futuramente

elif menu == "🏆 Ranking dos Bairros":
    st.markdown("### Bairros com mais denúncias de lixo:")
    ranking = data['bairro'].value_counts().reset_index()
    ranking.columns = ['Bairro', 'Total de Lixos Reportados']
    st.table(ranking)
