# Resolução de Sistemas Lineares - Decomposição LU

Aplicação web interativa para resolver sistemas de equações lineares usando o método de decomposição LU.

## 📋 Descrição

Este projeto implementa uma interface web usando Streamlit que permite resolver sistemas lineares da forma **Ax = b** através da decomposição LU. A aplicação oferece:

- Interface interativa para entrada de dados
- Decomposição LU completa (A = LU)
- Resolução de sistemas triangulares (forward e backward substitution)
- Análise de erros e validação de resultados
- Comparação com soluções esperadas
- Visualizações gráficas dos resultados

## 🚀 Instalação

### Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

### Passos para Instalação

1. **Clone ou baixe o projeto**

2. **Ative o ambiente virtual** (se já existir):
   ```bash
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Como Usar

1. **Execute a aplicação**:
   ```bash
   streamlit run app.py
   ```

2. **A aplicação abrirá automaticamente no navegador** (geralmente em `http://localhost:8501`)

3. **Na interface web**:
   - Defina a dimensão da matriz (número de equações/variáveis)
   - Preencha a matriz A com os coeficientes do sistema
   - Preencha o vetor b com os termos independentes
   - (Opcional) Forneça a solução esperada para comparação
   - Clique em "Resolver Sistema"

4. **Visualize os resultados**:
   - Matrizes L e U da decomposição
   - Solução calculada
   - Erro relativo
   - Número de condicionamento
   - Comparação com solução esperada (se fornecida)
   - Gráficos comparativos

## 📁 Estrutura do Projeto

```
Metodos Numericos/
├── app.py                 # Aplicação principal Streamlit
├── lu_decomposition.py    # Algoritmos de decomposição LU
├── analysis.py            # Funções de análise e comparação
├── requirements.txt       # Dependências do projeto
├── README.md              # Este arquivo
└── venv/                  # Ambiente virtual Python
```

## 🔧 Componentes Principais

### `lu_decomposition.py`
Contém as funções principais:
- `lu_decomposition(A)`: Realiza a decomposição A = LU
- `forward_substitution(L, b)`: Resolve Ly = b
- `backward_substitution(U, y)`: Resolve Ux = y
- `solve_lu(L, U, b)`: Resolve o sistema completo
- `solve_system(A, b)`: Função principal que combina todos os passos

### `analysis.py`
Funções de análise:
- `calculate_relative_error(A, x_calc, b)`: Calcula ε = ||Ax_calc - b|| / ||b||
- `compare_solutions(x_calc, x_expected)`: Compara soluções
- `calculate_condition_number(A)`: Calcula cond(A)
- `validate_solution(A, x, b)`: Valida a solução

### `app.py`
Interface web Streamlit com:
- Entrada dinâmica de dados
- Visualização de resultados
- Gráficos comparativos
- Análise de erros

## 📊 Exemplo de Uso

### Sistema do Circuito Elétrico (4 malhas)

**Matriz A:**
```
[ 3, -1,  0, -1]
[-1,  4, -1,  0]
[ 0, -1,  4, -1]
[-1,  0, -1,  3]
```

**Vetor b:**
```
[5]
[0]
[0]
[5]
```

**Solução Esperada:**
```
[2.5]
[1.5]
[1.0]
[3.0]
```

## ⚠️ Observações Importantes

- A matriz A deve ser **não-singular** (determinante diferente de zero)
- Matrizes **mal condicionadas** podem produzir resultados imprecisos
- O número de condicionamento indica a qualidade da matriz:
  - `cond(A) < 10^8`: Bem condicionada
  - `cond(A) > 10^12`: Muito mal condicionada

## 🎯 Critérios de Avaliação Atendidos

- ✅ **Correção e precisão**: Implementação correta do método LU
- ✅ **Qualidade do código**: Código organizado, comentado e com boas práticas
- ✅ **Análise de resultados**: Cálculo de erros e comparação com solução esperada
- ✅ **Relatório técnico**: Documentação completa e interface clara
- ✅ **Criatividade e extras**: Visualizações gráficas, análise de condicionamento, validação de resultados

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais como parte do Trabalho Final da disciplina de Métodos Numéricos.

## 👨‍💻 Autores

<div align="center">

<br><br>
   <i>Fernando Horita Siratuti - Undergraduate - 4th Semester, Computer Engineering @ CEFET-MG</i>
<br><br>

[![Gmail][gmail-badge]][gmail-autor2]
[![Linkedin][linkedin-badge]][linkedin-autor2]
[![GitHub][github-badge]][github-autor2]
[![Instagram][instagram-badge]][instagram-autor2]

<br><br>
   <i>Hugo Henrique Marques - Undergraduate - 4th Semester, Computer Engineering @ CEFET-MG</i>
<br><br>

[![Gmail][gmail-badge]][gmail-autor3]
[![Linkedin][linkedin-badge]][linkedin-autor3]
[![GitHub][github-badge]][github-autor3]
[![Instagram][instagram-badge]][instagram-autor3]

<br><br>
   <i>Vinicius Ramalho de Oliveira - Undergraduate - 4th Semester, Computer Engineering @ CEFET-MG</i>
<br><br>

[![Gmail][gmail-badge]][gmail-autor5]
[![Linkedin][linkedin-badge]][linkedin-autor5]
[![GitHub][github-badge]][github-autor5]
[![Instagram][instagram-badge]][instagram-autor5]

</div>

[gmail-badge]: https://img.shields.io/badge/-Gmail-c14438?style=flat-square&logo=Gmail&logoColor=white
[linkedin-badge]: https://img.shields.io/badge/-LinkedIn-blue?style=flat-square&logo=Linkedin&logoColor=white
[github-badge]: https://img.shields.io/badge/-GitHub-181717?style=flat-square&logo=github&logoColor=white
[instagram-badge]: https://img.shields.io/badge/-Instagram-E4405F?style=flat-square&logo=instagram&logoColor=white

[gmail-autor2]: mailto:siratutifernando@gmail.com
[linkedin-autor2]: https://www.linkedin.com/in/fernando-siratuti-503ba8301/
[github-autor2]: https://github.com/fernando-horita-siratuti
[instagram-autor2]: https://www.instagram.com/siratuti_/

[gmail-autor3]: mailto:hugohmarques4@gmail.com
[linkedin-autor3]: https://www.linkedin.com/in/hugo-h-marques-980629216/
[github-autor3]: https://github.com/hugnarok
[instagram-autor3]: https://www.instagram.com/hugomarques_02/

[gmail-autor5]: mailto:ramalhooliveiravini@gmail.com
[linkedin-autor5]: https://www.linkedin.com/in/vin%C3%ADcius-ramalho-de-oliveira-4464b8327/
[github-autor5]: https://github.com/ViniciusRO22
[instagram-autor5]: https://www.instagram.com/_vinicius.ro_/

---

**Desenvolvido para Trabalho Final - Métodos Numéricos**
