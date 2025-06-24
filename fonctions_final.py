import yaml
import subprocess
import random
from fonctions_base_données import charger_questions, filtre_exercices


def enonce_propre(texte):
    end_algo_tag = r"\end{algorithm}"
    index = texte.find(end_algo_tag)

    if index != -1:
        index_fin = index + len(end_algo_tag)
        partie_algo = texte[:index_fin]
        reste = texte[index_fin:].strip()

        result = partie_algo + "\n\n"
        if reste:
            result += "\\enonce{" + reste + "}\n"
        else:
            result += "\\enonce{}\n"
        return result
    else:
        return "\\enonce{" + texte + "}\n"


def groupe_to_latex(groupe, correction=False, exercice=True):
    latex = ""
    if "questions" in groupe:
        if "nom" in groupe and groupe["nom"]:
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

        # QCM
        if not q.get("libre", False):
            latex += "\\difficulte{" + str(q.get("difficulte", "?")) + "}\n"
            if "image" in q:
                latex += "\\begin{figure}[h]\n\\centering\n"
                latex += (
                    "\\includegraphics[width="
                    + q.get("taille_image", "0.8")
                    + "\\textwidth]{"
                    + q["image"]
                    + "}\n"
                )
                latex += "\\end{figure}\n"
            latex += enonce_propre(q["enonce"])

            latex += "\\begin{center}\n\\fbox{%\n\\begin{minipage}{0.9\\linewidth}\n"
            latex += "\\setcounter{possibility}{0}\n\\possibilites{\n"

            choix_melanges = list(q.get("choix", []))
            random.shuffle(choix_melanges)
            for choix in choix_melanges:
                texte = (
                    choix.get("texte", "") if isinstance(choix, dict) else str(choix)
                )
                correct = (
                    choix.get("correct", False) if isinstance(choix, dict) else False
                )
                if correct:
                    if correction:
                        latex += "    \\correct \\textcolor{red}{" + texte + "}\n"
                    else:
                        latex += "    \\leurre " + texte + "\n"
                else:
                    latex += "    \\leurre " + texte + "\n"

            latex += "}\n\\end{minipage}}\n\\end{center}\n"

            if correction and "explication" in q:
                latex += (
                    "\\renewcommand{\\pourquoi}{"
                    + "\\textcolor{red}{"
                    + q["explication"]
                    + "}}\n"
                )
            else:
                latex += "\\pourquoi{}\n"

        # Question libre
        elif q["libre"]:
            latex += "\\subsection*{" + q.get("id", "") + "}\n"
            latex += "\\difficulte{" + str(q.get("difficulte", "?")) + "}\n"

            if "image" in q:
                latex += "\\begin{figure}[h]\n\\centering\n"
                latex += (
                    "\\includegraphics[width="
                    + q.get("taille_image", "0.8")
                    + "\\textwidth]{"
                    + q["image"]
                    + "}\n"
                )
                latex += "\\end{figure}\n"
            latex += enonce_propre(q["enonce"])

            if "choix" in q:
                latex += (
                    "\\begin{center}\n\\fbox{%\n\\begin{minipage}{0.9\\linewidth}\n"
                )
                latex += "\\setcounter{possibility}{0}\n\\possibilites{\n"

                choix_melanges = list(q.get("choix", []))
                random.shuffle(choix_melanges)
                for choix in choix_melanges:
                    texte = (
                        choix.get("texte", "")
                        if isinstance(choix, dict)
                        else str(choix)
                    )
                    correct = (
                        choix.get("correct", False)
                        if isinstance(choix, dict)
                        else False
                    )
                    if correct:
                        if correction:
                            latex += "    \\correct \\textcolor{red}{" + texte + "}\n"
                        else:
                            latex += "    \\leurre " + texte + "\n"
                    else:
                        latex += "    \\leurre " + texte + "\n"
                latex += "}\n\\end{minipage}}\n\\end{center}\n"
            if correction:
                explications = "\\textcolor{red}{" + q.get("explication", "") + "}\n"

                hauteur_zone = q.get("cadre", "4cm")
                latex += rf"""\noindent
    \begin{{tabular}}{{|p{{\dimexpr\textwidth-2\tabcolsep-2\arrayrulewidth}}|}}
    \hline
    \parbox[t][{hauteur_zone}][c]{{\dimexpr\textwidth-2\tabcolsep-2\arrayrulewidth}}{{{explications}}}
    \\
    \hline
    \end{{tabular}}
    """
            else:
                hauteur_zone = q.get("cadre", "4cm")
                latex += rf"""\noindent
    \begin{{tabular}}{{|p{{\dimexpr\textwidth-2\tabcolsep-2\arrayrulewidth}}|}}
    \hline
    \parbox[t][{hauteur_zone}][c]{{\dimexpr\textwidth-2\tabcolsep-2\arrayrulewidth}}{{}}
    \\
    \hline
    \end{{tabular}}
    """
        else:
            latex += "\\difficulte{" + str(q.get("difficulte", "?")) + "}\n"
            latex += enonce_propre(q["enonce"])

        latex += "\n\\vspace{1cm}\n"
    return latex


def ecrire_latex(
    contenu_questions, nom_fichier, identifiant, institution, date, titre, correction=False, packages=[]
):
    date_2 = date.strftime("%d-%m-%Y")
    preambule = r"""\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{calc}"""
    total = ""
    total = "\n".join(packages) + "\n"
    premabule21 = (
        total
        + r"""
\usepackage{enumitem,amssymb}
\usepackage{tabularx}
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
    )
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
  {\textsc{""" + institution + r"""}}\vspace{0.1cm}
  \\
    {\bf {\Large"""
    preambule22 = (
        " "
        + titre
        + r"""}}\\%\vspace{0.2cm}
    \\
    {\bf  { Contrôle 1A }}\\"""
    )
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

"""
    preambule31 = r"""

\vspace{2cm}
\noindent
\begin{tabular}{|l|p{10cm}|}
    \hline
""" + f"{identifiant} & \\\\ \n\\hline\n\\end{{tabular}}\n\\vspace*{{2cm}}\n" + r"""
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
    preambule = (
        preambule
        + premabule21
        + preambule4
        + preambule5
        + preambule22
        + preambule2
        + preambule3
        + preambule31
    )
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


def generate_exam(date: str,base_donnée: str, instructions=""):
    if instructions == base_donnée:
        base = charger_questions(base_donnée)
        paramètres = base.get("instructions", [])
        nombre_question = paramètres.get("nombre_question", 20)
        theme = paramètres.get("theme", [])
        mode = paramètres.get("mode", "AND")
        nom_fichier = paramètres.get("nom_fichier", "test.tex")
        correction = paramètres.get("correction", True)
        exercice = paramètres.get("exercice", False)
        titre_cours = paramètres.get("titre_section_cours", "Question de cours")
        titre_eval = paramètres.get("titre_eval", "Test UE Algorithmie et programmation")
        identifiant = paramètres.get("identifiant", "Nom/Prenom")
        institution = paramètres.get("intitution", "Aix-Marseille-Université")
    else:
        base = charger_questions(base_donnée)
        with open(instructions, "r", encoding="utf-8") as f:
            instruc = yaml.safe_load(f)
        paramètres = instruc.get("instructions", False)
        if not paramètres:
            print("Les intructions sont manquantes")
        nombre_question = paramètres.get("nombre_question", 20)
        theme = paramètres.get("theme", [])
        mode = paramètres.get("mode", "AND")
        nom_fichier = paramètres.get("nom_fichier", "test.tex")
        correction = paramètres.get("correction", True)
        exercice = paramètres.get("exercice", False)
        titre_cours = paramètres.get("titre_section_cours", "Question de cours")
        titre_eval = paramètres.get("titre_eval", "Test UE Algorithmie et programmation")
        identifiant = paramètres.get("identifiant", "Nom/Prenom")
        institution = paramètres.get("intitution", "Aix-Marseille-Université")
    tous_les_exercices = base.get("exercices", [])
    exercices = filtre_exercices(tous_les_exercices, theme, mode=mode)
    exercices_simples = []
    exercices_complexes = []
    package = [
        "inputenc", "graphicx", "enumitem", "amssymb", "tabularx", "calc",
        "cprotect", "xcolor", "geometry", "fancybox", "pifont", "ifthen"
    ]
    latex_code = ""
    for exo in exercices:
        questions = exo.get("questions", [])
        if len(questions) == 1:
            exercices_simples.append(exo)
        elif len(questions) > 1:
            exercices_complexes.append(exo)

    Liste_complexes = []
    Liste_simples = []

    if exercice:
        total_questions_complexes = sum(len(e.get("questions", [])) for e in exercices_complexes)
        if nombre_question > total_questions_complexes:
            Liste_complexes = list(exercices_complexes)
            nb_manquantes = nombre_question - total_questions_complexes
            Liste_simples = exercices_simples[:nb_manquantes]
        else:
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
            latex_code += "\\section*{" + titre_cours + "}\n"
            for groupe in Liste_simples:
                latex_code += groupe_to_latex(groupe, correction=False) + "\n"
    else:
        Liste_simples = exercices_simples[:nombre_question]
        latex_code += "\\section*{" + titre_cours + "}\n"
        for groupe in Liste_simples:
            latex_code += groupe_to_latex(groupe, correction=False) + "\n"
    
    liste_package = []
    for groupe in exercices_simples + Liste_complexes:
        for question in groupe.get("questions", []):
            if question.get("package"):
                liste_package.append(question["package"])
    liste_package = list(set(liste_package))
    ecrire_latex(latex_code, nom_fichier, identifiant, institution, date, titre=titre_eval, correction=False, packages=liste_package)
    final = generation_pdf(nom_fichier)

    if correction:
        correc = ""
        if exercice:
            for groupe in Liste_complexes:
                correc += groupe_to_latex(groupe, correction=True) + "\n"
            if Liste_simples:
                correc += "\\section*{" + titre_cours + "}\n"
                for groupe in Liste_simples:
                    correc += groupe_to_latex(groupe, correction=True) + "\n"
        else:
            correc += "\\section*{" + titre_cours + "}\n"
            for groupe in Liste_simples:
                correc += groupe_to_latex(groupe, correction=True) + "\n"
        ecrire_latex(correc, "corrige.tex", identifiant, institution, date, titre=titre_eval, correction=False, packages=liste_package)
        generation_pdf("corrige.tex")
    exam_yaml = {
        "instructions": {
            "nombre_question": nombre_question,
            "theme": theme,
            "mode": mode,
            "nom_fichier": nom_fichier,
            "correction": correction,
            "exercice": exercice,
            "titre_section_cours": titre_cours,
            "titre_eval": titre_eval,
        },
        "exercices": [],
    }
    numero_exercice = 1
    liste_exercices_selectionnes = Liste_complexes + Liste_simples

    for exo in liste_exercices_selectionnes:
        exercice_yaml = {
            "nom": exo.get("nom", ""),
            "mots_clés": exo.get("mots_clés", ""),
            "questions": [],
        }
        questions = exo.get("questions", [])
        numero_question = 1
        for question in questions:
            identifiant = f"{numero_exercice}.{numero_question}" if len(questions) > 1 else f"{numero_exercice}"
            nouvelle_question = dict(question)
            nouvelle_question["question"] = identifiant
            exercice_yaml["questions"].append(nouvelle_question)
            numero_question += 1
        exam_yaml["exercices"].append(exercice_yaml)
        numero_exercice += 1
    with open("examen_selection.yaml", "w", encoding="utf-8") as fichier_yaml:
        yaml.dump(exam_yaml, fichier_yaml, sort_keys=False, allow_unicode=True)
    return final
