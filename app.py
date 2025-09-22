import streamlit as st
from db_sqlite import create_tables, insert_city, query_cities
from db_mongo import create_collection, insert_local, query_locais
from geoprocessamento import calcular_distancia, locais_proximos
import folium
from streamlit_folium import folium_static

create_tables()
create_collection()

def main():
    st.set_page_config(page_title="Persistência Poliglota", layout="wide")
    st.title("🌍 Persistência Poliglota com MongoDB e SQLite")
    st.sidebar.title("📋 Main")
    menu = st.sidebar.radio("Selecione uma funcionalidade:", ["Cadastro de Cidades", "Cadastro de Locais", "Consulta de Locais", "Geoprocessamento"])

    if menu == "Cadastro de Cidades":
        st.header("🏙️ Cadastro de Cidades")
        st.write("Nesta seção, você pode cadastrar novas cidades e seus respectivos estados no banco de dados SQLite.")
        nome = st.text_input("Digite o nome da cidade:")
        estado = st.text_input("Digite o estado correspondente:")
        if st.button("Cadastrar Cidade"):
            if nome and estado:
                insert_city(nome, estado)
                st.success(f"A cidade **{nome}** foi cadastrada com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos.")

    elif menu == "Cadastro de Locais":
        st.header("📍 Cadastro de Locais")
        st.write("Aqui você pode cadastrar novos locais de interesse, incluindo suas coordenadas geográficas e uma descrição dentro do mongoDB.")
        nome_local = st.text_input("Digite o nome do local:")
        cidade = st.text_input("Digite a cidade onde o local está situado:")
        latitude = st.number_input("Digite a latitude (ex: -7.11532):", format="%.6f")
        longitude = st.number_input("Digite a longitude (ex: -34.861):", format="%.6f")
        descricao = st.text_area("Adicione uma descrição para o local:")
        if st.button("Cadastrar Local"):
            if nome_local and cidade and descricao:
                insert_local(nome_local, cidade, latitude, longitude, descricao)
                st.success(f"O local **{nome_local}** foi cadastrado com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos.")

    elif menu == "Consulta de Locais":
        st.header("🔍 Consulta de Locais")
        st.write("Selecione uma cidade cadastrada para visualizar os locais de interesse associados a ela.")
        cidades = query_cities()
        cidade_selecionada = st.selectbox("Selecione uma cidade:", [f"{c[1]} - {c[2]}" for c in cidades])
        if cidade_selecionada:
            cidade_nome = cidade_selecionada.split(" - ")[0]
            locais = [l for l in query_locais() if l['cidade'] == cidade_nome]
            st.write(f"### Locais cadastrados na cidade **{cidade_nome}**:")

            if locais:
                mapa = folium.Map(location=[locais[0]['coordenadas']['latitude'], locais[0]['coordenadas']['longitude']], zoom_start=12, width='100%', height='600px')
                for local in locais:
                    folium.Marker(
                        location=[local['coordenadas']['latitude'], local['coordenadas']['longitude']],
                        popup=f"{local['nome_local']}: {local['descricao']}",
                    ).add_to(mapa)
                folium_static(mapa)
            else:
                st.warning("Nenhum local encontrado para esta cidade.")
    elif menu == "Geoprocessamento":
        st.header("🗺️ Geoprocessamento")
        st.write("Forneça uma coordenada e um raio para encontrar locais próximos, ou calcule a distância entre dois pontos.")

        # Coordenadas do ponto de referência
        latitude = st.number_input("Digite a latitude do ponto de referência (ex: -7.065):", format="%.6f")
        longitude = st.number_input("Digite a longitude do ponto de referência (ex: -34.8417):", format="%.6f")
        raio = st.number_input("Digite o raio de busca (em km):", min_value=0.0, format="%.2f")

        if st.button("Buscar Locais Próximos"):
            locais = query_locais()
            proximos = locais_proximos((latitude, longitude), locais, raio)
            st.write(f"### Locais encontrados em um raio de **{raio} km**:")

            if proximos:
                mapa = folium.Map(location=[latitude, longitude], zoom_start=12)
                folium.Marker(
                    location=[latitude, longitude],
                    popup="Ponto de Referência",
                    icon=folium.Icon(color="red")
                ).add_to(mapa)

                for local in proximos:
                    folium.Marker(
                        location=[local['coordenadas']['latitude'], local['coordenadas']['longitude']],
                        popup=f"{local['nome_local']}: {local['descricao']}",
                    ).add_to(mapa)

                folium_static(mapa)
            else:
                st.warning("Nenhum local encontrado dentro do raio especificado.")

        # Cálculo de distância entre dois pontos
        st.write("---")
        st.write("### Calcular Distância entre Dois Pontos")
        lat1 = st.number_input("Digite a latitude do primeiro ponto (ex: -7.065):", key="lat1", format="%.6f")
        lon1 = st.number_input("Digite a longitude do primeiro ponto (ex: -34.8417):", key="lon1", format="%.6f")
        lat2 = st.number_input("Digite a latitude do segundo ponto (ex: -7.12000):", key="lat2", format="%.6f")
        lon2 = st.number_input("Digite a longitude do segundo ponto (ex: -34.87000):", key="lon2", format="%.6f")

        if st.button("Calcular Distância"):
            if lat1 and lon1 and lat2 and lon2:
                distancia = calcular_distancia((lat1, lon1), (lat2, lon2))
                st.success(f"A distância entre os dois pontos é de **{distancia:.2f} km**.")
            else:
                st.error("Por favor, preencha todas as coordenadas.")

if __name__ == "__main__":
    main()