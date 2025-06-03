from fonctions import generation_pdf, ecrire_latex, generer_debut_latex_amc, combiner

debut = generer_debut_latex_amc("Test 1")
corps = r"""\documentclass[a4paper,12pt]{exam}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}

\begin{document}

\begin{questions}

% Question ouverte
\question[5] Expliquez pourquoi Paris est la capitale de la France.

% Question QCM (plusieurs choix, une seule bonne réponse)
\question[3] Quelle est la capitale de la France ?

\begin{choices}
    \choice Lyon
    \CorrectChoice Paris
    \choice Marseille
\end{choices}

% Question à réponse courte (l’élève doit écrire un mot ou une phrase courte)
\question[2] Donnez la couleur du drapeau français.

\end{questions}

\end{document}
"""
total = combiner(debut, corps)

fichier_latex = ecrire_latex(corps, "qcm_exemple.tex")

generation_pdf(fichier_latex)
