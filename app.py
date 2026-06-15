import streamlit as st
import sqlite3
from datetime import datetime
import time
import pandas as pd
import os
from metodos.database import iniciar_conexao, criar_tabelas, obter_tags
from metodos.horas_e_metas import agregar_horas, extrair_metas
from assets.utils import img_to_base64

ICON_PATH = "assets/icon.png"

st.set_page_config(page_title="Stude", page_icon=ICON_PATH, layout="centered")

# Título com ícone customizado
icon_base64 = img_to_base64(ICON_PATH)
st.markdown(f"""
<div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px; margin-top: -20px;">
    <img src="data:image/png;base64,{icon_base64}" width="45" style="border-radius: 8px;">
    <h1 style="margin: 0; padding: 0; font-size: 2.2rem;">Stude</h1>
</div>
""", unsafe_allow_html=True)
# CSS customizado (arquivo externo)
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
con = iniciar_conexao()
try:
    con.rollback() # Limpa qualquer transação falha residual
except:
    pass

def carregar_dados(conexao):
    st.session_state.tradutorTags = obter_tags(conexao)
    st.session_state.horas = agregar_horas(conexao)
    st.session_state.metas = extrair_metas(conexao)
    cur = conexao.cursor()
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
        start = st.button("Start", use_container_width=True, type="primary") 
        if start:
            # Notificação permanente enquanto tempo rodando
            st.session_state.mostrar_notificacao = True
            #Injeção dos dados
            cur = con.cursor()
            cur.execute("DELETE FROM sessao") # Primeiro deleta sessão anterior
            agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cur.execute("INSERT INTO sessao (id, hora_inicial) VALUES (1, ?)", (agora,)) # Insere o timestamp atual
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
        st.markdown('<span class="red-button-marker"></span><p style="font-size: 0.875rem; color: rgba(250,250,250,0.6); margin-bottom: 0;">Parar Temporizador</p>', unsafe_allow_html=True)
        stop = st.button("Stop", use_container_width=True)
        if stop:
            if tag_selecionada is None:
                st.toast("⚠️ Escolha uma matéria antes de parar o tempo!")
            else:
                st.session_state.mostrar_notificacao = False
                try:
                    cur = con.cursor()
                    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cur.execute("UPDATE sessao SET hora_final = ? WHERE id = 1", (agora,))
                    cur.execute("SELECT ROUND((julianday(hora_final) - julianday(hora_inicial)) * 24 * 60) FROM sessao WHERE id = 1")
                    resultado = cur.fetchone()
                    if resultado and resultado[0] is not None:
                        minutos_estudados = max(0, int(resultado[0]))
                        tag_escolhida_id = tradutorTags[tag_selecionada]
                        data_hoje = datetime.now().strftime('%Y-%m-%d')
                        cur.execute(
                            "INSERT INTO log_estudo (data, minutos, pausas_min, tag_id) VALUES (?, ?, ?, ?)",
                            (data_hoje, minutos_estudados, minutos_pausa, tag_escolhida_id)
                        )
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
    h_hoje, m_hoje, h_semana, m_semana, h_mes, m_mes, h_semana_a, m_semana_a = st.session_state.horas

    meta_semana, meta_mes = st.session_state.metas
    
# Linha superior: Semana Anterior | Semana | Mês
    horas_feitas_semana_anterior, horas_feitas_semana, horas_feitas_mes = st.columns(3, vertical_alignment="center")
    
    # --- Semana Anterior ---
    with horas_feitas_semana_anterior:
        st.markdown(
            f"""
            <div style="text-align: center;">
                <p style="font-size: 16px; color: #b0bec5; margin-bottom: -10px;">Horas feitas na semana anterior</p>
                <p style="font-size: 35px; color: white; font-weight: bold; margin-top: 0px;">{h_semana_a}h{m_semana_a}min</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    # --- Semana ---
    with horas_feitas_semana:
        st.markdown(
            f"""
            <div style="text-align: center;">
                <p style="font-size: 18px; color: #b0bec5; margin-bottom: -15px;">Horas feitas na semana</p>
                <p style="font-size: 50px; color: #00BFA5; font-weight: bold; margin-top: 0px;">{h_semana}h{m_semana}min</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    # --- Mês ---
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

    # Espaço entre as linhas de métricas
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Linha inferior: Meta Semanal | Horas feitas hoje | Meta Mensal
    col_meta_semana, col_hoje, col_meta_mes = st.columns(3, vertical_alignment="center")
    with col_meta_semana:
        st.markdown(
            f"""
            <div style="text-align: center;">
                <p style="font-size: 16px; color: #b0bec5; margin-bottom: -10px;">Meta Semanal</p>
                <p style="font-size: 35px; color: white; font-weight: bold; margin-top: 0px;">{meta_semana}h</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    with col_hoje:
        st.markdown(
            f"""
            <div style="text-align: center;">
                <p style="font-size: 18px; color: #b0bec5; margin-bottom: -15px;">Horas feitas hoje</p>
                <p style="font-size: 50px; color: #FF9800; font-weight: bold; margin-top: 0px;">{h_hoje}h{m_hoje}min</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    with col_meta_mes:
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
        cur = con.cursor()
        cur.execute("UPDATE notas SET texto = ? WHERE id = 1;", (nota_nova,))
        con.commit()
        st.session_state.nota_antiga = nota_nova
        st.toast("✅ Nota salva!")

# ==========================================
# 2. ABA 2: CONFIGURAÇÕES
# ==========================================
with tab2:
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
                submit_materia = st.form_submit_button("Salvar Matéria", use_container_width=True, type="primary")

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
                st.markdown('<span class="red-button-marker"></span>', unsafe_allow_html=True)
                submit_excluirMateria = st.form_submit_button("Excluir Matéria", use_container_width=True)
        # ==========================================
        # 2.6 Visualização de Tags
        # ==========================================
        st.markdown("##### 🏷️Tags registradas:")
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
            nova_meta_semanal = st.text_input(
                "Meta Semanal", 
                placeholder="Digite a meta semanal em horas (ex: 15)"
            )

            # Meta Mensal
            nova_meta_mensal = st.text_input(
                "Meta Mensal", 
                placeholder="Digite a meta mensal em horas (ex: 60)"
            )

            submit_metas = st.form_submit_button("Salvar Metas", use_container_width=True, type="primary")
            
    # =================================================
    # 2.4 Condicionais de Criação e Exclusão de Matéria
    # =================================================
    if submit_materia:
        if nova_materia.strip() == "":
            st.warning("⚠️ O nome da matéria não pode ser vazio!")
        else:
            try:
                cur = con.cursor()
                cur.execute("""
                    INSERT INTO tags (tag) 
                    VALUES (?);
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
                cur = con.cursor()
                cur.execute("DELETE FROM tags WHERE id = ?;", (id_excluir,))
                con.commit()
                carregar_dados(con)
                st.toast(f"🗑️ Matéria '{tag_excluir}' excluída!")
                time.sleep(1)
                st.rerun()
            except sqlite3.IntegrityError:
                con.rollback()
                st.toast(f"❌ Não é possível excluir '{tag_excluir}' pois existem registros de estudo vinculados a ela.")
            except Exception as e:
                con.rollback()
                st.toast(f"Erro ao excluir matéria: {e}")

    # ==================================================
    # 2.5 Condicionais de Criação e Atualização de Metas
    # ==================================================

    if submit_metas:
        tem_semanal = nova_meta_semanal.strip() != ""
        tem_mensal = nova_meta_mensal.strip() != ""

        if not tem_semanal and not tem_mensal:
            st.warning("⚠️ Preencha pelo menos uma meta!")
        else:
            try:
                cur = con.cursor()
                if tem_semanal:
                    horas_sem = int(nova_meta_semanal)
                    cur.execute("SELECT 1 FROM metas WHERE tipo_meta = 'semanal'")
                    if cur.fetchone():
                        cur.execute("UPDATE metas SET horas_alvo = ? WHERE tipo_meta = 'semanal'", (horas_sem,))
                    else:
                        cur.execute("INSERT INTO metas (tipo_meta, horas_alvo) VALUES ('semanal', ?)", (horas_sem,))

                if tem_mensal:
                    horas_men = int(nova_meta_mensal)
                    cur.execute("SELECT 1 FROM metas WHERE tipo_meta = 'mensal'")
                    if cur.fetchone():
                        cur.execute("UPDATE metas SET horas_alvo = ? WHERE tipo_meta = 'mensal'", (horas_men,))
                    else:
                        cur.execute("INSERT INTO metas (tipo_meta, horas_alvo) VALUES ('mensal', ?)", (horas_men,))

                con.commit()
                carregar_dados(con)
                st.toast("✅ Metas salvas com sucesso!")
                time.sleep(1)
                st.rerun()
            except ValueError:
                st.error("⚠️ Por favor, insira apenas números válidos.")
            except Exception as e:
                con.rollback()
                st.error(f"Erro ao salvar as metas: {e}")

# ==========================================
# 3. ABA 3: Dashboard
# ==========================================

with tab3:
    st.header("📊 Dashboard")
    iframe_url = os.getenv("url_dashboard", "")
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("url_dashboard="):
                    iframe_url = line.strip().split("=", 1)[1]
                    break

    st.components.v1.html(
        f"""
        <iframe
            src="{iframe_url}"
            width="100%"
            height="750"
            frameborder="0"
            style="border: none; border-radius: 8px;"
            allowfullscreen
        ></iframe>
        """,
        height=750
    )