"""Auditoria reproduzível de tamanho; não avalia verdade ou plausibilidade.

python3 tests/audit_alternatives.py --check
python3 tests/audit_alternatives.py --html /tmp/versao-anterior.html --json
"""

import argparse
import json
from pathlib import Path
from statistics import median

from validate_bank import load_questions, validate_questions


def rank_rates(rows, measure):
    """Acerto ao escolher por posição de tamanho, sorteando entre empates.

    Ordem crescente: 0 = menor; 3 = maior. A resposta certa é q[4].
    Contar toda resposta empatada como acerto inflaria o resultado.
    """
    scores = [0.0] * 4
    for row in rows:
        sizes = [measure(text) for text in row[4:8]]
        for rank, size in enumerate(sorted(sizes)):
            if sizes[0] == size:
                scores[rank] += 1 / sizes.count(size)
    return [score / len(rows) for score in scores] if rows else [0.0] * 4


def summarize(rows):
    result = {"questions": len(rows)}
    for name, measure in [("characters", len), ("words", lambda text: len(text.split()))]:
        sizes = [[measure(text) for text in row[4:8]] for row in rows]
        result[name] = {
            "correct_strictly_longest": sum(s[0] > max(s[1:]) for s in sizes),
            "correct_strictly_shortest": sum(s[0] < min(s[1:]) for s in sizes),
            "correct_tied_for_longest": sum(s[0] == max(s) and s.count(s[0]) > 1 for s in sizes),
            "rank_strategy_rates": rank_rates(rows, measure),
        }
    result["correct_over_50_percent_longer_than_all_distractors"] = sum(
        len(row[4]) > 1.5 * max(map(len, row[5:8])) for row in rows
    )
    return result


def audit(questions):
    normal = [row for row in questions if row[2] < 3]
    return {
        "normal": summarize(normal),
        "hardcore": summarize([row for row in questions if row[2] == 3]),
        "normal_by_lesson": {
            str(lesson): summarize([row for row in normal if row[0] == lesson])
            for lesson in sorted({row[0] for row in normal})
        },
    }


def check_balance(questions):
    """Detecta regressões evidentes; limites são alertas editoriais, não quotas.

    Grupos menores que 60 não têm volume para esta checagem de distribuição.
    As quatro posições são verificadas, evitando trocar 'maior' por 'menor'.
    """
    issues = []
    report = audit(questions)
    groups = [(name, report[name], 0.35) for name in ["normal", "hardcore"]]
    groups += [(f"aula {lesson}", data, 0.45) for lesson, data in report["normal_by_lesson"].items()]
    for name, group, ceiling in groups:
        if group["questions"] < 60:
            continue
        for metric in ["characters", "words"]:
            for rank, rate in enumerate(group[metric]["rank_strategy_rates"], 1):
                if rate > ceiling:
                    issues.append(f"{name}: posição {rank} por {metric} acerta {rate:.1%}, acima de {ceiling:.0%}.")
    for question_id, row in enumerate(questions, 1):
        sizes = list(map(len, row[4:8]))
        for index, size in enumerate(sizes):
            others = sizes[:index] + sizes[index + 1:]
            if size > 120 and size > 2 * median(others):
                issues.append(f"Questão {question_id}: alternativa {index + 1} tem extensão desproporcional; revisar.")
    if issues:
        raise ValueError("\n".join(issues))
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html", type=Path, help="Arquivo HTML para comparar com o banco atual")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.html:
        source = args.html.read_text(encoding="utf-8")
        questions = json.loads(source.split("const Q=", 1)[1].split("\n];", 1)[0] + "\n]")
    else:
        questions = load_questions()
    validate_questions(questions)
    report = audit(questions)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for label in ["normal", "hardcore"]:
            data = report[label]
            print(f"{label}: {data['questions']} questões")
            for metric in ["characters", "words"]:
                row = data[metric]
                rates = ", ".join(f"{rate:.1%}" for rate in row["rank_strategy_rates"])
                print(f"  {metric}: correta estritamente maior em {row['correct_strictly_longest']}; estratégias menor → maior: {rates}")
    if args.check:
        check_balance(questions)
        print("Auditoria de tamanho aprovada; revisão pedagógica continua obrigatória.")


if __name__ == "__main__":
    main()
