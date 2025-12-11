from django.shortcuts import render
from ai_client import AIClient
import difflib
from ast_utils import summarize_python_ast, summarize_js_ast

SUPPORTED_LANGUAGES = ["python", "javascript"]

def index(request):
    print("INDEX VIEW LOADED")
    return render(request, "index.html")

def detect_language(snippet):
    snippet = snippet.strip()
    if snippet.startswith("def ") or "import " in snippet or "return " in snippet:
        return "python"
    if "console.log" in snippet or "function" in snippet:
        return "javascript"
    return "unknown"

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
        detected_lang = "python" if "def " in snippet or ":" in snippet else "javascript"

        ast_summary = ""
        if detected_lang == "python":
            ast_summary = summarize_python_ast(snippet)
        elif detected_lang == "javascript":
            ast_summary = summarize_js_ast(snippet)

        result = client.explain_code(
            snippet,
            language=detected_lang,
            ast_summary=ast_summary
        )
        optimized = result.get("optimized_code", "")
        highlighted = result.get("highlighted_code", "")
        # side_by_side = generate_side_by_side_diff(snippet, optimized)
        left_diff, right_diff = generate_side_by_side_diff(snippet, optimized)

        results.append({
            "highlighted": highlighted,
            "optimized": optimized,
            "explanation": result.get("explanation", ""),
            "key_points": result.get("key_points", []),
            "complexity": result.get("complexity", ""),
            "left_diff": left_diff,
            "right_diff": right_diff,
            "detected": result.get("detected_language", "unknown"),
            "ast": ast_summary,
        })

    return render(request, "result.html", {"results": results})
