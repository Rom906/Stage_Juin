import subprocess


def ecrire_latex(fichier_texte, titre):
    with open(titre, "w", encoding="utf-8") as fichier:
        fichier.write(fichier_texte)
    return titre


def generation_pdf(fichier_latex):
    pdf = subprocess.run(["pdflatex", fichier_latex])
    return pdf