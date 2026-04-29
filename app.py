import streamlit as st
import psycopg2
from datetime import datetime
import time
from metodos.database import iniciar_conexao, criar_tabelas, obter_tags

st.set_page_config(page_title="Stude", page_icon="📚", layout="centered")

con = iniciar_conexao()
criar_tabelas(con)
tradutorTags = obter_tags(con)

# Se a variável 'estudando' não existir cria ela como Falsa
if 'estudando' not in st.session_state:
    st.session_state.estudando = False

# Se a hora de início não existir, criamos ela vazia
if 'hora_inicio' not in st.session_state:
    st.session_state.hora_inicio = None


tab1, tab2 = st.tabs(["Ciclos de Estudo", "Configurações"])

# ==========================================
# 1. ABA 1: Ciclos de Estudo
# ==========================================
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write("\n\n")
        start = st.button("Start", use_container_width=True) 
        
        # 2. LÓGICA DO START
        if start and not st.session_state.estudando:
            st.session_state.hora_inicio = datetime.now() # Guarda a hora exata agora!
            st.session_state.estudando = True
            st.info("⏱️ O tempo está rodando! Bons estudos.")
            
    with col2:
        st.write("\n\n")
        tag_selecionada = st.selectbox(
            "Escolha de tag", 
            options=list(tradutorTags.keys()),
            label_visibility="collapsed",
            index=None,
            placeholder="Matéria"
        )
        
    with col3:
        st.write("\n\n")
        stop = st.button("Stop", use_container_width=True)
        
        # 3. LÓGICA DO STOP
        if stop and st.session_state.estudando:
            hora_fim = datetime.now()
            
            tempo_total = hora_fim - st.session_state.hora_inicio
            minutos_estudo = int(tempo_total.total_seconds() / 60)
            
            # Se você parar muito rápido durante os testes, ele salva pelo menos 1 min
            if minutos_estudo == 0:
                minutos_estudo = 1 
                
            # Esvazia a variável para uma próxima sessão
            st.session_state.estudando = False
            st.session_state.hora_inicio = None
            
            # Mostra o resultado na tela!
            st.success(f"🎉 Sessão finalizada! Você estudou por {minutos_estudo} minutos.")

    with col4:
        # Renomeei a variável para não conflitar com a palavra "pause"
        minutos_pausa = st.number_input("Tempo de Pausa", min_value=0, step=1)

    st.divider()
    
    col5, col6, col7 = st.columns(3)
    with col5:
        st.metric(label="Horas feitas hoje x Meta semanal", value="2h / 15h")
    with col6:
        st.metric(label="Horas na semana x Meta mensal", value="12h / 60h")
    with col7:
        st.metric(label="Horas feitas no mês", value="45h")

    st.divider() 
    
    notas = st.text_area("Espaço para escrever:", value="Substituir valor", height=150)

# ==========================================
# 2. ABA 2: CONFIGURAÇÕES
# ==========================================
with tab2:
    st.markdown("#### Configure suas matérias e Visualize")
    
    with st.form("configuracoes_form", clear_on_submit=True):
        col_input, col_botao = st.columns([3, 1])

        with col_input:
            nova_materia = st.text_input(
                "Digite o nome da matéria", 
                placeholder="Ex: Matemática, Python, etc...",
                label_visibility="collapsed" 
            )

        with col_botao:
            submit_materia = st.form_submit_button("Salvar Matéria", use_container_width=True)

    if submit_materia:
        if nova_materia.strip() == "":
            st.warning("⚠️ O nome da matéria não pode ser vazio!")
        else:
            with con.cursor() as cur:
                cur.execute("""
                    INSERT INTO tags (tag) 
                    VALUES (%s);
                """, (nova_materia.capitalize(),))
            
            con.commit()
            st.success(f"✅ Matéria '{nova_materia.capitalize()}' criada com sucesso!")
            time.sleep(1)
            st.rerun()

# ==========================================
# 3. SALVANDO NO BANCO DE DADOS
# ==========================================
if stop and 'minutos_estudo' in locals():
    # Pegamos a data de hoje para salvar
    if tag_selecionada is None:
        st.error("⚠️ Escolha uma matéria antes de parar o tempo!")
        st.session_state.estudando = True
    else:
        data_estudo = datetime.now().date()
        tag_escolhida_id = tradutorTags[tag_selecionada]

        with con.cursor() as cur:
            cur.execute("""
                INSERT INTO log_estudo (data, minutos, pausas_min, tag_id)
                VALUES (%s, %s, %s, %s)
            """, (data_estudo, minutos_estudo, minutos_pausa, tag_escolhida_id))
            
        con.commit()