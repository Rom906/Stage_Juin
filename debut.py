from fonctions import generation_pdf, ecrire_latex, generer_debut_latex

debut = generer_debut_latex("Test 1")
debut += r"""\end{document}"""

fichier_latex = ecrire_latex(debut, "qcm_exemple.tex")

generation_pdf(fichier_latex)
