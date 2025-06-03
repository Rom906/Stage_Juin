import subprocess
import os

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

def ajoute_qcm(numero_question: str, question: str,
    liste_choix:list, indices_bonnes_reponses:list):
    latex = "\\element{math}{\n"
    latex += "\\begin{question}{" + str(numero_question) + "} " + question + "\n"
    latex += "\\begin{choices}\n"

    for i in range(len(liste_choix)):
        if i in indices_bonnes_reponses:
            latex += "  \\correctchoice " + liste_choix[i] + "\n"
        else:
            latex += "  \\choice " + liste_choix[i] + "\n"

    latex += "\\end{choices}\n"
    latex += "\\end{question}\n"
    latex += "}\n"

    return latex