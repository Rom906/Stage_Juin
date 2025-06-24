from fonctions_final import generate_exam
from datetime import datetime

generate_exam(
    date=datetime(2025, 6, 10),
    base_donnée="qcm_questions.yaml"
)
