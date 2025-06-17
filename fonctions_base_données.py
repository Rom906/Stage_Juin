import yaml
import os


def combiner(base1, base2, sortie):
    with open(base1, "r", encoding="utf-8") as f1:
        base = yaml.safe_load(f1)
    with open(base2, "r", encoding="utf-8") as f2:
        base2_data = yaml.safe_load(f2)
    if type(base) == list and type(base2_data) == list:
        resultat = base + base2_data
    elif type(base) == dict and type(base2_data) == dict:
        resultat = base.copy()
        resultat.update(base2_data)
    else:
        resultat = [base, base2_data]
    with open(sortie, "w", encoding="utf-8") as f_out:
        resultat_final = yaml.dump(resultat, f_out)
    return resultat_final


# combiner("test.yaml", "test2.yaml", "resultat2.yaml")


def charger_questions(fichier_yaml):
    dossier = os.path.dirname(fichier_yaml)

    with open(fichier_yaml, 'r', encoding='utf-8') as fichier:
        base = yaml.safe_load(fichier)
    for exercice in base.get('exercices', []):
        for question in exercice.get('questions', []):
            enonce = question.get('enonce', '')
            chemin_enonce = os.path.join(dossier, enonce)
            if enonce.endswith('.tex') and os.path.isfile(chemin_enonce):
                with open(chemin_enonce, 'r', encoding='utf-8') as f_tex:
                    question['enonce'] = f_tex.read()
    return base
