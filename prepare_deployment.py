#!/usr/bin/env python3
"""
🚀 Deployment Preparation Script
Prepares database and FAISS index for Gitpod deployment
"""

import os
import shutil
import subprocess
from pathlib import Path

def check_files():
    """Check if required files exist"""
    print("🔍 Checking deployment files...")
    
    files_to_check = [
        "lego_data.duckdb",
        "faiss_index/index.faiss",
        "faiss_index/index.pkl"
    ]
    
    all_exist = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            all_exist = False
    
    return all_exist

def create_missing_files():
    """Create missing database and FAISS index"""
    print("\n🔧 Creating missing files...")
    
    # Check if database exists
    if not os.path.exists("lego_data.duckdb"):
        print("📊 Creating database...")
        subprocess.run(["uv", "run", "python", "load_data.py"], check=True)
    else:
        print("✅ Database already exists")
    
    # Check if FAISS index exists
    if not os.path.exists("faiss_index"):
        print("🔍 Creating FAISS index...")
        subprocess.run(["uv", "run", "python", "fix_faiss.py"], check=True)
    else:
        print("✅ FAISS index already exists")

def verify_deployment():
    """Verify deployment is ready"""
    print("\n🎯 Verifying deployment...")
    
    # Test database
    try:
        import duckdb
        conn = duckdb.connect("lego_data.duckdb")
        count = conn.execute("SELECT COUNT(*) FROM lego_data").fetchone()[0]
        print(f"✅ Database: {count} records")
        conn.close()
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    # Test FAISS index
    try:
        from langchain_openai import OpenAIEmbeddings
        from langchain_community.vectorstores import FAISS
        from dotenv import load_dotenv
        
        load_dotenv()
        embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        vectorstore = FAISS.load_local("./faiss_index", embeddings, allow_dangerous_deserialization=True)
        
        # Test search
        results = vectorstore.similarity_search("Star Wars", k=3)
        print(f"✅ FAISS index: {len(results)} test results")
    except Exception as e:
        print(f"❌ FAISS error: {e}")
        return False
    
    return True

def main():
    """Main deployment preparation"""
    print("🚀 LEGO RAG Deployment Preparation")
    print("=" * 50)
    
    # Check current files
    if check_files():
        print("\n✅ All files ready for deployment!")
    else:
        print("\n🔧 Creating missing files...")
        create_missing_files()
    
    # Verify everything works
    if verify_deployment():
        print("\n🎉 Deployment ready!")
        print("\n📋 Next steps:")
        print("1. git add .")
        print("2. git commit -m 'Add database and FAISS index for instant Gitpod startup'")
        print("3. git push")
        print("4. Open Gitpod workspace - should start instantly!")
    else:
        print("\n❌ Deployment verification failed")
        print("Please check the errors above")

if __name__ == "__main__":
    main() 