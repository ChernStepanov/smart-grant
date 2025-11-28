import json
from SCvalidator import parse_smeta  # твоя библиотека парсинга DOCX → JSON
from PMvalidator import validate_payments  # твой валидатор переводов

SMETA_DOCX = "smeta_complex.docx"
TRANSFERS_JSON = "transfers_invalid.json"  # можно подставить любой список переводов

# 1. Генерируем JSON сметы из DOCX
print("\nШаг 1: Парсим смету из DOCX...")
grant_json = parse_smeta(SMETA_DOCX, verbose=False)

# 2. Загружаем переводы
print("Шаг 2: Загружаем список переводов...")
with open(TRANSFERS_JSON, "r", encoding="utf-8") as f:
    transfer_list = json.load(f)

# 3. Проверяем переводы на валидность по смете
print("\nШаг 3: Валидация переводов...")
result = validate_payments(grant_json, transfer_list)

# 4. Выводим результаты
print("\n=== КОРРЕКТНЫЕ ПЕРЕВОДЫ ===\n")
for entry in result["report"]:
    print("[OK]", entry)

if result["errors"]:
    print("\n=== ОБНАРУЖЕНЫ ОШИБКИ ===\n")
    for error in result["errors"]:
        print(error)
else:
    print("\nОШИБОК НЕ НАЙДЕНО. ВСЕ ПЕРЕВОДЫ КОРРЕКТНЫ")

print("\n=== ИСПОЛЬЗОВАНИЕ БЮДЖЕТНЫХ ЛИМИТОВ ===\n")
for stage_id, rules in result["limits_used"].items():
    stage_name = None
    for stage in grant_json['stages']:
        if stage['stage_id'] == stage_id:
            stage_name = stage['stage_name']
            break
    
    print(f"ЭТАП {stage_id}: {stage_name}")
    print("-" * 40)
    for rule_id, used in rules.items():
        limit = None
        rule_name = None
        for rule in result["rules_by_stage"][stage_id]:
            if rule['rule_id'] == rule_id:
                limit = rule['limit']
                for stage in grant_json['stages']:
                    if stage['stage_id'] == stage_id:
                        for r in stage['spending_rules']:
                            if r['rule_id'] == rule_id:
                                rule_name = r['rule_name']
        percent = (used / limit * 100) if limit else 0
        status = "ПРЕВЫШЕН" if used > limit else "OK" if used > 0 else "НЕ ИСПОЛЬЗОВАН"
        print(f"  {rule_id} ({rule_name}) - {used:,} руб из {limit:,} руб ({percent:.1f}%) Статус: {status}")

total_spent = sum(sum(rules.values()) for rules in result["limits_used"].values())
total_budget = grant_json['grant_metadata']['total_budget']
print("\n=== ИТОГ ===")
print(f"Бюджет проекта: {total_budget:,} руб")
print(f"Потрачено: {total_spent:,} руб")
print(f"Остаток: {total_budget - total_spent:,} руб")

