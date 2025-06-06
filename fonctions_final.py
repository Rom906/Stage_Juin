import yaml
import subprocess
import random


def question_to_latex(q, correction=False):
    latex = ""
    if not q["libre"]:
        if "image" in q:
            latex += "\\section{" + q.get("section", "") + "}\n"
            latex += "\\difficulte{" + str(q["difficulte"]) + "}\n"
            latex += "\\begin{figure}[h]\n"
            latex += "\\centering\n"
            latex += "\\includegraphics[width=" + q.get("taille_image", "1.0") + "\\textwidth]{" + q["image"] + "}\n"
            latex += "\\end{figure}\n"
            latex += "\\enonce{" + q["enonce"] + "}\n"
            latex += "\\setcounter{possibility}{0}\n"
            latex += "\\possibilites{\n"

            choix_mélangés = list(q["choix"])
            random.shuffle(choix_mélangés)

            for choix in choix_mélangés:
                if choix["correct"]:
                    if correction:
                        latex += "    \\correct " + "\\textcolor{red}{" + choix["texte"] + "}\n"
                    else:
                        latex += "    \\leurre " + choix["texte"] + "\n"
                else:
                    latex += "    \\leurre " + choix["texte"] + "\n"
            latex += "}\n"
            if correction and "explication" in q:
                latex += "\\renewcommand{\\pourquoi}{" + "\\textcolor{red}{" + q["explication"] + "}}\n"
            else:
                latex += "\\pourquoi{}\n"
        else:
            latex += "\\section{" + q.get("section", "") + "}\n"
            latex += "\\difficulte{" + str(q["difficulte"]) + "}\n"
            latex += "\\enonce{" + q["enonce"] + "}\n"
            latex += "\\setcounter{possibility}{0}\n"
            latex += "\\possibilites{\n"

            choix_mélangés = list(q["choix"])
            random.shuffle(choix_mélangés)

            for choix in choix_mélangés:
                if choix["correct"]:
                    if correction:
                        latex += "    \\correct " + "\\textcolor{red}{" + choix["texte"] + "}\n"
                    else:
                        latex += "    \\leurre " + choix["texte"] + "\n"
                else:
                    latex += "    \\leurre " + choix["texte"] + "\n"
            latex += "}\n"
            if correction and "explication" in q:
                latex += "\\renewcommand{\\pourquoi}{" + "\\textcolor{red}{" + q["explication"] + "}}\n"
            else:
                latex += "\\pourquoi{}\n"
    else:
        if "image" in q:
            latex += "\\section{" + q.get("section", "") + "}\n"
            latex += "\\difficulte{" + str(q["difficulte"]) + "}\n"
            latex += "\\begin{figure}[h]\n"
            latex += "\\centering\n"
            latex += "\\includegraphics[width=" + q.get("taille_image", "1.0") + "\\textwidth]{" + q["image"] + "}\n"
            latex += "\\end{figure}\n"
            latex += "\\enonce{" + q["enonce"] + "}\n"
            latex += rf"""\noindent
\begin{{tabular}}{{|p{{\dimexpr\textwidth-2\tabcolsep-2\arrayrulewidth}}|}}
\hline
\parbox[t][{q["choix"]}][c]{{\dimexpr\textwidth-2\tabcolsep-2\arrayrulewidth}}{{}}
\\
\hline
\end{{tabular}}
"""
        else:
            latex += "\\section{" + q.get("section", "") + "}\n"
            latex += "\\difficulte{" + str(q["difficulte"]) + "}\n"
            latex += "\\enonce{" + q["enonce"] + "}\n"
            latex += rf"""\noindent
\begin{{tabular}}{{|p{{\dimexpr\textwidth-2\tabcolsep-2\arrayrulewidth}}|}}
\hline
\parbox[t][{q["choix"]}][c]{{\dimexpr\textwidth-2\tabcolsep-2\arrayrulewidth}}{{}}
\\
\hline
\end{{tabular}}
"""
    return latex


def ecrire_latex(contenu_questions, nom_fichier, date: str, correction=False):
    preambule = r"""\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{enumitem,amssymb}
\usepackage{tabularx}
\usepackage{calc}
\usepackage{cprotect}
\usepackage{xcolor}
\usepackage[a4paper,textwidth=16cm,top=2cm,bottom=2cm,headheight=25pt,headsep=12pt,footskip=25pt]{geometry}
\usepackage{fancybox}
\newenvironment{framed}%
  {\begin{Sbox}\begin{minipage}{\dimexpr\linewidth-2\fboxrule-2\fboxsep}}%
  {\end{minipage}\end{Sbox}\fbox{\TheSbox}}

\usepackage{pifont}
\usepackage{ifthen}

\newcommand{\corrige}{0}
\newcounter{possibility}"""
    if correction:
        preambule4 = r"""
    \newcommand{{\correct}}{%
      \addtocounter{{possibility}}{1}
      \ifthenelse{\equal{\corrige}{1}}%
        {\item[\ding{\numexpr171+\value{possibility}}]}%
        {\item[\textcolor{red}{\ding{\numexpr171+\value{possibility}}}]}%
    }"""
    else:
        preambule4 = r"""\newcommand{\correct}{%
  \addtocounter{possibility}{1}
  \ifthenelse{\equal{\corrige}{0}}%
    {\item[\textcolor{red}{\ding{\numexpr171+\value{possibility}}}]}%
    {\item[\ding{\numexpr171+\value{possibility}}]}%
}
"""
    preambule5 = r"""
\newcommand{\leurre}{%
  \addtocounter{possibility}{1}
  \item[\ding{\numexpr171+\value{possibility}}]%
}

\newcommand{\enonce}[1]{%
  \noindent
  Question~:
  \vspace*{.5\baselineskip}

  \noindent
  \begin{framed}
    #1
  \end{framed}
}

\newcommand{\difficulte}[1]{%
  Difficulté : 
  \ifthenelse{#1 > 1 \or #1 = 1}{\ding{72}}{\ding{73}} 
  \ifthenelse{#1 > 2 \or #1 = 2}{\ding{72}}{\ding{73}}
  \ifthenelse{#1 > 3 \or #1 = 3}{\ding{72}}{\ding{73}}
  \ifthenelse{#1 > 3}{S}{}%
}

\newcommand{\possibilites}[1]{%
  \setcounter{possibility}{0}
  \vspace*{\baselineskip}
  \begin{itemize}[label={}]
    #1
  \end{itemize}
}


\newcommand{\pourquoi}[1]{}

\begin{document}
\begin{center}
  \begin{tabular}{c}
  \hline\\%\vspace{0.1cm}
  {\textsc{\'Ecole Centrale Marseille}}\vspace{0.1cm}
  \\

    {\bf {\Large Modélisation et Conception Objet}}\\%\vspace{0.2cm}
    \\
    {\bf  { Contrôle 1A }}\\"""
    preambule2 = r"""
    {{\footnotesize {}}}\\""".format(
        date
    )
    preambule3 = r"""
    \hline
  \end{tabular}
\end{center}
\vspace{0.6cm}

\noindent
{\em Les réponses sont à donner directement sur le sujet. Un espace est réservé pour chaque réponse.}

\vspace*{1cm}
\noindent
\begin{tabular}{|l|p{10cm}|}
    \hline
    Nom : & \\
    \hline
    Prénom : & \\
    \hline
    
\end{tabular}


\vspace*{2cm}
\noindent
Barème. Pour chaque question : 
\begin{itemize}
    \item ne pas répondre donne 0 point,
    \item répondre de façon exacte donne : $\mathbf{+\frac{2}{3}}$ points
    \item répondre de façon inexacte\footnote{le nombre de points négatifs varie pour que si l'on répond de façon aléatoire l'espérance soit nulle} : 
    \begin{itemize}
        \item pour une réponse de type VRAI/FAUX : $\mathbf{-\frac{2}{3}}$ points,
        \item pour une réponse libre : $\mathbf{-\frac{2}{3}}$ points,
        \item pour une réponse de type 1 parmi 3 : $\mathbf{-\frac{1}{3}}$ points.
    \end{itemize}
\end{itemize}
\newpage
"""
    preambule = preambule + preambule4 + preambule5 + preambule2 + preambule3
    with open(nom_fichier, "w", encoding="utf-8") as fichier:
        fichier.write(preambule)
        fichier.write(contenu_questions)
        fichier.write(
            "\n\\end{document}"
        )  # rajoute la fin pour que le compilateur ne plante pas
    return fichier


def generation_pdf(nom_fichier):
    pdf = subprocess.run(["pdflatex", nom_fichier])
    return pdf


def extraire_difficulte(q):
    return q["difficulte"]


def generate_exam(nombre_question: int, theme: str, nom_fichier: str, date: str, correction: bool):
    with open("qcm_questions.yaml", "r", encoding="utf-8") as fichier:
        base = yaml.safe_load(fichier)
    latex_code = ""
    toutes_les_questions = base[theme]

    if nombre_question >= len(toutes_les_questions):
        Liste = list(toutes_les_questions)
    else:
        Liste = []
        indices_deja_choisis = set()
        while len(Liste) < nombre_question:
            index = random.randrange(len(toutes_les_questions))
            if index not in indices_deja_choisis:
                Liste.append(toutes_les_questions[index])
                indices_deja_choisis.add(index)
    Liste.sort(key=extraire_difficulte)
    for question in Liste:
        latex_code += question_to_latex(question, correction=False) + "\n"
    ecrire_latex(latex_code, nom_fichier, date)
    final = generation_pdf(nom_fichier)
    if correction:
        correc = ""
        for question in Liste:
            correc += question_to_latex(question, correction=True) + "\n"
        ecrire_latex(correc, "corrige.tex", date)
        generation_pdf("corrige.tex")

    return final
