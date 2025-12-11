# AI Code Analyzer (Django + OpenAI)

A simple web tool that lets you paste code and get:

- Explanation  
- Key points  
- Time/space complexity  
- Optimized version  
- Diff comparison  
- Semantic highlighting  
- Support for multiple snippets (`---` separator)

Supports **Python & JavaScript**.

## Features
- Explain code in plain English  
- Highlight functions, loops, conditions, variables, etc.  
- Show optimized code  
- Compare original vs optimized using diff  
- Analyze time and space complexity  
- Handle multiple snippets at once  

## How to Run
1. Install dependencies:
```
pip install -r requirements.txt
```

2. Set your API key:
```
OPENAI_API_KEY=your_key_here
```

3. Start the server:
```
python manage.py runserver
```

4. Open in browser:
```
http://127.0.0.1:8000/
```

## Multi-Snippet Example
```
console.log(5+3)
---
def add(a,b):
    return a + b
```

## Project Structure
```
codeai/
  codeai/        # Django settings
  explainer/     # App with AI logic
  templates/     # HTML UI
  ai_client.py   # OpenAI API integration
  manage.py
```

## Note
Do not upload:
- venv  
- __pycache__  
- API keys  
