# Análise de Algoritmos Bioinspirados em Problemas de Otimização

Este repositório consolida a pesquisa, os códigos e a documentação do Trabalho de Conclusão de Curso (TCC) de Antonio Marcos Patricio Castro, apresentado ao Bacharelado Interdisciplinar em Ciência e Tecnologia da Universidade Federal do Maranhão (UFMA).

## Descrição do Projeto

O avanço na Ciência de Dados e no Aprendizado de Máquina demanda algoritmos de otimização cada vez mais complexos para resolver problemas de nível $\mathcal{NP}$-difícil. Abordagens clássicas (determinísticas) falham em funções não-convexas devido ao aprisionamento em ótimos locais. Este projeto desenvolveu e avaliou uma **plataforma padronizada de benchmark** para avaliar algoritmos estocásticos (meta-heurísticas bioinspiradas) e investigar os impactos da hibridização com Inteligência Artificial.

Os seguintes algoritmos foram analisados exaustivamente:
- **PSO** (_Particle Swarm Optimization_): Enxame de partículas.
- **ACO** (_Ant Colony Optimization_): Colônia de formigas.
- **GWO** (_Grey Wolf Optimizer_): Lobos cinzentos (hierarquia e cerco matemático).
- **BWO** (_Beluga Whale Optimization_): Baleias beluga.
- **QL-GWO** (_Q-Learning GWO_): Variante híbrida orientada a Aprendizado por Reforço.
- **DRL-BWO** (_Deep Reinforcement Learning BWO_): BWO hibridizado com Redes Neurais Profundas.

## Estrutura do Repositório

O projeto foi totalmente reestruturado para manter a clareza e separação das responsabilidades:

```text
Evo-Lab-Benchmark/
│
├── docs/                      # Documentações, TCC (LaTeX) e Rascunhos
├── notebooks/                 # Cadernos Jupyter (Google Colab) com os experimentos
├── scripts/                   # Scripts auxiliares e ferramentas do projeto
├── assets/                    # Imagens, logotipos e recursos estáticos
├── presentation/              # Arquivos finais de apresentação de defesa (.pptx, PDFs)
│
├── LICENSE                    # Licença do Repositório
└── README.md                  # Este documento
```

## Metodologia e Tecnologias

Todo o ambiente computacional foi arquitetado no **Google Colab** utilizando:
- **Python**: Linguagem central da pesquisa e modelagem orientada a objetos das classes de avaliação.
- **PyTorch**: Construção dos modelos de _Deep Reinforcement Learning_.
- **Scikit-Learn**: Empregado na validação cruzada do classificador KNN.
- **Matplotlib**: Engine de plotagem estrita para geração dos gráficos de viés acadêmico.

### Validação Empírica
O projeto aplicou as meta-heurísticas nos seguintes cenários, respeitando limites iguais de execuções (NFEs):
1. **Funções Benchmark Multimodais:** Rastrigin, Ackley, Sphere, Rosenbrock, Schwefel e Griewank ($D=30$ e $D=50$).
2. **Feature Selection (FS):** Seleção de atributos em altíssima dimensionalidade ($D=150$) na base _GunPoint_.
3. **Hyperparameter Optimization (HPO):** Sintonia fina do modelo K-Nearest Neighbors.

O viés estocástico (aleatório) foi completamente isolado através de 30 execuções independentes e verificado estatisticamente usando os **Testes de Friedman** (ranking global), **U de Mann-Whitney** (vitórias par-a-par) e métrica de **Cliff's Delta** (magnitude do efeito).

## Principais Conclusões

- A inserção de Matrizes de Aprendizado por Reforço (como no **QL-GWO**) é **vital** e altamente recomendada na engenharia de dados moderna. O agente de IA substituiu os parâmetros rígidos determinísticos, ajustando perfeitamente o dilema de *Explotação vs. Exploração*, gerando o modelo mais consistente estatisticamente.
- Entre as heurísticas puramente biológicas, o **GWO** assumiu a liderança absoluta, provando superioridade geométrica sobre os pares, em especial na função Rastrigin (onde cravou um custo de $10^{-13}$).
- Mecanismos modernos que contam com saltos meramente probabilísticos, como a "Queda da Baleia" do **BWO**, falharam e colapsaram ao enfrentar espaços fortemente esparsos e de alta dimensão.

---

**Autor:** Antonio Marcos Patricio Castro  
**Orientador:** Prof. Dr. Pedro Baptista Fernandes  
**Instituição:** Universidade Federal do Maranhão (UFMA) - 2026
