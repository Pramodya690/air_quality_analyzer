from openai import OpenAI
import os
import traceback
from tools import load_all_data
import pandas as pd
import numpy as np


def analyze_data(query):
    data = load_all_data()
    code_prompt = f"""
        You are an expert data scientist.

        Context:
        - Each room's data is in a pandas DataFrame within the `data` dictionary.
        Example:
        - data["room1"]
        - data["room2"]

        - Each DataFrame contains the following columns:
        'timestamp', 'co2', 'temperature', and 'humidity'.

        Task:
        - Write Python code that answers the following question:
        "{query}"

        Guidelines:
        - Use `pandas` for data manipulation.
        - If you need to perform numerical computations like mean, std, use `np`, not `pd.np`.
        - Assume that `import numpy as np` is already available.
        - Do not import pandas, NumPy, or load the data yourself.
        - Assign the final output to a variable called `result`.
        - Only return the code inside a Python code block.
        """


    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": code_prompt}],
        temperature=0.2
    )

    message = response.choices[0].message.content
    code = extract_code(message)

    # Execute code to get result
    result = safe_exec(code, data)

    # Generate explanation based on result
    explanation = generate_explanation(result, query)
    

    return {
        "output": result,
        "explanation": explanation
    }


def extract_code(code_str):
    return code_str.strip("```python").strip("```")


def safe_exec(code, data):
    try:
        local_vars = {}
        exec_globals = {
            "pd": pd,
            "np": np, 
            "data": data,
        }
        exec(code, exec_globals, local_vars)
        result = local_vars.get("result", "No result returned.")

        # Return DataFrame as JSON-ready dict
        if isinstance(result, pd.DataFrame):
            return {
                "type": "table",
                "data": result.round(2).to_dict(orient="records"),
                "columns": list(result.columns)
            }
        elif isinstance(result, dict) and "type" in result and "data" in result:
            return result  
        else:
            return {"type": "text", "data": result if isinstance(result, (str, int, float, list, dict)) else str(result)}
    except Exception as e:
        return {
            "type": "error",
            "content": f"Error running code:\n{str(e)}\n{traceback.format_exc()}"
        }



def generate_explanation(result, query):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Convert to a compact, human-readable summary
    if isinstance(result, dict) and result.get("type") == "table":
        preview = result["data"][:5]
    else:
        preview = result

    prompt = f"""
            You are a helpful data analyst.

            Given the following result from a data analysis task, explain the key insights in simple language.

            Query: {query}

            Result:
            {preview}

            Write a brief explanation (2-3 sentences).
            """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
