import sys

with open('main.tex', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_content = """\\chapter{Metodologia} \\label{chap:metodologia}

\\section{Desenho Experimental e Plataforma de Benchmark}
Para conduzir a análise comparativa entre as diferentes abordagens algorítmicas, foi concebida e desenvolvida uma plataforma de \\textit{benchmark} padronizada. O propósito central deste ambiente experimental é assegurar a reprodutibilidade metodológica ao submeter todos os algoritmos avaliados — abrangendo os modelos clássicos e predatórios puramente biológicos (PSO, ACO, GA, GWO, WOA e BWO) e as suas variantes híbridas guiadas por Aprendizado por Reforço (QL-GWO e DRL-BWO) — a condições idênticas de orçamento computacional, ambiente e critério de parada. Dessa forma, as discrepâncias de desempenho observadas durante os ensaios decorrem intrinsecamente da eficiência do núcleo lógico de cada otimizador, isolando variáveis estruturais ou vieses de implementação.

\\section{Configuração do Orçamento Computacional}
A fim de estabelecer um paralelo fidedigno com a literatura acadêmica e as métricas exigidas pelas competições de otimização de larga escala, o orçamento computacional foi calibrado sob restrições severas e padronizadas. Determinou-se a execução de um mínimo de 30 amostragens independentes (\\textit{runs}) para cada cenário experimental. Esta parametrização é fundamental para acomodar a estocasticidade inerente às meta-heurísticas e satisfazer os pressupostos do Teorema do Limite Central, garantindo estabilidade estocástica e permitindo análises estatísticas robustas \\cite{ismail2026beyond}. O limite iterativo foi fixado em 500 iterações absolutas, fornecendo um ciclo de processamento suficiente para que as fases matemáticas de exploração e explotação sejam plenamente executadas \\cite{huang2023evaluation}. 

Adicionalmente, a configuração demográfica estipulou uma população variando entre 30 a 50 agentes de busca, promovendo um balanço adequado entre diversidade populacional e parcimônia na alocação de recursos computacionais. Em todos os ensaios analíticos contínuos, os espaços matemáticos foram avaliados em 30 ou 50 dimensões ($D$). O emprego de 30 ou 50 dimensões é de suma importância para evitar a maldição da dimensionalidade e expor a verdadeira escalabilidade e resiliência dos métodos, uma vez que a vasta expansão do espaço de busca tende a degradar consideravelmente o desempenho de arquiteturas menos sofisticadas \\cite{zhong2022beluga}. A Tabela \\ref{tab:orcamento} sintetiza a parametrização do orçamento experimental.

\\begin{table}[htbp]
\\centering
\\caption{Resumo dos parâmetros de orçamento computacional.}
\\label{tab:orcamento}
\\begin{tabular}{ll}
\\toprule
\\textbf{Parâmetro} & \\textbf{Configuração Adotada} \\\\
\\midrule
Execuções Independentes (\\textit{runs}) & 30 \\\\
Limite de Iterações & 500 \\\\
Tamanho da População & 30 a 50 agentes \\\\
Dimensionalidade ($D$) & 30 ou 50 \\\\
\\bottomrule
\\end{tabular}
\\\\ \\vspace{0.2cm}
{\\small \\textit{Fonte: Elaboração própria (2026).}}
\\end{table}

\\section{Funções de Teste (Mundo Sintético)}
Para a avaliação rigorosa em ambiente sintético controlado, foram adotadas as funções matemáticas padronizadas do catálogo de testes do IEEE CEC. A suíte foi dividida logicamente com base nos diferentes perfis de desafio impostos aos algoritmos.

O primeiro subconjunto contemplou as \\textbf{Funções Unimodais} (como a função \\textit{Sphere}). Por apresentarem um único mínimo global, sem a interferência de ótimos locais adjacentes, essas funções são empregadas precipuamente para testar a velocidade de convergência e a capacidade de explotação das meta-heurísticas em uma descida contínua. Em contraste, o segundo subconjunto envolveu as \\textbf{Funções Multimodais Ruidosas} (como as funções de \\textit{Ackley} e \\textit{Rastrigin}). Caracterizadas por uma densa e intrincada malha de bacias de atração secundárias, essas topologias têm como premissa avaliar a competência da busca global (exploração) dos algoritmos em promover evasão de ótimos locais para prevenir a estagnação prematura.

\\section{Aplicações no Mundo Real (Machine Learning)}
A metodologia expande o escopo avaliativo para o mundo real, transpondo as heurísticas para o domínio complexo do Aprendizado de Máquina. Foram mapeados dois problemas otimizatórios baseados nas operações do classificador K-Vizinhos Mais Próximos (KNN):

\\begin{itemize}
    \\item \\textbf{Seleção de Atributos (\\textit{Feature Selection}):} Problema modelado em um espaço esparso de alta dimensão ($D = 150$). Neste contexto, as coordenadas contínuas propostas pelas heurísticas sofreram um processo de binarização mediante limiar contínuo para determinar quais características dos dados devem ser preservadas ou descartadas.
    \\item \\textbf{Otimização de Hiperparâmetros (HPO):} Problema focado na sintonia fina (\\textit{fine-tuning}) da própria arquitetura do modelo. Otimizou-se um conjunto denso de parâmetros em um espaço de dimensão restrita ($D = 6$) para maximizar o desempenho preditivo do classificador perante bases de dados.
\\end{itemize}

O custo correspondente a ambas as tarefas baseou-se na implementação da técnica de validação cruzada estratificada (\\textit{Stratified Cross-Validation}), de modo a calcular o custo incorrido a cada avaliação penalizando configurações redundantes de alta dimensionalidade.

\\section{Métricas de Custo e Eficiência Computacional}
A verificação sistemática do esforço de \\textit{hardware} para consecução dos processamentos estipulou a monitorização de três métricas de custo e eficiência operacionais distintas:
\\begin{enumerate}
    \\item \\textbf{Complexidade Teórica:} Calculada com base na estrutura assintótica da Notação Big-O, parametrizada na forma $\\mathcal{O}(T \\times N \\times D)$, relacionando os ciclos iterativos ($T$), o escalonamento populacional ($N$) e o quantitativo de dimensões em exploração ($D$).
    \\item \\textbf{Custo Empírico de CPU:} Métrica real contabilizada em segundos de tempo do processador exigidos para as convergências contínuas de cada bateria de execução.
    \\item \\textbf{Avaliações da Função Objetivo (NFEs):} Métrica adotada como determinante para averiguação da eficiência industrial, medindo a quantidade nua de checagens efetuadas sobre a formulação matemática. Esta parametrização suprime vantagens arquiteturais do \\textit{hardware} hospedeiro.
\\end{enumerate}

\\section{Rigor Estatístico (Validação Não-Paramétrica)}
Devido à estocasticidade intrínseca às heurísticas analisadas, enfatiza-se que a comparação fundamentada na simples observação de médias aritméticas perfaz-se insuficiente para justificar conclusões definitivas em otimização global. Dessa forma, as distribuições de custo e tempo compuseram um fluxo rígido de validação estatística não-paramétrica.

A etapa preliminar recorreu aos testes globais de \\textbf{Kruskal-Wallis} e \\textbf{Friedman} para averiguar o ranqueamento multivariado do algoritmo ante o ecossistema e constatar a existência de divergências significativas intergrupos. Confirmadas tais diferenças, aplicou-se sistematicamente o teste \\textbf{U de Mann-Whitney} para confrontos bilaterais e par-a-par adotando um limiar de significância $p < 0,05$. Por fim, procedeu-se com a aferição moderna por meio da métrica de \\textbf{Cliff's Delta}, que quantifica matematicamente a Magnitude do Efeito (\\textit{Effect Size}) proveniente das vitórias dos métodos. Este parâmetro permitiu atestar de maneira contundente os ganhos em relação à estabilidade promovida pelas hibridizações em IA sobre seus equivalentes originais.
"""

new_lines = lines[:479] + [new_content + "\n"] + lines[675:]

with open('main.tex', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Replacement complete.")
