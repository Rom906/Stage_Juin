import subprocess

nom_fichier = "algo_test"

latex_code = r"""
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
\usepackage[linesnumbered, ruled, vlined, french, frenchkw]{algorithm2e}

\newcommand{\PourChaque}[2]{\ForEach{#1}{#2}}
\SetAlgoNoEnd
\begin{document}

\begin{algorithm}
\DontPrintSemicolon
\Entree{Une liste $L$}
\Sortie{La somme des éléments de $L$}
$s \gets 0$\;
\PourChaque{$x \in L$}{
  $s \gets s + x$\;
}
\Retour{$s$}
\end{algorithm}

\end{document}



"""

with open(f"{nom_fichier}.tex", "w", encoding="utf-8") as f:
    f.write(latex_code)
subprocess.run(["pdflatex", f"{nom_fichier}.tex"], check=True)
