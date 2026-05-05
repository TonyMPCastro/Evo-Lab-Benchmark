# Evo-Lab-Benchmark

**Plataforma de Benchmark para Algoritmos de Otimização Bio-inspirados**

Este projeto é desenvolvido para um Trabalho de Conclusão de Curso (TCC) e consiste em uma suíte de benchmark com nível acadêmico para avaliação e comparação rigorosa de algoritmos de otimização bio-inspirados (meta-heurísticas).

## 🎯 Objetivo

Fornecer um ambiente de testes robusto e profissional para validar algoritmos clássicos e modernos, utilizando padrões reconhecidos mundialmente pela academia (como o IEEE CEC) e aplicando-os em cenários de otimização do mundo real, como Ciência de Dados e Engenharia.

## 🧬 Algoritmos Analisados

*   **Clássicos (Padrão da Indústria):**
    *   **PSO** (Particle Swarm Optimization)
    *   **ACO** (Ant Colony Optimization)
    *   **GWO** (Grey Wolf Optimizer)
    *   **ALO** (Ant Lion Optimizer)
    *   **WOA** (Whale Optimization Algorithm)
    *   **BWO** (Beluga Whale Optimization)
*   **Híbridos com Inteligência Artificial (2024–2026):**
    *   **DRL-MORIME** (Deep Reinforcement Learning Meta-heuristic)
    *   **DRL-BWO** (Deep Reinforcement Learning + Beluga Whale Optimization)
    *   **QL-GWO** (Q-Learning Grey Wolf Optimizer)

## 🧪 Metodologia de Testes e Aplicações

1.  **Baterias de Funções Benchmark Matemáticas:** Testes de explotação (funções unimodais como Esfera) e exploração (funções multimodais como Ackley e Rastrigin) para medir velocidade de convergência e inteligência de fuga de ótimos locais.
2.  **Ciência de Dados e Machine Learning:**
    *   *Feature Selection* (Seleção de Características): Minimização de variáveis mantendo alta acurácia do classificador.
    *   *Sintonia de Hiperparâmetros*: Otimização de parâmetros de Redes Neurais e outros modelos.
3.  **Engenharia e Controle:** Sintonia de Controladores PID visando minimizar o erro (como RMSE) e melhorar estabilidade e *rise time*.

## 📊 Visualizações e Métricas

A plataforma gera visualizações modernas e prontas para publicação acadêmica:
*   **Gráficos de Convergência:** Com bandas de erro e eixo Y em escala logarítmica.
*   **Trajetórias em Contorno 2D:** Visualização do mapa de busca dos agentes.
*   **Gráficos de Resposta ao Degrau:** Para simulação em engenharia.
*   **Análise Estatística:** Validação não-paramétrica (como teste de Wilcoxon) pós 30+ execuções independentes, garantindo rigor científico.

## 🚀 Como Executar

O projeto foi construído em Python. A execução principal e visualizações se encontram no Jupyter Notebook incluído no repositório.

1. Clone o repositório.
2. Abra e execute as células do arquivo `Plataforma_de_Benchmark_para_Algoritmos_de_Otimização_Bio_inspirados.ipynb` para visualizar as baterias de testes.
