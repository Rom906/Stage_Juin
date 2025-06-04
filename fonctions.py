import subprocess


def generer_debut_latex_amc(titre):
    debut = r"""\documentclass[a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
\usepackage[noautomark]{automultiplechoice}

\begin{document}

\onecopy[draft=false]{1}{"""
    return debut


def combiner(fichier1, fichier2):
    return fichier1 + fichier2


def ecrire_latex(fichier_texte, titre):
    with open(titre, "w", encoding="utf-8") as fichier:
        fichier.write(fichier_texte + r"""}
    \end{document}""")
    return titre


def generation_pdf(fichier_latex):
    pdf = subprocess.run(["pdflatex", fichier_latex])
    return pdf


# Base de donnée

def ajoute_qcm(numero_question: int, question: str, liste_choix: list,
               indices_bonnes_reponses: list, theme: str, base="base_donnée.tex"):
    numero_question = str(numero_question)
    latex = rf"""\element{{{theme}}}{{
\begin{{question}}{{{numero_question}}} {question}
\begin{{choices}}
"""

    for i in range(len(liste_choix)):
        if i in indices_bonnes_reponses:
            latex += rf"  \correctchoice {liste_choix[i]}\n"
        else:
            latex += rf"  \wrongchoice {liste_choix[i]}\n"
    latex += r"""\end{choices}
\end{question}
}
"""
    with open(base, "w", encoding="utf-8") as fichier:
        fichier.write(latex)
    return base


def ajoute_question_libre(numero_question: int, question: str, espace: int, theme: str, base="base_donée.tex"):
    numero_question = str(numero_question)
    latex = rf"""\element{{{theme}}}{{
    \begin{{question}}{{{numero_question}}}{question}
\begin{{choices}}"""
    latex += rf"""\vspace{{{espace + "cm"}}}""" # rajouter un cadre à proportionner en fonction de l'espace voulu par l'utilisateur
    with open(base, "w", encoding="utf-8") as fichier:
        fichier.write(latex)
    return base

