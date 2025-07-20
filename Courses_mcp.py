from datetime import datetime, time
from typing import List, Dict, Any
import json
import os
from fastmcp import FastMCP
import numpy as np
from fastapi import Body, status
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("courses_embedded.json") as f:
    embedded_courses = json.load(f)

embedding_matrix = np.array([c["embedding"] for c in embedded_courses], dtype = "float32")

def find_match(query: str, k: int = 25):
    query_embedding = model.encode([query])[0]
    query_vector = np.array(query_embedding).reshape(1, -1)
    similarities = cosine_similarity(query_vector, embedding_matrix)[0]
    top_k = similarities.argsort()[-k:][::-1]
    return  [embedded_courses[i] for i in top_k]
    
mcp = FastMCP("Tool to extract courses")

@mcp.tool()
def get_courses(
    query: str = Body(
        ..., 
        embed=True, 
        description="Give the keywords like subject, instructor's name"
    )
) -> dict:
    """
    Searhced Duke Course List by keywords and gives back a list of matching courses, their descriptions and lab schedules
    """
   

    raw_query = query.strip().lower()
    keywords = [word for word in raw_query.split()]
    data = find_match(query, 25)

    
    return {
    "courses": [
        {
            "Subject":    c.get("Subject"),
            "Catalog":    c.get("Catalog"),
            "Section":    c.get("Section"),
            "Long Title": c.get("Long.Title"),
            "Mtg Start":  c.get("Mtg.Start"),
            "Mtg End":    c.get("Mtg.End"),
            "Days":       c.get("Pat"),
            "Facility":   c.get("Facility"),
            "Instructor": c.get("Instructor"),
            "Enrl Stat":  c.get("Enrl.Stat"),
            "Tot Enrl":   c.get("Tot.Enrl"),
            "Cap Enrl":   c.get("Cap.Enrl"),
            "Description": c.get("CourseDescr"),
            "Labs/Disussions": c.get("Support_Components")
        }
        for c in data
    ]
}


if __name__ == "__main__":
    mcp.run()
