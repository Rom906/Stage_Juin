from fonctions import generation_pdf, ecrire_latex, generer_debut_latex_amc, combiner

debut = generer_debut_latex_amc("Test 1")

fichier_latex = ecrire_latex(debut, "qcm_exemple.tex")

generation_pdf(fichier_latex)
