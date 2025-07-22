import streamlit_authenticator as stauth

# Usuários e senhas
users = ['user1', 'user2']
names = ['Usuário 1', 'Usuário 2']
passwords = ['123', 'abc']

# Criação dos hashes
hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(
    names, users, hashed_passwords,
    'cidade_limpa_cookie', 'abcdef', cookie_expiry_days=30
)

# Tela de login
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == False:
    st.error('Usuário ou senha incorretos.')

if authentication_status == None:
    st.warning('Por favor, faça login.')

if authentication_status:
    authenticator.logout('Sair', 'sidebar')
    st.sidebar.success(f'Bem-vindo, {name} 👋')

    # DAQUI PRA BAIXO: seu app continua normalmente




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
