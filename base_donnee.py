import yaml


# Fonction de transformation (identique à celle de tout à l’heure)
def question_to_latex(q):
    latex = "\\vbox{\n"
    latex += "    \\section{" + q.get("section", "") + "}\n"
    latex += "    \\difficulte{" + q["difficulte"] + "}\n"
    latex += "    \\enonce{" + q["enonce"] + "}\n"
    latex += "    \\possibilites{\n"
    for choix in q["choix"]:
        if choix["correct"]:
            latex += "        \\correct " + choix["texte"] + "\n"
        else:
            latex += "        \\leurre " + choix["texte"] + "\n"
    latex += "    }\n"
    latex += "    \\pourquoi{}\n"
    latex += "}\n"
    return latex


with open("questions.yaml", "r", encoding="utf-8") as f:
    base_de_donnée = yaml.safe_load(f)

for question in base_de_donnée["questions"]:
    latex_code = question_to_latex(question)
    print(latex_code) 
