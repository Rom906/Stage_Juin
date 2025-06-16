import yaml
import subprocess
import random


def groupe_to_latex(groupe, correction=False, exercice=True):
    latex = ""
    if "questions" in groupe:
        if "nom" in groupe: # Verifie que c'est pas une chaine vide au moins evite de rajouter du latex pour rien 
            latex += "\\section*{" + groupe["nom"] + "}\n"
        questions = groupe["questions"]
    else:
        questions = groupe

    for q in questions:
        if not exercice and len(questions) != 1:
            continue
        if not isinstance(q, dict):
            print("Attention, un élément n'est pas un dictionnaire:", q)
            continue
        # Si la question n'est pas libre (QCM)
        if not q.get("libre", False):
            latex += "\\difficulte{" + str(q.get("difficulte", "?")) + "}\n"

            if "image" in q:
                latex += "\\begin{figure}[h]\n\\centering\n"
                latex += "\\includegraphics[width=" + q.get("taille_image", "0.8") + "\\textwidth]{" + q["image"] + "}\n"
                latex += "\\end{figure}\n"
            latex += "\\enonce{" + q["enonce"] + "}\n"
            latex += "\\setcounter{possibility}{0}\n\\possibilites{\n"
            choix_melanges = list(q.get("choix", []))
            random.shuffle(choix_melanges)
            for choix in choix_melanges:
                if isinstance(choix, dict):
                    texte = choix.get("texte", "")
                    correct = choix.get("correct", False)
                else:
                    texte = str(choix)
                    correct = False
                if correct:
                    if correction:
                        latex += "    \\correct \\textcolor{red}{" + texte + "}\n"
                    else:
                        latex += "    \\leurre " + texte + "\n"
                else:
                    latex += "    \\leurre " + texte + "\n"
            latex += "}\n"
            if correction and "explication" in q:
                latex += "\\renewcommand{\\pourquoi}{" + "\\textcolor{red}{" + q["explication"] + "}}\n"
            else:
                latex += "\\pourquoi{}\n"
        # Question libre (avec ou sans choix)
        elif q["libre"]:
            latex += "\\subsection*{" + q.get("id", "") + "}\n"
            latex += "\\difficulte{" + str(q.get("difficulte", "?")) + "}\n"
            if "image" in q:
                latex += "\\begin{figure}[h]\n\\centering\n"
                latex += "\\includegraphics[width=" + q.get("taille_image", "0.8") + "\\textwidth]{" + q["image"] + "}\n"
                latex += "\\end{figure}\n"
            latex += "\\enonce{" + q["enonce"] + "}\n"
            # Si on a des choix (QCM dans une question libre)
            if "choix" in q and q["choix"]:
                latex += "\\setcounter{possibility}{0}\n\\possibilites{\n"

                choix_melanges = list(q.get("choix", []))
                random.shuffle(choix_melanges)
                for choix in choix_melanges:
                    if isinstance(choix, dict):
                        texte = choix.get("texte", "")
                        correct = choix.get("correct", False)
                    else:
                        texte = str(choix)
                        correct = False
                    if correct:
                        if correction:
                            latex += "    \\correct \\textcolor{red}{" + texte + "}\n"
                        else:
                            latex += "    \\leurre " + texte + "\n"
                    else:
                        latex += "    \\leurre " + texte + "\n"
                latex += "}\n"
            # On met toujours le cadre même s'il y a choix pour que l'élève puisse justifier
            hauteur_zone = q.get("cadre", "4cm")
            latex += rf"""\noindent
\begin{{tabular}}{{|p{{\dimexpr\textwidth-2\tabcolsep-2\arrayrulewidth}}|}}
\hline
\parbox[t][{hauteur_zone}][c]{{\dimexpr\textwidth-2\tabcolsep-2\arrayrulewidth}}{{}}
\\
\hline
\end{{tabular}}
"""

        else: # securité car j'ai rencontrer des petits problemes parfois
            latex += "\\difficulte{" + str(q.get("difficulte", "?")) + "}\n"
            latex += "\\enonce{" + q["enonce"] + "}\n"

    return latex


def ecrire_latex(contenu_questions, nom_fichier, date, correction=False):
    date_2 = date.strftime("%d-%m-%Y")
    preambule = r"""\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{enumitem,amssymb}
\usepackage{tabularx}
\usepackage{calc}
\usepackage{cprotect}
\usepackage{xcolor}
\usepackage[a4paper,textwidth=16cm,top=2cm,bottom=2cm,headheight=25pt,headsep=12pt,footskip=25pt]{geometry}
\usepackage{fancybox}
\newenvironment{framed}%
  {\begin{Sbox}\begin{minipage}{\dimexpr\linewidth-2\fboxrule-2\fboxsep}}%
  {\end{minipage}\end{Sbox}\fbox{\TheSbox}}

\usepackage{pifont}
\usepackage{ifthen}

\newcommand{\corrige}{0}
\newcounter{possibility}"""
    if correction:
        preambule4 = r"""
    \newcommand{{\correct}}{%
      \addtocounter{{possibility}}{1}
      \ifthenelse{\equal{\corrige}{1}}%
        {\item[\ding{\numexpr171+\value{possibility}}]}%
        {\item[\textcolor{red}{\ding{\numexpr171+\value{possibility}}}]}%
    }"""
    else:
        preambule4 = r"""\newcommand{\correct}{%
  \addtocounter{possibility}{1}
  \ifthenelse{\equal{\corrige}{0}}%
    {\item[\textcolor{red}{\ding{\numexpr171+\value{possibility}}}]}%
    {\item[\ding{\numexpr171+\value{possibility}}]}%
}
"""
    preambule5 = r"""
\newcommand{\leurre}{%
  \addtocounter{possibility}{1}
  \item[\ding{\numexpr171+\value{possibility}}]%
}

\newcommand{\enonce}[1]{%
  \noindent
  Question~:
  \vspace*{.5\baselineskip}

  \noindent
  \begin{framed}
    #1
  \end{framed}
}

\newcommand{\difficulte}[1]{%
  Difficulté : 
  \ifthenelse{#1 > 1 \or #1 = 1}{\ding{72}}{\ding{73}} 
  \ifthenelse{#1 > 2 \or #1 = 2}{\ding{72}}{\ding{73}}
  \ifthenelse{#1 > 3 \or #1 = 3}{\ding{72}}{\ding{73}}
  \ifthenelse{#1 > 3}{S}{}%
}

\newcommand{\possibilites}[1]{%
  \setcounter{possibility}{0}
  \vspace*{\baselineskip}
  \begin{itemize}[label={}]
    #1
  \end{itemize}
}


\newcommand{\pourquoi}[1]{}

\begin{document}
\begin{center}
  \begin{tabular}{c}
  \hline\\%\vspace{0.1cm}
  {\textsc{\'Ecole Centrale Marseille}}\vspace{0.1cm}
  \\

    {\bf {\Large Modélisation et Conception Objet}}\\%\vspace{0.2cm}
    \\
    {\bf  { Contrôle 1A }}\\"""
    preambule2 = r"""
    {{\footnotesize {}}}\\""".format(
        date_2
    )
    preambule3 = r"""
    \hline
  \end{tabular}
\end{center}
\vspace{0.6cm}

\noindent
{\em Les réponses sont à donner directement sur le sujet. Un espace est réservé pour chaque réponse.}

\vspace*{1cm}
\noindent
\begin{tabular}{|l|p{10cm}|}
    \hline
    Nom : & \\
    \hline
    Prénom : & \\
    \hline
    
\end{tabular}


\vspace*{2cm}
\noindent
Barème. Pour chaque question : 
\begin{itemize}
    \item ne pas répondre donne 0 point,
    \item répondre de façon exacte donne : $\mathbf{+\frac{2}{3}}$ points
    \item répondre de façon inexacte\footnote{le nombre de points négatifs varie pour que si l'on répond de façon aléatoire l'espérance soit nulle} : 
    \begin{itemize}
        \item pour une réponse de type VRAI/FAUX : $\mathbf{-\frac{2}{3}}$ points,
        \item pour une réponse libre : $\mathbf{-\frac{2}{3}}$ points,
        \item pour une réponse de type 1 parmi 3 : $\mathbf{-\frac{1}{3}}$ points.
    \end{itemize}
\end{itemize}
\newpage
"""
    preambule = preambule + preambule4 + preambule5 + preambule2 + preambule3
    with open(nom_fichier, "w", encoding="utf-8") as fichier:
        fichier.write(preambule)
        fichier.write(contenu_questions)
        fichier.write(
            "\n\\end{document}"
        )  # rajoute la fin pour que le compilateur ne plante pas
    return fichier


def generation_pdf(nom_fichier):
    pdf = subprocess.run(["pdflatex", nom_fichier])
    return pdf


def extraire_difficulte(q):
    if "difficulte" in q:
        try:
            diff = int(q["difficulte"])
            if diff < 1:
                diff = 1
            elif diff > 3:
                diff = 3
            return diff
        except:
            return 1
    else:
        return 1


def generate_exam(nombre_question: int, theme: list, nom_fichier: str, date: str, correction: bool, exercice=False):
    with open("qcm_questions.yaml", "r", encoding="utf-8") as fichier:
        base = yaml.safe_load(fichier)

    latex_code = ""

    exercices = [g for g in base.get("exercices", []) if any(t in g.get("mots_clés", "") for t in theme)]

    exercices_simples = [ex for ex in exercices if len(ex.get("questions", [])) == 1]
    exercices_complexes = [ex for ex in exercices if len(ex.get("questions", [])) > 1]

    if exercice:
        total_questions_complexes = sum(len(ex.get("questions", [])) for ex in exercices_complexes)

        if nombre_question > total_questions_complexes:
            Liste_complexes = list(exercices_complexes)
            nb_manquantes = nombre_question - total_questions_complexes
            Liste_simples = exercices_simples[:nb_manquantes]
        else:
            Liste_complexes = []
            indices_choisis = set()
            while len(Liste_complexes) < nombre_question:
                idx = random.randrange(len(exercices_complexes))
                if idx not in indices_choisis:
                    Liste_complexes.append(exercices_complexes[idx])
                    indices_choisis.add(idx)
            Liste_simples = []

        Liste_complexes.sort(key=extraire_difficulte)

        for groupe in Liste_complexes:
            latex_code += groupe_to_latex(groupe, correction=False) + "\n"

        if Liste_simples:
            latex_code += "\\section*{Questions cours}\n"
            for groupe in Liste_simples:
                latex_code += groupe_to_latex(groupe, correction=False) + "\n"

    else:
        Liste_simples = exercices_simples[:nombre_question]
        latex_code += "\\section*{Questions cours}\n"
        for groupe in Liste_simples:
            latex_code += groupe_to_latex(groupe, correction=False) + "\n"

    ecrire_latex(latex_code, nom_fichier, date)
    final = generation_pdf(nom_fichier)
    if correction:
        correc = ""
        if exercice:
            for groupe in Liste_complexes:
                correc += groupe_to_latex(groupe, correction=True) + "\n"
            if Liste_simples:
                correc += "\\section*{Questions cours (les questions sont donc independantes)}\n"
                for groupe in Liste_simples:
                    correc += groupe_to_latex(groupe, correction=True) + "\n"
        else:
            correc += "\\section*{Questions cours (les questions sont donc independantes)}\n"
            for groupe in Liste_simples:
                correc += groupe_to_latex(groupe, correction=True) + "\n"
        ecrire_latex(correc, "corrige.tex", date)
        generation_pdf("corrige.tex")

    return final
