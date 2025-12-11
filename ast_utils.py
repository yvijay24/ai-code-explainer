# ast_utils.py
import ast

def summarize_python_ast(code: str) -> str:
    """
    Returns structural info for Python code: functions, loops, if-blocks.
    Used to reduce hallucinations.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
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
