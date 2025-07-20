#!/usr/bin/env python3
"""
🔧 FAISS Index Fixer
Recreates the FAISS index with optimized text processing
"""

import json
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import duckdb

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def create_faiss_index():
    """Create FAISS index with optimized text processing"""
    print("🔧 Creating FAISS index...")
    
    # Connect to database
    conn = duckdb.connect("lego_data.duckdb")
    
    # Get all records
    result = conn.execute(
        """
        SELECT details, name, theme, year, pieces 
        FROM lego_data 
        ORDER BY year DESC, pieces DESC
    """
    ).fetchall()

    if not result:
        print("⚠️  No data found in database.")
        return

    print(f"  Processing {len(result)} records...")

    # Create optimized text representations
    enhanced_texts = []
    for row in result:
        details = json.loads(row[0])
        name = row[1] or ""
        theme = row[2] or ""
        year = row[3] or ""
        pieces = row[4] or ""

        # Create compact text representation (avoid token limits)
        enhanced_text = f"LEGO Set: {name} | Theme: {theme} | Year: {year} | Pieces: {pieces} | Details: {json.dumps(details, ensure_ascii=False)[:300]}"
        enhanced_texts.append(enhanced_text)

    print(f"  Creating embeddings for {len(enhanced_texts)} texts...")

    try:
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        vectorstore = FAISS.from_texts(enhanced_texts, embeddings)

        # Save the FAISS index
        vectorstore.save_local("./faiss_index")
        print("✅ FAISS index created and saved successfully!")
        
        # Test the index
        test_query = "Star Wars"
        results = vectorstore.similarity_search(test_query, k=3)
        print(f"✅ Test search for '{test_query}' found {len(results)} results")
        
    except Exception as e:
        print(f"❌ Error creating FAISS index: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    create_faiss_index() 