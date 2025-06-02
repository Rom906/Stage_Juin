import subprocess
contenu_latex = r""" 
\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
\usepackage{enumitem}
\usepackage{pifont}

\begin{document}

\section*{QCM Exemple}

\textbf{Question 1 :} Quelle est la capitale de la France ?\\
\begin{itemize}[label=\ding{113}]
  \item Berlin
  \item Madrid
  \item Rome
  \item Paris
\end{itemize}

\vspace{0.5cm}

\textbf{Question 2 :} Décrivez brièvement la Révolution française.\\
\vspace{3cm}

\end{document}
"""

# Écriture dans un fichier
with open("qcm_exemple.tex", "w", encoding="utf-8") as f:
    f.write(contenu_latex)

subprocess.run(["pdflatex", "qcm_exemple.tex"])
