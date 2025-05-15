import os
from dotenv import load_dotenv
from app.db import supabase
from google import genai
from google.genai import types
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)

def summarize_profile(profile_text: str) -> str:
    prompt = f"""Summarize this candidate profile in 3 bullet points:\n\n{profile_text}. Be very concise, and avoid data overhead, such as Here is a summary of..."""
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-04-17",
        contents=prompt)
    return response.text

def generate_embedding(text: str) -> list[float]: 
    result = client.models.embed_content(
        model="gemini-embedding-exp-03-07",
        contents=text,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT", output_dimensionality=1536)
    )
    return result.embeddings[0].values

def search_profiles(query: str, threshold: float = 0.5, top_k: int = 10):
    """
    Searches the Supabase database for candidate profiles that match the given query using pgvector.
    """
    try:
        # 1. Generate the embedding for the search query
        query_embedding = generate_embedding(query)
        
        # 3. Execute the query using Supabase's raw SQL functionality
        # response = supabase.from_("candidates").select("*", "1 - (embedding <=> '" + str(query_embedding) + "') as similarity").order("similarity", desc=True).limit(10).execute()
        response = supabase.rpc(
            "match_candidates",
            {
                "query_embedding": query_embedding,
                "match_threshold": threshold,
                "match_count": top_k
            }
        ).execute()

        # 4. Extract the data from the response
        data = response.data
        print(data)
        return data

    except Exception as e:
        print(f"Error during semantic search: {e}")
        return []