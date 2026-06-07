"""
Uses local Gemma model via ollama+litellm to audit LaTeX quality.
"""
import json
import random
from pathlib import Path

import litellm

MODEL = "ollama/gemma4:12b"
NUM_SAMPLES = 30

SYSTEM_PROMPT = """You are a LaTeX quality auditor. For each equation:
1. Check if the LaTeX syntax is valid (balanced braces, proper commands)
2. Check if it correctly represents the intended physics/math
3. Rate it 1-5 (5=perfect)

Reply with one line per equation in exactly this format:
ID|score|issues|suggestion
- issues: comma-separated or "none"
- suggestion: corrected LaTeX or "none"

Example:
0|5|none|none
1|3|missing braces|F = ma"""


def main():
    path = Path(__file__).parent / "famous_equations.json"
    data = json.load(open(path))
    print(f"Loaded {len(data)} equations, using {MODEL}\n")

    random.seed(42)
    sample = random.sample(data, NUM_SAMPLES)

    lines = []
    for i, eq in enumerate(sample):
        lines.append(f"{i}: {eq['name']} | {eq['equation']} | context: {eq.get('context','')}")

    prompt = "Check these LaTeX equations:\n\n" + "\n".join(lines) + "\n\nRespond in the specified format."

    try:
        response = litellm.completion(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=2000,
        )
        text = response.choices[0].message.content.strip()
        print(f"Model response:\n{text}\n")

        scores = []
        issues_found = []

        for line in text.split("\n"):
            line = line.strip()
            if not line or "|" not in line:
                continue
            parts = [p.strip() for p in line.split("|")]
            try:
                idx = int(parts[0])
            except ValueError:
                continue

            eq = sample[idx]
            score = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
            issues = parts[2] if len(parts) > 2 else "none"
            suggestion = parts[3] if len(parts) > 3 else "none"

            scores.append(score)
            status = "PASS" if score >= 4 else "WARN" if score >= 3 else "FAIL"
            print(f"  [{status}] ({score}/5) {eq['name']}")

            if issues and issues != "none":
                issues_found.append((eq["name"], eq["equation"], issues, suggestion))

        avg = sum(scores) / len(scores) if scores else 0
        print("\n--- Results ---")
        print(f"Average score: {avg:.1f}/5")
        print(f"Evaluated: {len(scores)}/{NUM_SAMPLES}")
        print(f"Equations with issues: {len(issues_found)}")

        if issues_found:
            print("\n--- Issues ---")
            for name, latex, issues, suggestion in issues_found:
                print(f"\n  {name}")
                print(f"    LaTeX: {latex}")
                print(f"    Issues: {issues}")
                if suggestion != "none":
                    print(f"    Suggested: {suggestion}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
