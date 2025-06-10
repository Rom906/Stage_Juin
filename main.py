from fonctions_final import generate_exam
from datetime import datetime

date = datetime(2025, 6, 10)

generate_exam(3, ["POO"], "autre.tex", date, correction=True)
