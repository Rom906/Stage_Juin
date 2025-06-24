from fonctions_final import generate_exam
from datetime import datetime

date = datetime(2025, 6, 10)

generate_exam(
    25,
    ["POO", "Algorithmie"],
    "AND_SPECIAL",
    "test.tex",
    date,
    correction=True,
    exercice=True,
    titre_eval="Test 1"
)
