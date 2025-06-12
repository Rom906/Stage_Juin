import yaml

with open("qcm_questions.yaml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

print(data)
