// Parse JS code and output a simple structural summary for Python

const esprima = require("esprima");

const fs = require("fs");

let code = fs.readFileSync(0, "utf8"); // read from stdin

try {
    const ast = esprima.parseScript(code, { loc: true });

    let summary = [];

    function walk(node) {
        switch (node.type) {
            case "FunctionDeclaration":
                summary.push(`Function: ${node.id.name} at line ${node.loc.start.line}`);
                break;

            case "ForStatement":
            case "ForInStatement":
            case "ForOfStatement":
                summary.push(`For loop at line ${node.loc.start.line}`);
                break;

            case "WhileStatement":
                summary.push(`While loop at line ${node.loc.start.line}`);
                break;

            case "IfStatement":
                summary.push(`If statement at line ${node.loc.start.line}`);
                break;
        }

        for (let key in node) {
            let child = node[key];
            if (Array.isArray(child)) child.forEach(walk);
            else if (child && typeof child === "object") walk(child);
        }
    }

    walk(ast);

    process.stdout.write(summary.join("\n"));
} catch (err) {
    process.stdout.write("");
}
