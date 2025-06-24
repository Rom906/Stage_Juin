from fonctions_final import generate_exam
from datetime import datetime

generate_exam(
    25,
    ["POO", "Algorithmie"],
    "AND_SPECIAL",
    "test.tex",
    date=datetime(2025, 6, 10),
    correction=True,
    exercice=True,
    titre_eval="Test 1"
)
