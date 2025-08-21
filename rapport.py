import yaml
from fonctions_base_données import charger_questions

base = charger_questions("qcm_questions.yaml")
print(base)