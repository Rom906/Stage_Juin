from fonctions import compiler_amc, ecrire_latex, generer_debut_latex_amc

debut = generer_debut_latex_amc("Test 1")


fichier_latex = ecrire_latex(debut, "qcm_exemple.tex")

compiler_amc(fichier_latex)
