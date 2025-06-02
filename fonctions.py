import subprocess


def generer_debut_latex(titre):
    debut = r"""
        \documentclass[12pt]{{article}}
        \usepackage[utf8]{{inputenc}}
        \usepackage[T1]{{fontenc}}
        \usepackage[french]{{babel}}
        \usepackage{{enumitem}}
        \usepackage{{pifont}}

        \begin{{document}}
        \section*{{{}}}
        """.format(titre)
    return debut


# def combiner():
def ecrire_latex(fichier_texte, titre):
    with open(titre, "w", encoding="utf-8") as fichier:
        fichier.write(fichier_texte)
    return titre


def generation_pdf(fichier_latex):
    pdf = subprocess.run(["pdflatex", fichier_latex])
    return pdf