from fonctions_final import generate_exam
from datetime import datetime

date = datetime(2025, 6, 10)

generate_exam(15, ["POO", "Algorithmie"], "autre.tex", date, correction=True, exercice=True)
