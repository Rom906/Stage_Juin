import yaml
import os


def charger_questions(fichier_yaml):
    dossier = os.path.dirname(fichier_yaml)
    with open(fichier_yaml, "r", encoding="utf-8") as fichier:
        base = yaml.safe_load(fichier)
    for exercice in base.get("exercices", []):
        for question in exercice.get("questions", []):
            enonce = question.get("enonce", "")
            if enonce.endswith(".tex"):
                chemin_enonce = os.path.join(dossier, enonce)
                if os.path.isfile(chemin_enonce):
                    with open(chemin_enonce, "r", encoding="utf-8") as f_tex:
                        lignes = f_tex.readlines()
                    lignes_utiles = []
                    dedans = False
                    for ligne in lignes:
                        if ligne.strip().startswith("% QUESTION"):
                            dedans = True
                            continue
                        if ligne.strip().startswith("% FIN"):
                            dedans = False
                            break
                        if dedans:
                            lignes_utiles.append(ligne)
                    question["enonce"] = "".join(lignes_utiles)

    return base


def est_sous_liste(petits, grands):
    for element in petits:
        if element not in grands:
            return False
    return True


def filtre_exercices(exercices, tags_recherches, mode="AND"):
    """
    Filtre la liste d'exercices selon les tags recherchés et le mode choisi.

    - mode "AND" : tous les tags doivent être présents
    - mode "OR" : au moins un tag doit être présent
    - mode "AND_SPECIAL" :
         soit tous les tags sont présents,
         soit l'exercice a exactement un tag parmi les tags recherchés
         (aucun autre tag)
    """
    exercices_filtres = []

    for exercice in exercices:
        tags = exercice.get("mots_clés", [])
        if isinstance(tags, str):
            tags = [tags]

        if mode == "AND":
            if est_sous_liste(tags_recherches, tags):
                exercices_filtres.append(exercice)

        elif mode == "OR":
            trouve = False
            for t in tags_recherches:
                if t in tags:
                    trouve = True
                    break
            if trouve:
                exercices_filtres.append(exercice)

        elif mode == "AND_SPECIAL":
            condition_1 = est_sous_liste(tags_recherches, tags)
            condition_2 = (len(tags) == 1) and (tags[0] in tags_recherches)
            if condition_1 or condition_2:
                exercices_filtres.append(exercice)

        else:
            raise ValueError(f"Mode inconnu : {mode}")

    return exercices_filtres
