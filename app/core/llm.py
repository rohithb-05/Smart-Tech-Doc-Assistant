import os
import google.generativeai as genai

# Read the API key from environment
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("Warning: GEMINI_API_KEY is not set.")

def generate_draft(query: str, context: str) -> str:
    """
    Step 1: Generate an answer based on the context using Gemini.
    """
    model = genai.GenerativeModel('gemini-1.5-pro-latest')  # or gemini-pro
    
    prompt = f"""
    You are a technical documentation assistant. 
    Use the following retrieved context to answer the user's question accurately.
    If the context does not contain the answer, state that you don't know based on the provided documentation.
    
    Context:
    {context}
    
    User Question: {query}
    
    Answer:
    """
    
    response = model.generate_content(prompt)
    return response.text


def verify_content(query: str, draft: str, context: str) -> str:
    """
    Step 2: Agentic Verification. Review the generated draft against the context to prevent hallucinations.
    """
    if "```" not in draft:
        # If there's no code block, we might skip heavy code verification,
        # but let's verify general correctness anyway to be safe.
        pass
        
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    
    prompt = f"""
    You are an expert code reviewer and technical verifier.
    Your task is to review a drafted response to ensure it strictly aligns with the provided technical documentation context.
    Mitigate any hallucinations, especially in code snippets or method names.
    If the drafted response includes features or syntax not present in the context, correct it or add a disclaimer.
    
    Original Question: {query}
    
    Provided Context:
    {context}
    
    Drafted Response to Verify:
    {draft}
    
    Output the Final Corrected Response below. If the draft is completely correct and aligns with the context, output the draft exactly as is.
    """
    
    response = model.generate_content(prompt)
    return response.text


def run_rag_pipeline(query: str, context_chunks: list[str]) -> str:
    """
    Orchestrates the LLM generation and verification steps.
    """
    if not context_chunks:
        return "I could not find relevant information in the uploaded documentation."
        
    combined_context = "\n\n---\n\n".join(context_chunks)
    
    # Step 1: Draft
    draft = generate_draft(query, combined_context)
    
    # Step 2: Verify
    final_answer = verify_content(query, draft, combined_context)
    
    return final_answer
