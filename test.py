from litellm import completion
import os
import sys

equation = sys.argv[1]
prompt = f"Explain the physical equation {equation}"

response = completion(model="gemini/gemini-2.5-flash", messages=[{"role": "user", "content": prompt}])

print(response)
