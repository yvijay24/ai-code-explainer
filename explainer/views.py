from django.shortcuts import render
from ai_client import AIClient
import difflib

SUPPORTED_LANGUAGES = ["python", "javascript"]

def index(request):
    print("INDEX VIEW LOADED")
    return render(request, "index.html")

def generate_side_by_side_diff(original: str, optimized: str):
    orig = original.splitlines()
    opt = optimized.splitlines()

    diff = list(difflib.ndiff(orig, opt))

    left = []
    right = []

    for line in diff:
        symbol = line[0]
        code = line[2:]

        # Skip ND diff annotation lines ("?")
        if symbol == "?":
            continue

        # Remove blank unchanged lines unless they contain indentation
        if symbol == " " and code.strip() == "":
            continue  # <-- This removes extra empty rows

        if symbol == "-":
            left.append({"line": code, "type": "remove"})
            right.append({"line": "", "type": "empty"})

        elif symbol == "+":
            left.append({"line": "", "type": "empty"})
            right.append({"line": code, "type": "add"})

        elif symbol == " ":
            left.append({"line": code, "type": "same"})
            right.append({"line": code, "type": "same"})

    return left, right

def analyze(request):
    print("ANALYZE VIEW CALLED! POST")
    code = request.POST.get("code", "").strip()
    print("CODE RECEIVED:", repr(code))

    if not code:
        return render(request, "index.html", {"error": "Please enter code."})

    # Split multiple snippets separated by '---'
    snippets = [s.strip() for s in code.split("---") if s.strip()]
    print("TOTAL SNIPPETS:", len(snippets))

    client = AIClient()
    results = []

    for idx, snippet in enumerate(snippets):
        print(f"Processing snippet {idx + 1}: {snippet[:30]}...")

        result = client.explain_code(snippet, language="unknown")

        optimized = result.get("optimized_code", "")
        highlighted = result.get("highlighted_code", "")

        # --- REAL DIFF ---
        raw_diff = "\n".join(
            difflib.unified_diff(
                snippet.splitlines(),
                optimized.splitlines(),
                fromfile=f"snippet_{idx+1}_original",
                tofile=f"snippet_{idx+1}_optimized",
                lineterm=""
            )
        )

        # --- PROCESSED DIFF FOR COLORING ---
        processed_diff = []
        for line in raw_diff.split("\n"):
            if line.startswith("+++") or line.startswith("---") or line.startswith("@@"):
                processed_diff.append({"text": line, "type": "header"})
            elif line.startswith("+"):
                processed_diff.append({"text": line, "type": "add"})
            elif line.startswith("-"):
                processed_diff.append({"text": line, "type": "remove"})
            else:
                processed_diff.append({"text": line, "type": "context"})
        # side_by_side = generate_side_by_side_diff(snippet, optimized)
        left_diff, right_diff = generate_side_by_side_diff(snippet, optimized)

        results.append({
            "highlighted": highlighted,
            "optimized": optimized,
            "explanation": result.get("explanation", ""),
            "key_points": result.get("key_points", []),
            "complexity": result.get("complexity", ""),
            "diff": processed_diff,
            "left_diff": left_diff,
            "right_diff": right_diff,
            "detected": result.get("detected_language", "unknown"),
        })

    return render(request, "result.html", {"results": results})
