import subprocess


def generer_debut_latex_amc(titre):
    debut = r"""\documentclass[a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
\usepackage{automultiplechoice}

\begin{document}
\onecopy{1}{
\AMCtitle{%s}
""" % titre
    return debut


def combiner(fichier1, fichier2):
    return fichier1 + fichier2


def ecrire_latex(fichier_texte, titre):
    with open(titre, "w", encoding="utf-8") as fichier:
        fichier.write(fichier_texte + r"""\end{document}""")
    return titre


def generation_pdf(fichier_latex):
    pdf = subprocess.run(["pdflatex", fichier_latex])
    return pdf