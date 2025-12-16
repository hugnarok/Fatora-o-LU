"""
Aplicação Streamlit para Resolução de Sistemas Lineares usando Decomposição LU

Interface web interativa que permite ao usuário:
- Definir a dimensão da matriz
- Inserir valores da matriz A e vetor b
- Fornecer solução esperada para comparação
- Visualizar resultados completos da decomposição LU
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from lu_decomposition import solve_system, lu_decomposition
from analysis import (
    calculate_relative_error,
    compare_solutions,
    calculate_condition_number,
    validate_solution
)

# Configuração da página
st.set_page_config(
    page_title="Decomposição LU - Sistemas Lineares",
    page_icon="🔢",
    layout="wide"
)

# Título principal
st.title("🔢 Resolução de Sistemas Lineares - Decomposição LU")
st.markdown("---")

# Sidebar com informações
with st.sidebar:
    st.header("ℹ️ Informações")
    st.markdown("""
    ### Como usar:
    1. **Defina a dimensão** da matriz (número de equações/variáveis)
    2. **Preencha a matriz A** com os coeficientes do sistema
    3. **Preencha o vetor b** com os termos independentes
    4. **Forneça a solução esperada** (opcional, para comparação)
    5. **Clique em "Resolver Sistema"** para calcular
    
    ### Sobre o método:
    A decomposição LU fatora a matriz A como:
    - **A = LU**
    - Onde L é triangular inferior e U é triangular superior
    - O sistema é resolvido em duas etapas:
      1. Ly = b (substituição forward)
      2. Ux = y (substituição backward)
    """)
    
    st.markdown("---")
    st.markdown("**Desenvolvido para:** Trabalho Final - Métodos Numéricos")

# Seção 1: Entrada de Dados
st.header("📝 Entrada de Dados")

# Entrada da dimensão
col1, col2 = st.columns([1, 3])
with col1:
    n = st.number_input(
        "Dimensão da matriz (n):",
        min_value=2,
        max_value=10,
        value=4,
        step=1,
        help="Número de equações/variáveis do sistema"
    )

st.markdown("---")

# Inicializa session state para armazenar os dados
if 'last_n' not in st.session_state:
    st.session_state.last_n = n

# Inicializa ou ajusta os arrays conforme a dimensão atual
if 'matrix_A' not in st.session_state:
    st.session_state.matrix_A = np.zeros((n, n))
if 'vector_b' not in st.session_state:
    st.session_state.vector_b = np.zeros(n)
if 'vector_expected' not in st.session_state:
    st.session_state.vector_expected = np.zeros(n)

# Atualiza dimensões se n mudou - limpa valores se dimensão diminuiu
if st.session_state.last_n != n:
    old_n = st.session_state.last_n
    
    # Se diminuiu, limpa os valores extras (mantém apenas os válidos)
    if n < old_n:
        st.session_state.matrix_A = st.session_state.matrix_A[:n, :n].copy()
        st.session_state.vector_b = st.session_state.vector_b[:n].copy()
        st.session_state.vector_expected = st.session_state.vector_expected[:n].copy()
    # Se aumentou, adiciona zeros nas novas posições
    elif n > old_n:
        new_A = np.zeros((n, n))
        new_A[:old_n, :old_n] = st.session_state.matrix_A
        st.session_state.matrix_A = new_A
        
        new_b = np.zeros(n)
        new_b[:old_n] = st.session_state.vector_b
        st.session_state.vector_b = new_b
        
        new_exp = np.zeros(n)
        new_exp[:old_n] = st.session_state.vector_expected
        st.session_state.vector_expected = new_exp
    
    st.session_state.last_n = n

# Garante que os arrays têm o tamanho correto
if st.session_state.matrix_A.shape[0] != n or st.session_state.matrix_A.shape[1] != n:
    st.session_state.matrix_A = np.zeros((n, n))
if len(st.session_state.vector_b) != n:
    st.session_state.vector_b = np.zeros(n)
if len(st.session_state.vector_expected) != n:
    st.session_state.vector_expected = np.zeros(n)

# Seção 2: Entrada da Matriz A e Vetor b lado a lado
st.subheader("Sistema Ax = b")

# Cabeçalho: Matriz A | Vetor b
header_cols = st.columns([n + 1, 1])
with header_cols[0]:
    st.markdown("**Matriz A**")
with header_cols[-1]:
    st.markdown("**Vetor b**")

# Cria campos para a matriz A e vetor b lado a lado
matrix_inputs = []
b_values = []

for i in range(n):
    # Cria n+1 colunas: n para a matriz A e 1 para o vetor b
    cols = st.columns(n + 1)
    row_values = []
    
    # Campos da matriz A (primeiras n colunas)
    for j in range(n):
        with cols[j]:
            key = f"A_{i}_{j}"
            # Usa valor do session_state se estiver dentro dos limites
            if i < st.session_state.matrix_A.shape[0] and j < st.session_state.matrix_A.shape[1]:
                value_A = float(st.session_state.matrix_A[i, j])
            else:
                value_A = 0.0
            value = st.number_input(
                f"A[{i+1},{j+1}]",
                value=value_A,
                key=key,
                format="%.6f",
                label_visibility="visible"
            )
            row_values.append(value)
    
    # Campo do vetor b (última coluna)
    with cols[-1]:
        key = f"b_{i}"
        if i < len(st.session_state.vector_b):
            value_b = float(st.session_state.vector_b[i])
        else:
            value_b = 0.0
        value = st.number_input(
            f"b[{i+1}]",
            value=value_b,
            key=key,
            format="%.6f",
            label_visibility="visible"
        )
        b_values.append(value)
    
    matrix_inputs.append(row_values)

st.session_state.matrix_A = np.array(matrix_inputs)
st.session_state.vector_b = np.array(b_values)

# Exibe a matriz A e vetor b formatados lado a lado
display_cols = st.columns([n + 1, 1])
with display_cols[0]:
    st.markdown("**Matriz A:**")
    st.dataframe(st.session_state.matrix_A, use_container_width=True)

with display_cols[-1]:
    st.markdown("**Vetor b:**")
    st.dataframe(st.session_state.vector_b.reshape(-1, 1), use_container_width=True)

st.markdown("---")

# Seção 4: Solução Esperada (opcional)
st.subheader("Solução Esperada (para comparação)")

exp_cols = st.columns(n)
exp_values = []
for i in range(n):
    with exp_cols[i]:
        key = f"expected_{i}"
        if i < len(st.session_state.vector_expected):
            value_exp = float(st.session_state.vector_expected[i])
        else:
            value_exp = 0.0
        value = st.number_input(
            f"x_esperado[{i+1}]",
            value=value_exp,
            key=key,
            format="%.6f"
        )
        exp_values.append(value)

st.session_state.vector_expected = np.array(exp_values)

if np.any(st.session_state.vector_expected != 0):
    st.markdown("**Solução Esperada:**")
    st.dataframe(st.session_state.vector_expected.reshape(-1, 1), use_container_width=True)

st.markdown("---")

# Botão para resolver
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    solve_button = st.button("🚀 Resolver Sistema", type="primary", use_container_width=True)

# Seção 5: Resultados
if solve_button:
    st.markdown("---")
    st.header("📊 Resultados")
    
    try:
        # Resolve o sistema
        with st.spinner("Calculando decomposição LU e resolvendo o sistema..."):
            x_calc, L, U = solve_system(st.session_state.matrix_A, st.session_state.vector_b)
        
        # Exibe as matrizes L e U
        st.subheader("Decomposição LU")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Matriz L (Triangular Inferior):**")
            st.dataframe(L, use_container_width=True)
        
        with col2:
            st.markdown("**Matriz U (Triangular Superior):**")
            st.dataframe(U, use_container_width=True)
        
        # Verifica se L * U = A
        st.markdown("**Validação: L × U = A**")
        LU_product = np.dot(L, U)
        st.dataframe({
            "Original A": st.session_state.matrix_A.flatten(),
            "L × U": LU_product.flatten(),
            "Diferença": (st.session_state.matrix_A - LU_product).flatten()
        }, use_container_width=True)
        
        st.markdown("---")
        
        # Solução calculada
        st.subheader("Solução Calculada")
        st.dataframe(x_calc.reshape(-1, 1), use_container_width=True)
        
        # Validação da solução
        is_valid, residuo, max_residuo = validate_solution(
            st.session_state.matrix_A, 
            x_calc, 
            st.session_state.vector_b
        )
        
        st.markdown(f"**Validação:** {'✅ Solução válida' if is_valid else '⚠️ Solução com resíduo alto'}")
        st.markdown(f"**Máximo resíduo:** {max_residuo:.2e}")
        
        st.markdown("---")
        
        # Erro relativo
        st.subheader("Análise de Erro")
        erro_relativo = calculate_relative_error(
            st.session_state.matrix_A,
            x_calc,
            st.session_state.vector_b
        )
        
        st.metric("Erro Relativo (ε)", f"{erro_relativo:.2e}")
        st.markdown("ε = ||Ax_calc - b|| / ||b||")
        
        # Número de condicionamento
        cond_num = calculate_condition_number(st.session_state.matrix_A)
        st.metric("Número de Condicionamento", f"{cond_num:.2e}")
        
        if cond_num > 1e12:
            st.warning("⚠️ Matriz muito mal condicionada! Resultados podem ser imprecisos.")
        elif cond_num > 1e8:
            st.info("ℹ️ Matriz mal condicionada. Resultados podem ter alguma imprecisão.")
        
        st.markdown("---")
        
        # Comparação com solução esperada (se fornecida)
        if np.any(st.session_state.vector_expected != 0):
            st.subheader("Comparação com Solução Esperada")
            
            comparacao = compare_solutions(x_calc, st.session_state.vector_expected)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Solução Calculada:**")
                st.dataframe(x_calc.reshape(-1, 1), use_container_width=True)
            
            with col2:
                st.markdown("**Solução Esperada:**")
                st.dataframe(st.session_state.vector_expected.reshape(-1, 1), use_container_width=True)
            
            st.markdown("**Diferença (x_calc - x_esperado):**")
            st.dataframe(comparacao['difference'].reshape(-1, 1), use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Erro Absoluto", f"{comparacao['absolute_error']:.2e}")
            with col2:
                st.metric("Erro Relativo", f"{comparacao['relative_error']:.2e}")
            with col3:
                st.metric("Máximo Erro", f"{comparacao['max_error']:.2e}")
            
            # Gráfico comparativo
            st.markdown("---")
            st.subheader("Visualização Comparativa")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            indices = np.arange(1, n + 1)
            width = 0.35
            
            ax.bar(indices - width/2, x_calc, width, label='Solução Calculada', alpha=0.8)
            ax.bar(indices + width/2, st.session_state.vector_expected, width, 
                   label='Solução Esperada', alpha=0.8)
            
            ax.set_xlabel('Componente')
            ax.set_ylabel('Valor')
            ax.set_title('Comparação: Solução Calculada vs Esperada')
            ax.set_xticks(indices)
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
        
        # Resumo final
        st.markdown("---")
        st.subheader("📋 Resumo")
        
        summary_data = {
            "Dimensão": [n],
            "Erro Relativo (ε)": [f"{erro_relativo:.2e}"],
            "Condicionamento": [f"{cond_num:.2e}"],
            "Solução Válida": ["Sim" if is_valid else "Não"]
        }
        
        if np.any(st.session_state.vector_expected != 0):
            summary_data["Erro Relativo vs Esperado"] = [f"{comparacao['relative_error']:.2e}"]
        
        st.dataframe(summary_data, use_container_width=True)
        
    except ValueError as e:
        st.error(f"❌ Erro: {str(e)}")
        st.info("Verifique se a matriz A é não-singular e bem condicionada.")
    except Exception as e:
        st.error(f"❌ Erro inesperado: {str(e)}")
        st.exception(e)

# Rodapé
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Métodos Numéricos - Decomposição LU | Trabalho Final"
    "</div>",
    unsafe_allow_html=True
)

