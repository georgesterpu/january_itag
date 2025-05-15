from fastapi import FastAPI, HTTPException
from app.db import supabase
from app.ai import summarize_profile, generate_embedding, search_profiles
from app.models import CandidateProfile
from typing import List, Dict

app = FastAPI()

@app.post("/candidate/")
def create_candidate(profile: CandidateProfile):
    
    profile_text = f"""
    Full Name: {profile.full_name}
    Headline: {profile.headline}
    About: {profile.about}
    Skills: {', '.join(profile.skills) if isinstance(profile.skills, list) else profile.skills}
    GitHub URL: {profile.github_url}
    """
    summary = summarize_profile(profile_text)
    embedding = generate_embedding(profile_text)

    # Store profile in Supabase
    data = {
        "full_name": profile.full_name,
        "headline": profile.headline,
        "about": summary,
        "skills": profile.skills,
        "github_url": profile.github_url,
        "embedding": embedding,
        "email": profile.email,
        "phone": profile.phone
    }

    res = supabase.table("candidates").insert(data).execute()

    if "error" in res.dict() and res.dict()["error"] is not None:
        raise HTTPException(status_code=500, detail=str(res.dict()["error"]))
    return {"message": "Candidate profile created successfully", "summary": summary}


@app.get("/search/")
def search_profiles_endpoint(query: str) -> List[Dict]:
    """
    API endpoint for searching candidate profiles.
    """
    try:
        results = search_profiles(query)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))