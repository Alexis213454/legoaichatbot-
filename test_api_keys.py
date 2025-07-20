#!/usr/bin/env python3
"""
🧱 LEGO RAG API Key Tester
Tests all API keys used in the project
"""

import os
import requests
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def test_openai_api():
    """Test OpenAI API key"""
    print("🔑 Testing OpenAI API...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return False
    
    if not api_key.startswith("sk-"):
        print("❌ Invalid OpenAI API key format (should start with 'sk-')")
        return False
    
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello! Just testing the API."}],
            max_tokens=10
        )
        print(f"✅ OpenAI API working! Model: {response.model}")
        return True
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return False

def test_rebrickable_api():
    """Test Rebrickable API key"""
    print("\n🔑 Testing Rebrickable API...")
    
    api_key = os.getenv("REBRICKABLE_API_KEY")
    if not api_key:
        print("⚠️  REBRICKABLE_API_KEY not found (optional)")
        return None
    
    try:
        url = "https://rebrickable.com/api/v3/lego/colors/"
        params = {"key": api_key, "page_size": 1}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Rebrickable API working! Found {data.get('count', 0)} colors")
            return True
        else:
            print(f"❌ Rebrickable API error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Rebrickable API error: {e}")
        return False

def test_brickset_api():
    """Test Brickset API credentials"""
    print("\n🔑 Testing Brickset API...")
    
    api_key = os.getenv("BRICKSET_API_KEY")
    username = os.getenv("BRICKSET_USERNAME")
    password = os.getenv("BRICKSET_PASSWORD")
    
    if not all([api_key, username, password]):
        print("⚠️  Brickset credentials not found (optional)")
        return None
    
    try:
        # Test login
        login_url = "https://brickset.com/api/v3.asmx/login"
        login_params = {
            "apiKey": api_key,
            "username": username,
            "password": password,
        }
        response = requests.get(login_url, params=login_params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                print(f"✅ Brickset API working! User: {username}")
                return True
            else:
                print(f"❌ Brickset login failed: {data}")
                return False
        else:
            print(f"❌ Brickset API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Brickset API error: {e}")
        return False

def test_brickowl_api():
    """Test BrickOwl API key"""
    print("\n🔑 Testing BrickOwl API...")
    
    api_key = os.getenv("BRICKOWL_API_KEY")
    if not api_key:
        print("⚠️  BRICKOWL_API_KEY not found (optional)")
        return None
    
    try:
        url = "https://api.brickowl.com/v1/catalog/list"
        params = {"key": api_key, "type": "Set", "limit": 1}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ BrickOwl API working! Found {len(data.get('results', []))} sets")
            return True
        else:
            print(f"❌ BrickOwl API error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ BrickOwl API error: {e}")
        return False

def check_environment():
    """Check environment setup"""
    print("🌍 Checking Environment Setup...")
    
    # Check .env file
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"✅ {env_file} file exists")
        with open(env_file, 'r') as f:
            content = f.read()
            if "OPENAI_API_KEY" in content:
                print("✅ OPENAI_API_KEY found in .env")
            else:
                print("❌ OPENAI_API_KEY not found in .env")
    else:
        print(f"❌ {env_file} file not found")
    
    # Check environment variables
    required_vars = ["OPENAI_API_KEY"]
    optional_vars = ["REBRICKABLE_API_KEY", "BRICKSET_API_KEY", "BRICKSET_USERNAME", "BRICKSET_PASSWORD", "BRICKOWL_API_KEY"]
    
    print("\n📋 Environment Variables:")
    for var in required_vars:
        value = os.getenv(var)
        if value:
            masked_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            print(f"✅ {var}: {masked_value}")
        else:
            print(f"❌ {var}: Not set")
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            masked_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            print(f"✅ {var}: {masked_value}")
        else:
            print(f"⚠️  {var}: Not set (optional)")

def main():
    """Main testing function"""
    print("🧱 LEGO RAG API Key Tester")
    print("=" * 50)
    
    # Check environment
    check_environment()
    
    print("\n" + "=" * 50)
    print("🔍 Testing API Keys...")
    print("=" * 50)
    
    # Test APIs
    results = {
        "openai": test_openai_api(),
        "rebrickable": test_rebrickable_api(),
        "brickset": test_brickset_api(),
        "brickowl": test_brickowl_api(),
    }
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    required_apis = ["openai"]
    optional_apis = ["rebrickable", "brickset", "brickowl"]
    
    all_required_working = True
    for api in required_apis:
        status = results[api]
        if status is True:
            print(f"✅ {api.upper()}: Working")
        elif status is False:
            print(f"❌ {api.upper()}: Failed")
            all_required_working = False
        else:
            print(f"⚠️  {api.upper()}: Not configured")
    
    print("\nOptional APIs:")
    for api in optional_apis:
        status = results[api]
        if status is True:
            print(f"✅ {api.upper()}: Working")
        elif status is False:
            print(f"❌ {api.upper()}: Failed")
        else:
            print(f"⚠️  {api.upper()}: Not configured")
    
    # Final recommendation
    print("\n" + "=" * 50)
    if all_required_working:
        print("🎉 All required APIs are working!")
        print("✅ You can now run: uv run streamlit run app.py")
    else:
        print("⚠️  Some required APIs are not working.")
        print("🔧 Please check your API keys and try again.")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 