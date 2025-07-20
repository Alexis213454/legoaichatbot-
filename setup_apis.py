#!/usr/bin/env python3
"""
🔧 API Setup Helper for LEGO RAG
Helps you get API keys and better data
"""

import os
import webbrowser
from dotenv import load_dotenv

def setup_rebrickable():
    """Help user get Rebrickable API key"""
    print("🔑 Setting up Rebrickable API")
    print("=" * 40)
    
    print("1. 🌐 Opening Rebrickable API page...")
    webbrowser.open("https://rebrickable.com/api/")
    
    print("\n2. 📝 Steps:")
    print("   • Click 'Get API Key'")
    print("   • Fill the form (name, email)")
    print("   • Check email for API key")
    print("   • Copy the key")
    
    print("\n3. 🔧 Add to .env file:")
    print("   REBRICKABLE_API_KEY=your-key-here")
    
    input("\nPress Enter when you have the key...")

def check_current_data():
    """Check what data we currently have"""
    print("\n📊 Current Data Status")
    print("=" * 40)
    
    try:
        import duckdb
        conn = duckdb.connect('lego_data.duckdb')
        
        # Check sources
        sources = conn.execute("SELECT source, COUNT(*) FROM lego_data GROUP BY source").fetchall()
        print("Data sources:")
        for source, count in sources:
            print(f"  • {source}: {count} sets")
        
        # Check themes
        themes = conn.execute("SELECT theme, COUNT(*) FROM lego_data WHERE theme IS NOT NULL GROUP BY theme ORDER BY COUNT(*) DESC LIMIT 10").fetchall()
        print("\nTop themes:")
        for theme, count in themes:
            print(f"  • {theme}: {count} sets")
        
        conn.close()
        
    except Exception as e:
        print(f"Error checking data: {e}")

def main():
    """Main setup function"""
    print("🧱 LEGO RAG API Setup Helper")
    print("=" * 50)
    
    # Check current data
    check_current_data()
    
    print("\n🎯 To get better data (Technic, Star Wars, etc.):")
    print("1. Get Rebrickable API key (free)")
    print("2. Add it to .env file")
    print("3. Run: uv run python load_data.py")
    
    choice = input("\nGet Rebrickable API key now? (y/n): ").lower()
    if choice == 'y':
        setup_rebrickable()
    
    print("\n✅ Setup complete!")
    print("Next: Add API key to .env and run load_data.py")

if __name__ == "__main__":
    main() 