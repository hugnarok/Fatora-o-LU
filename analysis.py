"""
Módulo de Análise e Comparação de Resultados

Implementa funções para análise de resultados, cálculo de erros
e comparação de soluções.
"""

import numpy as np


def vector_norm(v, p=2):
    """
    Calcula a norma de um vetor.
    
    Args:
        v: Vetor numpy
        p: Ordem da norma (padrão: 2 para norma euclidiana)
        
    Returns:
        float: Norma do vetor
    """
    v = np.array(v, dtype=float).flatten()
    return np.linalg.norm(v, ord=p)


def calculate_relative_error(A, x_calc, b):
    """
    Calcula o erro relativo: ε = ||Ax_calc - b|| / ||b||
    
    Este erro mede a qualidade da solução calculada comparando
    o resultado de Ax_calc com o vetor b original.
    
    Args:
        A: Matriz dos coeficientes (n x n)
        x_calc: Solução calculada (n x 1)
        b: Vetor do lado direito original (n x 1)
        
    Returns:
        float: Erro relativo ε
    """
    A = np.array(A, dtype=float)
    x_calc = np.array(x_calc, dtype=float).flatten()
    b = np.array(b, dtype=float).flatten()
    
    # Calcula Ax_calc
    Ax_calc = np.dot(A, x_calc)
    
    # Calcula o resíduo: Ax_calc - b
    residuo = Ax_calc - b
    
    # Calcula as normas
    norm_residuo = vector_norm(residuo)
    norm_b = vector_norm(b)
    
    # Evita divisão por zero
    if norm_b < 1e-10:
        return norm_residuo
    
    # Erro relativo
    erro_relativo = norm_residuo / norm_b
    
    return erro_relativo


def compare_solutions(x_calc, x_expected):
    """
    Compara a solução calculada com a solução esperada.
    
    Args:
        x_calc: Solução calculada (n x 1)
        x_expected: Solução esperada (n x 1)
        
    Returns:
        dict: Dicionário com informações da comparação:
            - 'difference': Diferença entre as soluções
            - 'absolute_error': Erro absoluto ||x_calc - x_expected||
            - 'relative_error': Erro relativo ||x_calc - x_expected|| / ||x_expected||
            - 'max_error': Máximo erro absoluto por componente
    """
    x_calc = np.array(x_calc, dtype=float).flatten()
    x_expected = np.array(x_expected, dtype=float).flatten()
    
    # Diferença entre as soluções
    diferenca = x_calc - x_expected
    
    # Erro absoluto
    erro_absoluto = vector_norm(diferenca)
    
    # Erro relativo
    norm_esperada = vector_norm(x_expected)
    if norm_esperada < 1e-10:
        erro_relativo = erro_absoluto
    else:
        erro_relativo = erro_absoluto / norm_esperada
    
    # Máximo erro por componente
    max_erro = np.max(np.abs(diferenca))
    
    return {
        'difference': diferenca,
        'absolute_error': erro_absoluto,
        'relative_error': erro_relativo,
        'max_error': max_erro
    }


def calculate_condition_number(A):
    """
    Calcula o número de condicionamento da matriz A.
    
    O número de condicionamento mede a sensibilidade da solução
    a pequenas perturbações nos dados. Valores grandes indicam
    sistemas mal condicionados.
    
    Args:
        A: Matriz dos coeficientes (n x n)
        
    Returns:
        float: Número de condicionamento cond(A)
    """
    A = np.array(A, dtype=float)
    try:
        cond_num = np.linalg.cond(A)
        return cond_num
    except np.linalg.LinAlgError:
        return np.inf


def validate_solution(A, x, b, tolerance=1e-6):
    """
    Valida se a solução x satisfaz o sistema Ax = b dentro de uma tolerância.
    
    Args:
        A: Matriz dos coeficientes (n x n)
        x: Solução (n x 1)
        b: Vetor do lado direito (n x 1)
        tolerance: Tolerância para validação (padrão: 1e-6)
        
    Returns:
        tuple: (is_valid, residuo, max_residuo) onde:
            - is_valid: True se a solução é válida
            - residuo: Vetor resíduo Ax - b
            - max_residuo: Máximo valor absoluto do resíduo
    """
    A = np.array(A, dtype=float)
    x = np.array(x, dtype=float).flatten()
    b = np.array(b, dtype=float).flatten()
    
    # Calcula Ax
    Ax = np.dot(A, x)
    
    # Calcula o resíduo
    residuo = Ax - b
    
    # Máximo resíduo
    max_residuo = np.max(np.abs(residuo))
    
    # Validação
    is_valid = max_residuo < tolerance
    
    return is_valid, residuo, max_residuo

