"""
Módulo de Decomposição LU para Sistemas Lineares

Implementa os algoritmos de decomposição LU, substituição forward/backward
e resolução completa de sistemas lineares Ax = b.
"""

import numpy as np


def lu_decomposition(A):
    """
    Realiza a decomposição LU da matriz A usando eliminação de Gauss.
    
    A decomposição LU fatora a matriz A como A = LU, onde:
    - L é uma matriz triangular inferior com diagonal unitária
    - U é uma matriz triangular superior
    
    Args:
        A: Matriz quadrada numpy (n x n)
        
    Returns:
        tuple: (L, U) onde L é triangular inferior e U é triangular superior
        
    Raises:
        ValueError: Se a matriz for singular ou não quadrada
    """
    A = np.array(A, dtype=float)
    n = A.shape[0]
    
    if A.shape[0] != A.shape[1]:
        raise ValueError("A matriz deve ser quadrada")
    
    # Inicializa L como matriz identidade e U como cópia de A
    L = np.eye(n)
    U = A.copy()
    
    # Eliminação de Gauss com pivotamento parcial implícito
    for k in range(n - 1):
        # Verifica se o pivô é zero (matriz singular)
        if abs(U[k, k]) < 1e-10:
            raise ValueError(f"Matriz singular ou mal condicionada. Pivô zero na posição ({k}, {k})")
        
        # Para cada linha abaixo da diagonal
        for i in range(k + 1, n):
            # Calcula o multiplicador
            multiplier = U[i, k] / U[k, k]
            
            # Armazena o multiplicador em L
            L[i, k] = multiplier
            
            # Elimina o elemento abaixo do pivô
            for j in range(k, n):
                U[i, j] -= multiplier * U[k, j]
    
    # Verifica se o último pivô é zero
    if abs(U[n-1, n-1]) < 1e-10:
        raise ValueError("Matriz singular ou mal condicionada")
    
    return L, U


def forward_substitution(L, b):
    """
    Resolve o sistema triangular inferior Ly = b usando substituição forward.
    
    Args:
        L: Matriz triangular inferior (n x n) com diagonal unitária
        b: Vetor do lado direito (n x 1)
        
    Returns:
        numpy.ndarray: Vetor solução y
    """
    L = np.array(L, dtype=float)
    b = np.array(b, dtype=float).flatten()
    n = len(b)
    
    y = np.zeros(n)
    
    # Primeira equação: y[0] = b[0] / L[0, 0]
    # Como L tem diagonal unitária, L[0, 0] = 1
    y[0] = b[0]
    
    # Para as demais equações
    for i in range(1, n):
        soma = 0.0
        for j in range(i):
            soma += L[i, j] * y[j]
        y[i] = b[i] - soma
    
    return y


def backward_substitution(U, y):
    """
    Resolve o sistema triangular superior Ux = y usando substituição backward.
    
    Args:
        U: Matriz triangular superior (n x n)
        y: Vetor do lado direito (n x 1)
        
    Returns:
        numpy.ndarray: Vetor solução x
    """
    U = np.array(U, dtype=float)
    y = np.array(y, dtype=float).flatten()
    n = len(y)
    
    x = np.zeros(n)
    
    # Última equação: x[n-1] = y[n-1] / U[n-1, n-1]
    x[n-1] = y[n-1] / U[n-1, n-1]
    
    # Para as demais equações (de baixo para cima)
    for i in range(n - 2, -1, -1):
        soma = 0.0
        for j in range(i + 1, n):
            soma += U[i, j] * x[j]
        x[i] = (y[i] - soma) / U[i, i]
    
    return x


def solve_lu(L, U, b):
    """
    Resolve o sistema Ax = b usando a decomposição LU.
    
    Primeiro resolve Ly = b (substituição forward),
    depois resolve Ux = y (substituição backward).
    
    Args:
        L: Matriz triangular inferior (n x n)
        U: Matriz triangular superior (n x n)
        b: Vetor do lado direito (n x 1)
        
    Returns:
        numpy.ndarray: Vetor solução x
    """
    # Resolve Ly = b
    y = forward_substitution(L, b)
    
    # Resolve Ux = y
    x = backward_substitution(U, y)
    
    return x


def solve_system(A, b):
    """
    Resolve o sistema Ax = b usando decomposição LU completa.
    
    Esta função combina todos os passos:
    1. Decomposição A = LU
    2. Resolução do sistema usando substituições
    
    Args:
        A: Matriz dos coeficientes (n x n)
        b: Vetor do lado direito (n x 1)
        
    Returns:
        tuple: (x, L, U) onde x é a solução, L e U são as matrizes da decomposição
    """
    L, U = lu_decomposition(A)
    x = solve_lu(L, U, b)
    return x, L, U

