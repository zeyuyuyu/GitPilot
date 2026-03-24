import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_code(prompt):
    """Generate code based on a given prompt using the OpenAI GPT-3 API."""
    response = openai.Completion.create(
        engine="code-davinci-002",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text

def optimize_code(code):
    """Optimize the generated code using the OpenAI Codex API."""
    response = openai.Completion.create(
        engine="code-davinci-002",
        prompt=f"Optimize the following code:\n{code}",
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text

def main():
    prompt = "Create a simple Flask web application that displays 'Hello, World!'"
    generated_code = generate_code(prompt)
    optimized_code = optimize_code(generated_code)
    print(optimized_code)

if __name__ == "__main__":
    main()