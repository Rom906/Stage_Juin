import subprocess

nom_fichier = "algo_test"

latex_code = r"""
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
\usepackage[linesnumbered, ruled, lined, french, frenchkw]{algorithm2e}

% Définition manuelle de TantQue
\newcommand{\TantQue}[2]{\While{#1}{#2}}

\begin{document}

\begin{algorithm}
\DontPrintSemicolon
\Entree{$x, y$ deux entiers}
\Sortie{Le produit $x \times y$}
$r \gets 0$\;
\TantQue{$x \neq 0$}{
  \Si{$x$ est impair}{
    $x \gets x - 1$\;
    $r \gets r + y$\;
  }
  $x \gets x / 2$\;
  $y \gets y \times 2$\;
}
\Retour{$r$}
\end{algorithm}

\end{document}

"""

with open(f"{nom_fichier}.tex", "w", encoding="utf-8") as f:
    f.write(latex_code)
subprocess.run(["pdflatex", f"{nom_fichier}.tex"], check=True)
