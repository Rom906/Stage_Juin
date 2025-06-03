from fonctions import ecrire_latex, generer_debut_latex_amc, generation_pdf

debut = generer_debut_latex_amc("Test 1")


fichier_latex = ecrire_latex(debut, "qcm_exemple.tex")

generation_pdf(fichier_latex)
