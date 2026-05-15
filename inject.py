import json

def patch_notebook(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # -------------------------------------------------------------
    # 1. Update BenchmarkPlotter (Cell 3)
    # -------------------------------------------------------------
    
    new_plotter_code = """
    # -------------------------------------------------------------------------
    # NOVAS VISUALIZACOES (Simplificadas e em PT-BR)
    # -------------------------------------------------------------------------

    CORES_PTBR = ['#0072B2','#D55E00','#009E73','#CC79A7',
                  '#F0E442','#56B4E9','#E69F00','#000000']

    @staticmethod
    def _apply_ptbr_style():
        matplotlib.rcParams.update({
            'font.family':'serif','font.size':11,'axes.titlesize':13,
            'axes.labelsize':12,'legend.fontsize':10,'figure.dpi':150,
            'savefig.dpi':300,'savefig.bbox':'tight',
            'axes.grid':True,'grid.alpha':0.3,
        })

    @staticmethod
    def plot_tabela_ranking(all_results, func_names):
        BenchmarkPlotter._apply_ptbr_style()
        if not func_names: return
        algos = list(all_results[func_names[0]].keys())
        n_algo, n_func = len(algos), len(func_names)
        
        medianas, rankings = np.zeros((n_algo, n_func)), np.zeros((n_algo, n_func))
        for fi, fn in enumerate(func_names):
            meds = [np.median(all_results[fn][a]['best_costs']) for a in algos]
            medianas[:, fi] = meds
            rankings[:, fi] = stats.rankdata(meds)
            
        rank_medio = rankings.mean(axis=1)
        fig, ax = plt.subplots(figsize=(max(8, n_func*2), max(4, n_algo*0.8)))
        ax.axis('off')
        
        col_labels = func_names + ['Ranking\\nMedio']
        tab_data = []
        for ai, a in enumerate(algos):
            linha = [f"{medianas[ai, fi]:.2e}\\n(#{int(rankings[ai, fi])})" for fi in range(n_func)]
            linha.append(f"{rank_medio[ai]:.2f}")
            tab_data.append(linha)
            
        cell_colors = []
        for ai in range(n_algo):
            row_colors = []
            for fi in range(n_func):
                t = (rankings[ai, fi] - 1) / max(n_algo - 1, 1)
                row_colors.append((1.0, 1.0 - t*0.7, 1.0 - t*0.7))
            t = (rank_medio[ai] - 1) / max(n_algo - 1, 1)
            row_colors.append((1.0 - t*0.5, 1.0 - t*0.3, 1.0 - t*0.5))
            cell_colors.append(row_colors)
            
        tbl = ax.table(cellText=tab_data, rowLabels=algos, colLabels=col_labels, 
                       cellColours=cell_colors, cellLoc='center', loc='center')
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(9)
        tbl.scale(1.4, 2.0)
        ax.set_title("Tabela de Desempenho — Mediana e Ranking por Funcao\\n(verde=melhor, vermelho=pior)", fontsize=13, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_win_tie_loss(all_results, func_names, alpha=0.05):
        BenchmarkPlotter._apply_ptbr_style()
        if not func_names: return
        algos = list(all_results[func_names[0]].keys())
        pares = [(algos[i], algos[j]) for i in range(len(algos)) for j in range(i+1, len(algos))]
        
        labels, win, tie, loss = [], [], [], []
        for a1, a2 in pares:
            w, t, l = 0, 0, 0
            for fn in func_names:
                c1, c2 = all_results[fn][a1]['best_costs'], all_results[fn][a2]['best_costs']
                try:
                    _, p = stats.mannwhitneyu(c1, c2, alternative='two-sided')
                    if p < alpha:
                        if np.median(c1) < np.median(c2): w += 1
                        else: l += 1
                    else: t += 1
                except ValueError: t += 1
            labels.append(f"{a1}\\nvs\\n{a2}")
            win.append(w); tie.append(t); loss.append(l)
            
        fig, ax = plt.subplots(figsize=(10, max(4, len(pares)*0.9)))
        y = np.arange(len(pares))
        h = 0.55
        
        ax.barh(y, win, h, color='#009E73', label='Vitoria')
        ax.barh(y, tie, h, left=win, color='#F0E442', label='Empate')
        ax.barh(y, loss, h, left=[w+t for w,t in zip(win,tie)], color='#D55E00', label='Derrota')
        
        for i, (w,t,l) in enumerate(zip(win,tie,loss)):
            if w>0: ax.text(w/2, i, str(w), ha='center', va='center', fontweight='bold', fontsize=9, color='white')
            if t>0: ax.text(w+t/2, i, str(t), ha='center', va='center', fontweight='bold', fontsize=9)
            if l>0: ax.text(w+t+l/2, i, str(l), ha='center', va='center', fontweight='bold', fontsize=9, color='white')
            
        ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=9)
        ax.set_xlabel("Numero de Funcoes Objetivo", fontsize=11)
        ax.set_title(f"Vitorias / Empates / Derrotas (Mann-Whitney, alpha={alpha})", fontsize=13, fontweight='bold')
        ax.legend(loc='lower right')
        ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_scatter_custo_tempo(all_results, func_names):
        BenchmarkPlotter._apply_ptbr_style()
        if not func_names: return
        algos = list(all_results[func_names[0]].keys())
        markers = ['o','s','^','D','v','<','>','p']
        fig, ax = plt.subplots(figsize=(9, 6))
        
        for fi, fn in enumerate(func_names):
            for ai, a in enumerate(algos):
                d = all_results[fn][a]
                tempo, custo = np.mean(d['time']), np.median(d['best_costs'])
                ax.scatter(tempo, max(custo, 1e-300), marker=markers[fi%len(markers)], 
                           color=BenchmarkPlotter.CORES_PTBR[ai%len(BenchmarkPlotter.CORES_PTBR)], s=120, alpha=0.8, edgecolors='black', 
                           label=f"{a} / {fn}" if fi==0 else "")
                ax.annotate(a, (tempo, max(custo, 1e-300)), textcoords="offset points", xytext=(6,3), fontsize=7)
                
        ax.set_yscale('log'); ax.set_xlabel("Tempo Medio (s)"); ax.set_ylabel("Custo Mediano Final (log)")
        ax.set_title("Trade-off: Qualidade vs. Velocidade (inferior esquerdo = ideal)", fontsize=13, fontweight='bold')
        ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_painel_boxplot(all_results, func_names):
        BenchmarkPlotter._apply_ptbr_style()
        if not func_names: return
        algos = list(all_results[func_names[0]].keys())
        fig, axes = plt.subplots(len(func_names), 1, figsize=(max(9, len(algos)*1.5), len(func_names)*3.5))
        if len(func_names) == 1: axes = [axes]
        
        for ax, fn in zip(axes, func_names):
            dados = [all_results[fn][a]['best_costs'] for a in algos]
            bp = ax.boxplot(dados, labels=algos, patch_artist=True, medianprops=dict(color='crimson', linewidth=2.5))
            for i, patch in enumerate(bp['boxes']):
                patch.set_facecolor(BenchmarkPlotter.CORES_PTBR[i%len(BenchmarkPlotter.CORES_PTBR)]); patch.set_alpha(0.6)
            all_c = np.concatenate(dados)
            if np.max(all_c) / (np.min(all_c[all_c>0]) + 1e-300) > 100:
                ax.set_yscale('log')
                ax.set_ylabel(f"{fn}\\n(log)")
            else:
                ax.set_ylabel(fn)
            ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
            
        fig.suptitle("Distribuicao dos Custos Finais por Funcao Objetivo", fontsize=13, fontweight='bold', y=1.01)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_convergencia_simples(all_curves, func_name):
        BenchmarkPlotter._apply_ptbr_style()
        fig, ax = plt.subplots(figsize=(9, 5))
        for idx, (nome, curvas) in enumerate(all_curves.items()):
            media = np.mean(np.array(curvas), axis=0)
            ax.plot(np.arange(len(media)), np.maximum(media, 1e-300), label=nome, 
                    color=BenchmarkPlotter.CORES_PTBR[idx%len(BenchmarkPlotter.CORES_PTBR)], linewidth=2.0)
        ax.set_yscale('log'); ax.set_xlabel("Iteracoes"); ax.set_ylabel("Custo Medio (log)")
        ax.set_title(f"Convergencia Media — {func_name}", fontsize=13, fontweight='bold')
        ax.legend(); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_barras_nfe(all_results, func_names):
        BenchmarkPlotter._apply_ptbr_style()
        if not func_names: return
        algos = list(all_results[func_names[0]].keys())
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        for ax, met, tit, ylab in zip(axes, ['nfes', 'time'], ["Avaliacoes (NFEs)", "Tempo de Execucao"], ["NFEs Medios", "Tempo Medio (s)"]):
            for fi, fn in enumerate(func_names):
                val = [np.mean(all_results[fn][a][met]) for a in algos]
                w = 0.8/len(func_names)
                ax.bar(np.arange(len(algos)) + (fi - len(func_names)/2 + 0.5)*w, val, w, label=fn, alpha=0.82)
            ax.set_xticks(np.arange(len(algos))); ax.set_xticklabels(algos, rotation=30, ha='right')
            ax.set_ylabel(ylab); ax.set_title(tit, fontweight='bold'); ax.legend(fontsize=8)
            ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
            
        fig.suptitle("Custo Computacional por Algoritmo", fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_resumo_executivo(all_results, all_curves, func_names):
        BenchmarkPlotter._apply_ptbr_style()
        if not func_names: return
        algos = list(all_results[func_names[0]].keys())
        fig = plt.figure(figsize=(15, 10))
        import matplotlib.gridspec as gridspec
        gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.35)
        
        ax1 = fig.add_subplot(gs[0, 0])
        for idx, (nome, curvas) in enumerate(all_curves[func_names[0]].items()):
            ax1.plot(np.maximum(np.mean(np.array(curvas), axis=0), 1e-300), label=nome, color=BenchmarkPlotter.CORES_PTBR[idx%len(BenchmarkPlotter.CORES_PTBR)])
        ax1.set_yscale('log'); ax1.set_title(f"Convergencia — {func_names[0]}", fontweight='bold')
        ax1.legend(fontsize=7); ax1.spines['top'].set_visible(False); ax1.spines['right'].set_visible(False)
        
        ax2 = fig.add_subplot(gs[0, 1])
        c_med = [np.mean([np.median(all_results[fn][a]['best_costs']) for fn in func_names]) for a in algos]
        ax2.bar(algos, c_med, color=[BenchmarkPlotter.CORES_PTBR[i%len(BenchmarkPlotter.CORES_PTBR)] for i in range(len(algos))], edgecolor='black')
        ax2.set_yscale('log'); ax2.set_title("Custo Mediano Medio", fontweight='bold'); ax2.tick_params(axis='x', rotation=30)
        ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)
        
        ax3 = fig.add_subplot(gs[1, 0])
        t_med = [np.mean([np.mean(all_results[fn][a]['time']) for fn in func_names]) for a in algos]
        ax3.bar(algos, t_med, color=[BenchmarkPlotter.CORES_PTBR[i%len(BenchmarkPlotter.CORES_PTBR)] for i in range(len(algos))], edgecolor='black')
        ax3.set_title("Tempo Medio (s)", fontweight='bold'); ax3.tick_params(axis='x', rotation=30)
        ax3.spines['top'].set_visible(False); ax3.spines['right'].set_visible(False)
        
        ax4 = fig.add_subplot(gs[1, 1])
        r_med = [np.mean([sorted([np.median(all_results[fn][aa]['best_costs']) for aa in algos]).index(np.median(all_results[fn][a]['best_costs']))+1 for fn in func_names]) for a in algos]
        ordem = np.argsort(r_med)
        ax4.barh([algos[i] for i in ordem], [r_med[i] for i in ordem], color=[BenchmarkPlotter.CORES_PTBR[i%len(BenchmarkPlotter.CORES_PTBR)] for i in ordem], edgecolor='black')
        ax4.set_xlabel("Ranking Medio (menor = melhor)"); ax4.set_title("Ranking Geral", fontweight='bold')
        ax4.spines['top'].set_visible(False); ax4.spines['right'].set_visible(False)
        
        fig.suptitle("Resumo Executivo do Benchmark", fontsize=14, fontweight='bold')
        plt.show()

"""
    # Insert methods before the final print statement in cell 3
    source_3 = "".join(nb['cells'][3]['source'])
    source_3 = source_3.replace('print("Secao 3: Modulo Grafico carregado!")', new_plotter_code + '\nprint("Secao 3: Modulo Grafico carregado!")')
    nb['cells'][3]['source'] = [line + '\n' for line in source_3.split('\n')]

    # -------------------------------------------------------------
    # 2. Update OptimizationBenchmarkSuite (Cell 4)
    # -------------------------------------------------------------
    source_4 = "".join(nb['cells'][4]['source'])
    
    show_all_plots_addition = """
        if self.config.get('PLOT_PAINEL_BOXPLOT', True):
            BenchmarkPlotter.plot_painel_boxplot(self.experiments_data, list(self.experiments_data.keys()))
        if self.config.get('PLOT_CONVERGENCIA_SIMPLES', True) and fn in self.all_curves:
            BenchmarkPlotter.plot_convergencia_simples(self.all_curves[fn], fn)
"""
    source_4 = source_4.replace('BenchmarkPlotter.plot_3d_landscape(func, results)', 'BenchmarkPlotter.plot_3d_landscape(func, results)' + show_all_plots_addition)
    
    show_global_plots_addition = """
        if self.config.get('PLOT_TABELA_RANKING', True):
            BenchmarkPlotter.plot_tabela_ranking(self.experiments_data, func_names)
        if self.config.get('PLOT_WIN_TIE_LOSS', True):
            BenchmarkPlotter.plot_win_tie_loss(self.experiments_data, func_names)
        if self.config.get('PLOT_SCATTER_CUSTO', True):
            BenchmarkPlotter.plot_scatter_custo_tempo(self.experiments_data, func_names)
        if self.config.get('PLOT_BARRAS_NFE', True):
            BenchmarkPlotter.plot_barras_nfe(self.experiments_data, func_names)
        if self.config.get('PLOT_RESUMO_EXECUTIVO', True):
            BenchmarkPlotter.plot_resumo_executivo(self.experiments_data, self.all_curves, func_names)
"""
    source_4 = source_4.replace('BenchmarkPlotter.print_latex_table(self.experiments_data, func_names)', 'BenchmarkPlotter.print_latex_table(self.experiments_data, func_names)\n' + show_global_plots_addition)
    
    nb['cells'][4]['source'] = [line + '\n' for line in source_4.split('\n')]

    # -------------------------------------------------------------
    # 3. Update CONFIG (Cell 5)
    # -------------------------------------------------------------
    source_5 = "".join(nb['cells'][5]['source'])
    flags = """
    'PLOT_TABELA_RANKING': True,
    'PLOT_WIN_TIE_LOSS': True,
    'PLOT_SCATTER_CUSTO': True,
    'PLOT_PAINEL_BOXPLOT': True,
    'PLOT_CONVERGENCIA_SIMPLES': True,
    'PLOT_BARRAS_NFE': True,
    'PLOT_RESUMO_EXECUTIVO': True,
"""
    # Find the line with PLOT_RADAR and insert our flags right after it
    import re
    source_5 = re.sub(r"('PLOT_RADAR':\s*(True|False),)", r"\1" + flags, source_5)
    nb['cells'][5]['source'] = [line + '\n' for line in source_5.split('\n')]

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)

patch_notebook('Plataforma_de_Benchmark_para_Algoritmos_de_Otimização_Bio_inspirados.ipynb')
print("Notebook patched successfully!")
