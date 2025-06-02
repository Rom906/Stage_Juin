import subprocess


def generation_pdf(titre, fichier_latex):
    pdf = subprocess.run(["pdflatex", titre+".tex"])
    return pdf