import streamlit as st
import psycopg2
from datetime import datetime
import time
import pandas as pd
import os
from metodos.database import iniciar_conexao, criar_tabelas, obter_tags
from metodos.horas_e_metas import agregar_horas, extrair_metas


st.set_page_config(page_title="Stude", page_icon="📚", layout="centered")
st.title("🖊️Stude")
con = iniciar_conexao()
try:
    con.rollback() # Limpa qualquer transação falha residual
except:
    pass

def carregar_dados(conexao):
    st.session_state.tradutorTags = obter_tags(conexao)
    st.session_state.horas = agregar_horas(conexao)
    st.session_state.metas = extrair_metas(conexao)
    with conexao.cursor() as cur:
        cur.execute("SELECT texto FROM notas WHERE id = 1;")
        resultado = cur.fetchone()
        st.session_state.nota_antiga = resultado[0] if resultado else ""

if "tabelas_criadas" not in st.session_state:
    criar_tabelas(con)
    st.session_state.tabelas_criadas = True

if "tradutorTags" not in st.session_state:
    carregar_dados(con)

tradutorTags = st.session_state.tradutorTags

tab1, tab2, tab3 = st.tabs(["Ciclos de Estudo", "Configurações", "Dashboard"])
# ==========================================
# 1. ABA 1: Ciclos de Estudo
# ==========================================

if "mostrar_notificacao" not in st.session_state:
    st.session_state.mostrar_notificacao = False

with tab1:
    col1, col2, col3, col4 = st.columns(4, vertical_alignment="bottom")
    with col1: #START
        st.caption("Iniciar Temporizador")
        start = st.button("Start", use_container_width=True) 
        if start:
            # Notificação permanente enquanto tempo rodando
            st.session_state.mostrar_notificacao = True
            #Injeção dos dados
            with con.cursor() as cur:
                cur.execute("DELETE FROM sessao") # Primeiro deleta sessão anterior
                cur.execute("INSERT INTO sessao (id, hora_inicial) VALUES (1, NOW() AT TIME ZONE 'America/Sao_Paulo')") # Insere o timestamp atual
                con.commit()
            
    with col2: # SELEÇÃO DE MATÉRIA
        st.caption("Selecione sua matéria")
        tag_selecionada = st.selectbox(
            "Escolha de tag", 
            options=list(tradutorTags.keys()),
            label_visibility="collapsed",
            index=None,
            placeholder="Matéria"
        )      
    with col3: # PAUSA
        st.caption("Tempo Ocioso")
        minutos_pausa = st.number_input(
        "Ocioso", 
        min_value=0, 
        step=1,
        label_visibility="collapsed"
        )
    with col4: # STOP
        st.caption("Parar Temporizador")
        stop = st.button("Stop", use_container_width=True)
        if stop:
            if tag_selecionada is None:
                st.toast("⚠️ Escolha uma matéria antes de parar o tempo!")
            else:
                # Some com a notificação
                st.session_state.mostrar_notificacao = False
                with con.cursor() as cur:
                    try:
                        # 1. Atualiza hora final
                        cur.execute("UPDATE sessao SET hora_final = NOW() AT TIME ZONE 'America/Sao_Paulo' WHERE id = 1")
                        
                        # 2. Calcula minutos estudados
                        cur.execute("SELECT ROUND(EXTRACT(EPOCH FROM (hora_final - hora_inicial)) / 60) FROM sessao WHERE id = 1")
                        resultado = cur.fetchone()
                        if resultado:
                            minutos_estudados = max(0, int(resultado[0]))
                            tag_escolhida_id = tradutorTags[tag_selecionada]
                            # 3. Salva no log de estudo
                            cur.execute("""
                                INSERT INTO log_estudo (data, minutos, pausas_min, tag_id)
                                VALUES ((NOW() AT TIME ZONE 'America/Sao_Paulo')::date, %s, %s, %s)
                            """, (minutos_estudados, minutos_pausa, tag_escolhida_id))
                        
                            con.commit()
                            carregar_dados(con)
                            st.toast(f"🎉 Sessão finalizada! Você estudou por {minutos_estudados} minutos.")
                            time.sleep(1)
                            st.rerun()
                    except Exception as e:
                        con.rollback()
                        st.error(f"Erro ao salvar sessão de estudo: {e}")
    if st.session_state.mostrar_notificacao:
        st.info("**Temporizador Rodando!**", icon="⏱️")
    st.divider()
    
# ==========================================
# 1.1 Métricas
# ==========================================
    h_hoje, m_hoje, h_semana, m_semana, h_mes, m_mes = st.session_state.horas

    meta_semana, meta_mes = st.session_state.metas
    
# Criamos apenas as 3 colunas principais
    horas_feitas_semana, horas_feitas_hoje, horas_feitas_mes = st.columns(3, vertical_alignment="center")
    
    # --- TORRE DA ESQUERDA ---
    with horas_feitas_semana:
        st.markdown(
            f"""
            <div style="text-align: center;">
                <p style="font-size: 16px; color: #b0bec5; margin-bottom: -10px;">Horas feitas na semana</p>
                <p style="font-size: 35px; color: white; font-weight: bold; margin-top: 0px;">{h_semana}h{m_semana}min</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # O bloquinho invisível para dar o espaço entre as duas métricas
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        
        st.markdown(
            f"""
            <div style="text-align: center;">
                <p style="font-size: 16px; color: #b0bec5; margin-bottom: -10px;">Meta Semanal</p>
                <p style="font-size: 35px; color: white; font-weight: bold; margin-top: 0px;">{meta_semana}h</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    # --- TORRE DO CENTRO ---
    with horas_feitas_hoje:
        st.markdown(
            f"""
            <div style="text-align: center;">
                <p style="font-size: 18px; color: #b0bec5; margin-bottom: -15px;">Horas feitas hoje</p>
                <p style="font-size: 50px; color: #FF9800; font-weight: bold; margin-top: 0px;">{h_hoje}h{m_hoje}min</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    # --- TORRE DA DIREITA ---
    with horas_feitas_mes:
        st.markdown(
            f"""
            <div style="text-align: center;">
                <p style="font-size: 16px; color: #b0bec5; margin-bottom: -10px;">Horas feitas no mês</p>
                <p style="font-size: 35px; color: white; font-weight: bold; margin-top: 0px;">{h_mes}h{m_mes}min</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # O bloquinho invisível para manter tudo alinhado com o lado esquerdo
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        
        st.markdown(
            f"""
            <div style="text-align: center;">
                <p style="font-size: 16px; color: #b0bec5; margin-bottom: -10px;">Meta Mensal</p>
                <p style="font-size: 35px; color: white; font-weight: bold; margin-top: 0px;">{meta_mes}h</p>
            </div>
            """, 
            unsafe_allow_html=True
        )    
    st.divider() 

    # Notas
    nota_antiga = st.session_state.nota_antiga

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
        st.session_state.nota_antiga = nota_nova
        st.toast("✅ Nota salva!")

# ==========================================
# 2. ABA 2: CONFIGURAÇÕES
# ==========================================
with tab2:
    st.markdown("### Configurações")
    st.markdown("Gerencie suas matérias e defina suas metas de estudo.")
    st.write("") # Espaçamento para respirar o layout

    # ==========================================
    # CARTÃO 1: GERENCIAMENTO DE MATÉRIAS
    # ==========================================
    with st.container(border=True):
        st.markdown("#### 📚 Matérias")
        
        # Formulário independente para ADICIONAR matéria
        with st.form("form_add_materia", clear_on_submit=True, border=False):
            col_input, col_botao = st.columns([3, 1], vertical_alignment="bottom")
            
            with col_input:
                nova_materia = st.text_input(
                    "Adicionar Matéria", 
                    placeholder="Digite o nome da nova matéria...",
                    label_visibility="collapsed" 
                )
            with col_botao:
                submit_materia = st.form_submit_button("Salvar Matéria", use_container_width=True)

        # Formulário independente para EXCLUIR matéria
        with st.form("form_del_materia", clear_on_submit=False, border=False):
            col_input2, col_botao2 = st.columns([3, 1], vertical_alignment="bottom")
            
            with col_input2:
                tag_excluir = st.selectbox(
                    "Excluir Matéria", 
                    options=list(tradutorTags.keys()), 
                    placeholder="Selecione a matéria para exclusão...",
                    label_visibility="collapsed"
                )
            with col_botao2:
                submit_excluirMateria = st.form_submit_button("Excluir Matéria", use_container_width=True)
        # ==========================================
        # 2.6 Visualização de Tags
        # ==========================================
        st.markdown("###### 🏷️Tags registradas:")
        if tradutorTags:
            visualizarTags = pd.DataFrame(list(tradutorTags.keys()), columns=["tag"])
            st.dataframe(visualizarTags, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum registro encontrado ainda.")    


    # ==========================================
    # CARTÃO 2: METAS DE ESTUDO
    # ==========================================
    with st.container(border=True):
        st.markdown("#### 🎯 Metas de Estudo")
        
        # Formulário independente para METAS
        with st.form("form_metas", clear_on_submit=True, border=False):
            
            # Meta Semanal
            meta_semanal_input, meta_semanal_salvar = st.columns([3, 1], vertical_alignment="bottom")
            with meta_semanal_input:
                nova_meta_semanal = st.text_input(
                    "Meta Semanal", 
                    placeholder="Digite a meta semanal em horas (ex: 15)",
                    label_visibility="collapsed"
                )
            with meta_semanal_salvar:
                submit_meta_semanal = st.form_submit_button("Salvar Semanal", use_container_width=True)

            st.write("") # Pequeno espaço entre os inputs de meta

            # Meta Mensal
            meta_mensal_input, meta_mensal_salvar = st.columns([3, 1], vertical_alignment="bottom")
            with meta_mensal_input:
                nova_meta_mensal = st.text_input(
                    "Meta Mensal", 
                    placeholder="Digite a meta mensal em horas (ex: 60)",
                    label_visibility="collapsed"
                )
            with meta_mensal_salvar:
                submit_meta_mensal = st.form_submit_button("Salvar Mensal", use_container_width=True)
            
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
                carregar_dados(con)
                st.toast(f"✅ Matéria '{nova_materia.capitalize()}' criada com sucesso!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                con.rollback()
                st.toast(f"Erro ao salvar matéria: {e}")
            
    if submit_excluirMateria:
        if tag_excluir:
            try:
                id_excluir = tradutorTags[tag_excluir]
                with con.cursor() as cur:
                    cur.execute("DELETE FROM tags WHERE id = %s;", (id_excluir,))
                con.commit()
                carregar_dados(con)
                st.toast(f"🗑️ Matéria '{tag_excluir}' excluída!")
                time.sleep(1)
                st.rerun()
            except psycopg2.errors.ForeignKeyViolation:
                con.rollback()
                st.toast(f"❌ Não é possível excluir '{tag_excluir}' pois existem registros de estudo vinculados a ela.")
            except Exception as e:
                con.rollback()
                st.toast(f"Erro ao excluir matéria: {e}")

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
                carregar_dados(con)
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
                carregar_dados(con)
                st.toast(f"✅ Meta mensal ('{horas}h') salva com sucesso!")
                time.sleep(1)
                st.rerun()
            except ValueError:
                st.error("⚠️ Por favor, insira um número válido (apenas números).")
            except Exception as e:
                con.rollback()
                st.error(f"Erro ao salvar a meta mensal: {e}")

# ==========================================
# 3. ABA 3: Dashboard
# ==========================================

with tab3:
    st.header("📊 Dashboard")
    iframe_url=os.getenv("url_dashboard")
    st.components.v1.iframe(iframe_url, height=800, scrolling=True)