import streamlit as st
from metodos.database import iniciar_conexao, criar_tabelas

con = iniciar_conexao()
criar_tabelas(con)

st.set_page_config(page_title="Stude", page_icon="📚",  layout="centered")

tab1, tab2 = st.tabs(["Ciclos de Estudo", "Configurações"])

#########################
# ABA 1 Ciclos de Estudo
###########################

with tab1:
    ##############################
    # Botões principais (Start, Stop, Tags e Pause)
    ##############################
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write("\n")
        st.write("\n")
        start = st.button("Start", use_container_width=True) 
        
    with col2:
        st.write("\n")
        st.write("\n")
        tag = st.selectbox(
            "Escolha de tag", 
            options=["Matéria"],
            label_visibility="collapsed"
        )
        
    with col3:
        st.write("\n")
        st.write("\n")
        stop = st.button("Stop", use_container_width=True)

    with col4:
        pause = st.number_input("Tempo de Pausa", min_value=1, step=1)

    st.markdown("---")
    
    # Row 2: Aggregation Functions (Purple)
    col5, col6, col7 = st.columns(3)
    
    with col5:
        st.metric(label="Horas feitas hoje x Meta semanal", value="2h / 15h")
        
    with col6:
        st.metric(label="Horas na semana x Meta mensal", value="12h / 60h")
        
    with col7:
        st.metric(label="Horas feitas no mês", value="45h")

    st.markdown("---")
    
    # Notas
    notas = st.text_area(
        "Espaço para escrever:",
        value="Substituir valor",
        height=150
    )

#########################
# ABA 2 CONFIGURAÇÕES
###########################
with tab2:
    st.write("Configurações do sistema ficarão aqui.")
    # You can add configuration options here later
    
    

# if submit_button:
#     with con.cursor() as cur:
#         cur.execute("""
#             INSERT INTO log_estudo (data, minutos, pausas_min, tag_id)
#             VALUES (%s, %s, %s, %s)
#         """, (data_estudo, minutos_estudo, minutos_pausa, tag_escolhida))
        
#     con.commit() 
#     st.success("Sessão salva com sucesso!")