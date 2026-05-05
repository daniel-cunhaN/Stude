import streamlit as st
import psycopg2
from datetime import datetime
import time
import pandas as pd
from metodos.database import iniciar_conexao, criar_tabelas, obter_tags
from metodos.horas_e_metas import agregar_horas, extrair_metas


st.set_page_config(page_title="Stude", page_icon="📚", layout="centered")

con = iniciar_conexao()
try:
    con.rollback() # Limpa qualquer transação falha residual
except:
    pass
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
    col1, col2, col3, col4 = st.columns(4, vertical_alignment="bottom")
    
    with col1: #START
        start = st.button("Start", use_container_width=True) 
        
        # LÓGICA DO START
        if start and not st.session_state.estudando:
            st.session_state.hora_inicio = datetime.now() # Guarda a hora exata agora
            st.session_state.estudando = True
            st.toast("⏱️ O tempo está rodando! Bons estudos.")
            
    with col2: # SELEÇÃO DE MATÉRIA
        tag_selecionada = st.selectbox(
            "Escolha de tag", 
            options=list(tradutorTags.keys()),
            label_visibility="collapsed",
            index=None,
            placeholder="Matéria"
        )
        
    with col3: # STOP
        stop = st.button("Stop", use_container_width=True)
        
        # LÓGICA DO STOP
        if stop and st.session_state.estudando:
            hora_fim = datetime.now()
            
            tempo_total = (hora_fim)-(st.session_state.hora_inicio)
            minutos_estudo = int(tempo_total.total_seconds() / 60)
            
            # Se você parar muito rápido durante os testes, ele salva pelo menos 1 min
            if minutos_estudo == 0:
                minutos_estudo = 1 
                
            # Esvazia a variável para uma próxima sessão
            st.session_state.estudando = False
            st.session_state.hora_inicio = None
            
            # Mostra o resultado na tela
            st.toast(f"🎉 Sessão finalizada! Você estudou por {minutos_estudo} minutos.")

    with col4: # PAUSA
        minutos_pausa = st.number_input("", min_value=0, step=1)

    st.divider()
    
    # Área de horas estudadas X metas

    horas_hoje, horas_semana, horas_mes = agregar_horas(con)
    meta_semana, meta_mes = extrair_metas(con)
    
    col5, col6, col7 = st.columns(3, vertical_alignment="bottom")
    with col5:
        st.metric(label="Horas feitas hoje x Meta semanal", value=f"{horas_hoje}h/{meta_semana}h")
    with col6:
        st.metric(label="Horas feitas na semana x Meta mensal", value=f"{horas_semana}h/{meta_mes}h") 
    with col7:
        st.metric(label="Horas feitas no mês", value=f"{horas_mes}h") 
    st.divider() 

    # Notas
    with con.cursor() as cur:
        cur.execute("SELECT texto FROM notas WHERE id = 1;")
        resultado = cur.fetchone()
        nota_antiga = resultado[0] if resultado else ""

    nota_nova = st.text_area(
        "Espaço para escrever:", 
        value=nota_antiga,
        height=150, 
        placeholder="Escreva suas notas"
    )

    if nota_nova != nota_antiga:
        with con.cursor() as cur:
            cur.execute("UPDATE notas SET texto = %s WHERE id = 1;", (nota_nova,))
        con.commit()
        st.toast("✅ Nota salva!")

# ==========================================
# 1.1. SALVANDO NO BANCO DE DADOS
# ==========================================
if stop and 'minutos_estudo' in locals():
    # Pegamos a data de hoje para salvar
    if tag_selecionada is None:
        st.error("⚠️ Escolha uma matéria antes de parar o tempo!")
        st.session_state.estudando = True
    else:
        try:
            data_estudo = datetime.now().date()
            tag_escolhida_id = tradutorTags[tag_selecionada]

            with con.cursor() as cur:
                cur.execute("""
                    INSERT INTO log_estudo (data, minutos, pausas_min, tag_id)
                    VALUES (%s, %s, %s, %s)
                """, (data_estudo, minutos_estudo, minutos_pausa, tag_escolhida_id))
                
            con.commit()
        except Exception as e:
            con.rollback()
            st.error(f"Erro ao salvar sessão de estudo: {e}")
# ==========================================
# 2. ABA 2: CONFIGURAÇÕES
# ==========================================
with tab2:
    st.markdown("#### Configure suas matérias e Visualize")
    
    with st.form("configuracoes_form", clear_on_submit=True):
        col_input, col_botao = st.columns([3, 1])

        # ==========================================
        # 2.1 Criação de matéria
        # ==========================================


        with col_input:
            nova_materia = st.text_input(
                "Digite o nome da matéria", 
                placeholder="Crie sua matéria aqui",
                label_visibility="collapsed" 
            )

        with col_botao:
            submit_materia = st.form_submit_button("Salvar Matéria", use_container_width=True)

        # ==========================================
        # 2.2 Exclusão de matéria
        # ==========================================


        col_input2, col_botao2 = st.columns([3, 1])

        with col_input2:
            tag_excluir = st.selectbox(
                "Excluir matéria", 
                options=list(tradutorTags.keys()), 
                label_visibility="collapsed", 
                placeholder="Selecione a matéria para exclusão"
            )
        
        with col_botao2:
            submit_excluirMateria = st.form_submit_button("Excluir Matéria", use_container_width=True)
        
        st.divider()
        
        # ==========================================
        # 2.3 Criação de Meta
        # ==========================================

        # CRIAÇÃO META SEMANAL

        meta_semanal_input, meta_semanal_salvar = st.columns([3, 1], vertical_alignment="bottom")

        with meta_semanal_input:
            nova_meta_semanal = st.text_input("", placeholder="Digite quantas hora será sua meta semanal")

        with meta_semanal_salvar:
            submit_meta_semanal = st.form_submit_button("Salvar Meta Semanal", use_container_width=True)

        # CRIAÇÃO META MENSAL

        meta_mensal_input, meta_mensal_salvar = st.columns([3, 1], vertical_alignment="bottom")

        with meta_mensal_input:
            nova_meta_mensal = st.text_input("", placeholder="Digite quantas hora será sua meta mensal")

        with meta_mensal_salvar:
            submit_meta_mensal = st.form_submit_button("Salvar Meta Mensal", use_container_width=True)
      

            
    # =================================================
    # 2.4 Condicionais de Criação e Exclusão de Matéria
    # =================================================
    if submit_materia:
        if nova_materia.strip() == "":
            st.warning("⚠️ O nome da matéria não pode ser vazio!")
        else:
            try:
                with con.cursor() as cur:
                    cur.execute("""
                        INSERT INTO tags (tag) 
                        VALUES (%s);
                    """, (nova_materia.capitalize(),))
                
                con.commit()
                st.success(f"✅ Matéria '{nova_materia.capitalize()}' criada com sucesso!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                con.rollback()
                st.error(f"Erro ao salvar matéria: {e}")
            
    if submit_excluirMateria:
        if tag_excluir:
            try:
                id_excluir = tradutorTags[tag_excluir]
                with con.cursor() as cur:
                    cur.execute("DELETE FROM tags WHERE id = %s;", (id_excluir,))
                con.commit()
                st.toast(f"🗑️ Matéria '{tag_excluir}' excluída!")
                time.sleep(1)
                st.rerun()
            except psycopg2.errors.ForeignKeyViolation:
                con.rollback()
                st.error(f"❌ Não é possível excluir '{tag_excluir}' pois existem registros de estudo vinculados a ela.")
            except Exception as e:
                con.rollback()
                st.error(f"Erro ao excluir matéria: {e}")

    # ==================================================
    # 2.5 Condicionais de Criação e Atualização de Metas
    # ==================================================

    # METAS SEMANAIS

    if submit_meta_semanal:
        if nova_meta_semanal.strip() == "":
            st.warning("⚠️ O número de horas da meta não pode ser nulo!")
        else:
            try:
                horas = int(nova_meta_semanal)
                with con.cursor() as cur:
                    cur.execute("SELECT 1 FROM metas WHERE tipo_meta = 'semanal'")
                    if cur.fetchone(): # Se a query existe, então...
                        cur.execute("UPDATE metas SET horas_alvo = %s WHERE tipo_meta = 'semanal'", (horas,))
                    else:
                        cur.execute("INSERT INTO metas (tipo_meta, horas_alvo) VALUES ('semanal', %s)", (horas,))
                
                con.commit()
                st.toast(f"✅ Meta semanal ('{horas}h') salva com sucesso!")
                time.sleep(1)
                st.rerun()
            except ValueError:
                st.error("⚠️ Por favor, insira um número válido (apenas números).")
            except Exception as e:
                con.rollback()
                st.error(f"Erro ao salvar a meta semanal: {e}")

    # METAS MENSAIS

    if submit_meta_mensal:
        if nova_meta_mensal.strip() == "":
            st.warning("⚠️ O número de horas da meta não pode ser nulo!")
        else:
            try:
                horas = int(nova_meta_mensal)
                with con.cursor() as cur:
                    cur.execute("SELECT 1 FROM metas WHERE tipo_meta = 'mensal'")
                    if cur.fetchone(): # Se a query existe, então...
                        cur.execute("UPDATE metas SET horas_alvo = %s WHERE tipo_meta = 'mensal'", (horas,))
                    else:
                        cur.execute("INSERT INTO metas (tipo_meta, horas_alvo) VALUES ('mensal', %s)", (horas,))
                
                con.commit()
                st.toast(f"✅ Meta mensal ('{horas}h') salva com sucesso!")
                time.sleep(1)
                st.rerun()
            except ValueError:
                st.error("⚠️ Por favor, insira um número válido (apenas números).")
            except Exception as e:
                con.rollback()
                st.error(f"Erro ao salvar a meta mensal: {e}")

                    
# ==========================================
# 2.6 Visualização de Tags
# ==========================================
    queryTags = """
    SELECT tag FROM tags
    """
    visualizarTags = pd.read_sql(queryTags, con)
    if not visualizarTags.empty:
        visualizarTags.fillna('', inplace=True) 
        st.dataframe(visualizarTags, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum registro encontrado ainda.")
        
        st.divider()