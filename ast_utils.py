import ast
import subprocess
import tempfile

def summarize_js_ast(code: str) -> str:
    """
    Uses Node.js + Esprima to produce a structural summary of JavaScript code.
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".js", mode="w") as tmp:
            tmp.write(code)
            tmp.flush()

            result = subprocess.run(
                ["node", "explainer/js_ast_helper.js"],
                input=code.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            return result.stdout.decode().strip()
    except Exception:
        return ""

def summarize_python_ast(code: str) -> str:
    """
    Returns a short line-based summary of top-level constructs.
    """
    try:
        tree = ast.parse(code)
    except Exception:
        return ""

    summary = []
    class Visitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            summary.append(f"Function: {node.name} at line {node.lineno}")
            self.generic_visit(node)

        def visit_For(self, node):
            summary.append(f"For loop at line {node.lineno}")
            self.generic_visit(node)

        def visit_While(self, node):
            summary.append(f"While loop at line {node.lineno}")
            self.generic_visit(node)

        def visit_If(self, node):
            summary.append(f"If statement at line {node.lineno}")
            self.generic_visit(node)

    Visitor().visit(tree)
    return "\n".join(summary)
