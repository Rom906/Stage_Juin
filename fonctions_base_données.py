import yaml


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


combiner("test.yaml", "test2.yaml", "resultat2.yaml")