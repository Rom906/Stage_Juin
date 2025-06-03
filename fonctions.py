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


def ajouter(nombre):

# def compiler_amc(nom_fichier_tex: str):
#     prefix = os.path.splitext(nom_fichier_tex)[0]
#     try:
#         subprocess.run([
#             "auto-multiple-choice", "prepare",
#             "--mode", "s",
#             "--prefix", ".",
#             nom_fichier_tex
#         ], check=True)

#         subprocess.run([
#             "auto-multiple-choice", "meptex",
#             "--src", nom_fichier_tex,
#             "--out", f"{prefix}-sujet.pdf",
#             "--prefix", "."
#         ], check=True)