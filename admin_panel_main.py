# admin_panel_main.py (PONTO DE ENTRADA E AUTENTICAÇÃO)

import streamlit as st
# A única importação que precisamos do nosso código é a função de autenticação
from shared_funcs import check_admin_auth

# Configuração da página - deve ser o primeiro comando Streamlit
st.set_page_config(layout="wide", page_title="Painel de Gestão Escriba AI")

# --- INICIALIZAÇÃO DA SESSÃO ---
# Usamos esta estrutura para garantir que as variáveis de sessão só sejam criadas uma vez
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

# NOTA: Os outros 'session_state' que você tinha são específicos de outras páginas.
# O ideal é que cada página gerencie seu próprio estado, mas não há problema em mantê-los aqui
# para simplificar. Vamos deixá-los por enquanto.
if 'new_api_key_info' not in st.session_state:
    st.session_state.new_api_key_info = None
if 'confirm_action' not in st.session_state:
    st.session_state.confirm_action = None
if 'last_perm_account_id' not in st.session_state:
    st.session_state.last_perm_account_id = None
if 'billing_report_data' not in st.session_state:
    st.session_state.billing_report_data = None


# --- TELA DE LOGIN / PROTEÇÃO ---
# Se o usuário não estiver autenticado, mostramos a tela de login e paramos a execução.
if not st.session_state.is_authenticated:
    st.title("Acesso ao Painel de Gestão - Escriba AI")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        api_key_input = st.text_input(
            "Chave de API de Administrador:", 
            type="password", 
            key="login_api_key",
            label_visibility="collapsed",
            placeholder="Insira sua chave de API de administrador"
        )
        if st.button("Entrar", use_container_width=True, type="primary"):
            # A função check_admin_auth agora vem do nosso arquivo centralizado
            if check_admin_auth(api_key_input):
                st.session_state.is_authenticated = True
                st.session_state.api_key = api_key_input
                st.rerun()  # Recarrega a página para mostrar o conteúdo protegido
            else:
                st.error("Chave de API inválida ou sem permissão de administrador.")
    
    st.stop() # Interrompe a renderização do resto da página

# --- CONTEÚDO EXIBIDO APÓS O LOGIN ---

# Função para limpar a sessão e deslogar o usuário
def logout():
    # Apaga todas as chaves da sessão para garantir um logout completo
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Configuração da Barra Lateral (Sidebar)
st.sidebar.title("Navegação")
st.sidebar.button("Sair (Logout)", on_click=logout, use_container_width=True)
st.sidebar.header("Módulos")

# Título e mensagem de boas-vindas na página principal
st.title("Painel de Gestão - Escriba AI")
st.markdown("### Bem-vindo!")
st.info("Selecione um módulo na barra lateral à esquerda para começar a gerenciar o sistema.", icon="👈")
