import requests
import json

def generate(query, context, profile, llm, local_pipeline=None, history=None):

    # Safely handle the profile argument, which might be a string ("farmer") or a dictionary
    prof_lang = profile.get('language', 'Bilingual (English/Hindi)') if isinstance(profile, dict) else 'Bilingual (English/Hindi)'

    history_str = ""
    if history:
        for turn in history[-3:]: # only include the last 3 turns
            history_str += f"\nUser: {turn['user']}\nAI: {turn['assistant']}\n"

    prompt = f"""
You are Sahara Saathi AI. Use the provided context to answer the user's current query thoughtfully.

Chat History:
{history_str}

User Query:
{query}

Context:
{context}

Generate:
1. Simple explanation
2. Eligibility
3. Required documents
4. Step-by-step application
5. Suggest other schemes if relevant

Language: {prof_lang}
"""

    try:
        # Try primary: coeai
        res = llm.generate(
            model="deepseek-r1:70b",
            prompt=prompt,
            max_tokens=20000
        )

        if isinstance(res, dict) and "choices" in res:
            return res["choices"][0]["message"]["content"]
        
        return str(res)

    except Exception as e:
        print(f"coeai LLM connection failed: {e}. Trying local Ollama (llama3.1)...")
        
        # Try secondary: Ollama
        try:
            ollama_response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.1",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=45
            )
            if ollama_response.status_code == 200:
                result = ollama_response.json()
                return result.get("response", "No response content from Ollama.")
        except Exception as ollama_err:
            print(f"Ollama fallback failed: {ollama_err}. Returning context snippets...")

        # Tertiary fallback: Context snapshots
        intro = "I'm currently operating in restricted offline mode. Here is the most relevant information I found for you:\n\n"
        
        if isinstance(context, list):
            formatted_context = "\n\n---\n\n".join(context)
        else:
            formatted_context = str(context)
            
        return intro + formatted_context + "\n\n(Note: Connect to UPESNET or start Ollama for full AI synthesis.)"