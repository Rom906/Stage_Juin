import yaml
import subprocess


def question_to_latex(q):
    latex = "\\section{" + q.get("section", "") + "}\n"
    latex += "\\difficulte{" + str(q["difficulte"]) + "}\n"
    latex += "\n" + "\\enonce{" + q["enonce"] + "}\n"
    latex += "\\possibilites{\n"
    for choix in q["choix"]:
        if choix["correct"]:
            latex += "    \\correct " + choix["texte"] + "\n"
        else:
            latex += "    \\leurre " + choix["texte"] + "\n"
    latex += "}\n"
    latex += "\\pourquoi{}\n"
    return latex


def ecrire_latex(contenu_questions, nom_fichier):
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
\newcounter{possibility}

\newcommand{\correct}{%
  \addtocounter{possibility}{1}
  \ifthenelse{\equal{\corrige}{0}}%
    {\item[\ding{\the\numexpr\value{possibility}}]}%
    {\item[\textcolor{red}{\ding{\the\numexpr\value{possibility}-10}}]}%
}

\newcommand{\leurre}{%
  \addtocounter{possibility}{1}
  \item[\ding{\the\numexpr\value{possibility}}]%
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
  \vspace*{\baselineskip}
  \begin{itemize}[label={}]
    #1
  \end{itemize}
}

\newcommand{\pourquoi}[1]{}

\begin{document}
"""
    with open(nom_fichier, "w", encoding="utf-8") as fichier:
        fichier.write(preambule)
        fichier.write(contenu_questions)
        fichier.write("\n\\end{document}") # rajoute la fin pour que le compilateur ne plante pas
    return fichier


def generation_pdf(nom_fichier):
    pdf = subprocess.run(["pdflatex", nom_fichier])
    return pdf


with open("qcm_questions.yaml", "r", encoding="utf-8") as fichier:
    base = yaml.safe_load(fichier)

latex_code = ""
for question in base["questions"]:
    latex_code += question_to_latex(question) + "\n"

ecrire_latex(latex_code, "prime.tex")

generation_pdf("prime.tex")
