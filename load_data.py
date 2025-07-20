import os
import requests
import hashlib
import json

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import duckdb

# Load environment variables with Gitpod fallback
if os.getenv("IN_GITPOD") == "true":
    load_dotenv(".env.gitpod")
else:
    load_dotenv(".env")  # Your default dev secrets
openai_api_key = os.getenv("OPENAI_API_KEY")
rebrickable_api_key = os.getenv("REBRICKABLE_API_KEY")
brickset_api_key = os.getenv("BRICKSET_API_KEY")
brickset_username = os.getenv("BRICKSET_USERNAME")
brickset_password = os.getenv("BRICKSET_PASSWORD")
brickowl_api_key = os.getenv("BRICKOWL_API_KEY")


def generate_unique_id(source, item_id):
    """Generate a unique ID for each record"""
    return hashlib.md5(f"{source}_{item_id}".encode()).hexdigest()


def initialize_database():
    """Initialize DuckDB database with enhanced schema"""
    conn = duckdb.connect("lego_data.duckdb")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS lego_data (
            id VARCHAR PRIMARY KEY,
            source VARCHAR,
            name VARCHAR,
            details TEXT,
            set_number VARCHAR,
            year INTEGER,
            theme VARCHAR,
            pieces INTEGER,
            minifigures INTEGER,
            price DECIMAL(10,2),
            rating DECIMAL(3,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    return conn


def fetch_rebrickable_enhanced(limit=200):
    """Enhanced Rebrickable data fetching with multiple themes"""
    print(f"Fetching {limit} records from Rebrickable API...")

    if not rebrickable_api_key:
        print("⚠️  Rebrickable API key not found. Skipping Rebrickable data.")
        return []

    # Popular theme IDs (from Rebrickable API)
    theme_ids = {
        "Star Wars": 171,      # Star Wars
        "City": 52,            # City
        "Technic": 1,          # Technic
        "Creator": 22,         # Creator
        "Architecture": 50,    # Architecture
        "Marvel": 171,         # Marvel (same as Star Wars for now)
        "DC Comics": 171,      # DC Comics (same as Star Wars for now)
        "Harry Potter": 171,   # Harry Potter (same as Star Wars for now)
        "Disney": 171,         # Disney (same as Star Wars for now)
        "Minecraft": 171,      # Minecraft (same as Star Wars for now)
        "Ninjago": 171,        # Ninjago (same as Star Wars for now)
        "Friends": 171,        # Friends (same as Star Wars for now)
        "Speed Champions": 171, # Speed Champions (same as Star Wars for now)
        "Ideas": 171,          # Ideas (same as Star Wars for now)
        "Expert": 171,         # Expert (same as Star Wars for now)
    }

    all_sets = []
    sets_per_theme = min(100, limit // len(theme_ids))  # Max 100 per theme

    for theme_name, theme_id in theme_ids.items():
        print(f"  Fetching {theme_name} theme...")
        url = "https://rebrickable.com/api/v3/lego/sets/"
        
        # Use key parameter instead of Authorization header
        params = {
            "key": rebrickable_api_key,
            "page_size": min(sets_per_theme, 1000),  # Increased page size
            "ordering": "-set_num",
            "theme_id": theme_id,
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            sets = data.get("results", [])[:sets_per_theme]
            all_sets.extend(sets)
            print(f"    Found {len(sets)} {theme_name} sets")

        except Exception as e:
            print(f"    Error fetching {theme_name}: {e}")
            continue

    print(f"  Total Rebrickable sets: {len(all_sets)}")
    return all_sets


def fetch_brickset_enhanced(limit=200):
    """Enhanced Brickset data fetching with multiple years"""
    print(f"Fetching {limit} records from Brickset API...")

    if not all([brickset_api_key, brickset_username, brickset_password]):
        print("⚠️  Brickset API credentials not found. Skipping Brickset data.")
        return []

    try:
        # Get user hash
        login_url = "https://brickset.com/api/v3.asmx/login"
        login_params = {
            "apiKey": brickset_api_key,
            "username": brickset_username,
            "password": brickset_password,
        }
        login_response = requests.get(login_url, params=login_params, timeout=30)
        login_response.raise_for_status()
        login_data = login_response.json()

        if login_data.get("status") != "success":
            print(f"  Brickset login failed: {login_data}")
            return []

        user_hash = login_data.get("hash")

        # Fetch from multiple years and themes
        all_sets = []
        
        # Strategy 1: Get diverse years
        years = [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015]
        sets_per_year = min(100, limit // (len(years) + 5))  # Max 100 per year
        
        for year in years:
            print(f"  Fetching {year} sets...")
            sets_url = "https://brickset.com/api/v3.asmx/getSets"
            sets_params = {
                "apiKey": brickset_api_key,
                "userHash": user_hash,
                "params": json.dumps({"year": year, "pageSize": sets_per_year}),
            }

            sets_response = requests.get(sets_url, params=sets_params, timeout=30)
            sets_response.raise_for_status()
            sets_data = sets_response.json()

            if sets_data.get("status") == "success":
                sets = sets_data.get("sets", [])[:sets_per_year]
                all_sets.extend(sets)
                print(f"    Found {len(sets)} {year} sets")

        # Strategy 2: Get popular themes
        popular_themes = ["Technic", "Star Wars", "City", "Creator", "Architecture", "Marvel", "Harry Potter", "Disney", "Ninjago", "Friends"]
        sets_per_theme = 50  # Increased to 50 per theme
        
        for theme in popular_themes:
            print(f"  Fetching {theme} theme sets...")
            try:
                theme_params = {
                    "apiKey": brickset_api_key,
                    "userHash": user_hash,
                    "params": json.dumps({"theme": theme, "pageSize": sets_per_theme}),
                }
                
                theme_response = requests.get(sets_url, params=theme_params, timeout=30)
                theme_response.raise_for_status()
                theme_data = theme_response.json()
                
                if theme_data.get("status") == "success":
                    theme_sets = theme_data.get("sets", [])[:sets_per_theme]
                    all_sets.extend(theme_sets)
                    print(f"    Found {len(theme_sets)} {theme} sets")
                else:
                    print(f"    No {theme} sets found")
                    
            except Exception as e:
                print(f"    Error fetching {theme}: {e}")
                continue

        print(f"  Total Brickset sets: {len(all_sets)}")
        return all_sets

    except Exception as e:
        print(f"  Error fetching from Brickset: {e}")
        return []


def fetch_brickowl_enhanced(limit=200):
    """Enhanced BrickOwl data fetching"""
    print(f"Fetching {limit} records from BrickOwl API...")

    if not brickowl_api_key:
        print("⚠️  BrickOwl API key not found. Skipping BrickOwl data.")
        return []

    url = "https://api.brickowl.com/v1/catalog/list"
    params = {"key": brickowl_api_key, "type": "Set", "limit": limit}

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        sets = data.get("results", [])[:limit]
        print(f"  Total BrickOwl sets: {len(sets)}")
        return sets

    except Exception as e:
        print(f"  Error fetching from BrickOwl: {e}")
        return []


def fetch_lego_official_api():
    """Fetch from LEGO's official API (if available)"""
    print("Fetching from LEGO Official API...")

    # LEGO doesn't have a public API, but we can scrape their website
    # This would require web scraping with proper rate limiting
    return []


def fetch_bricklink_data():
    """Fetch from BrickLink API"""
    print("Fetching from BrickLink API...")

    # BrickLink has an API but requires registration
    # https://www.bricklink.com/v3/api.page
    return []


def fetch_rebrickable_themes():
    """Fetch theme information from Rebrickable"""
    print("Fetching theme information...")

    if not rebrickable_api_key:
        return {}

    url = "https://rebrickable.com/api/v3/lego/themes/"
    headers = {"Authorization": f"key {rebrickable_api_key}"}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        return {theme["name"]: theme["id"] for theme in data.get("results", [])}
    except Exception as e:
        print(f"  Error fetching themes: {e}")
        return {}


def enhance_set_data(set_data, source):
    """Enhance set data with additional fields"""
    enhanced = set_data.copy()

    # Extract common fields
    enhanced["set_number"] = (
        set_data.get("set_num")
        or set_data.get("number")
        or set_data.get("boid")
        or str(set_data.get("id", ""))
    )

    enhanced["name"] = set_data.get("name", "Unknown Set")
    enhanced["year"] = set_data.get("year") or set_data.get("release_year")
    enhanced["theme"] = set_data.get("theme") or set_data.get("theme_name")
    enhanced["pieces"] = set_data.get("num_parts") or set_data.get("pieces")
    enhanced["minifigures"] = set_data.get("num_minifig") or set_data.get("minifigures")
    enhanced["price"] = set_data.get("price") or set_data.get("retail_price")
    enhanced["rating"] = set_data.get("rating") or set_data.get("user_rating")

    # Add source information
    enhanced["source"] = source
    enhanced["data_quality_score"] = calculate_data_quality(set_data)

    return enhanced


def calculate_data_quality(set_data):
    """Calculate a data quality score (0-100)"""
    score = 0
    fields = ["name", "set_num", "year", "theme", "num_parts"]

    for field in fields:
        if set_data.get(field):
            score += 20

    return score


def save_to_database_enhanced(conn, sets, source):
    """Save enhanced sets to database"""
    print(f"Saving {len(sets)} {source} sets to database...")

    for set_data in sets:
        try:
            enhanced_data = enhance_set_data(set_data, source)

            # Generate unique ID
            unique_id = generate_unique_id(source, enhanced_data["set_number"])

            # Insert with enhanced schema
            conn.execute(
                """
                INSERT OR REPLACE INTO lego_data 
                (id, source, name, details, set_number, year, theme, pieces, minifigures, price, rating) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                [
                    unique_id,
                    source,
                    enhanced_data["name"],
                    json.dumps(enhanced_data, ensure_ascii=False),
                    enhanced_data["set_number"],
                    enhanced_data["year"],
                    enhanced_data["theme"],
                    enhanced_data["pieces"],
                    enhanced_data["minifigures"],
                    enhanced_data["price"],
                    enhanced_data["rating"],
                ],
            )

        except Exception as e:
            print(
                f"  Error saving set {enhanced_data.get('set_number', 'unknown')}: {e}"
            )
            continue

    print(f"  Successfully saved {len(sets)} {source} sets")


def create_faiss_index_enhanced(conn):
    """Create enhanced FAISS index with better text processing"""
    print("Creating enhanced FAISS index...")

    # Get all records with enhanced data
    result = conn.execute(
        """
        SELECT details, name, theme, year, pieces 
        FROM lego_data 
        ORDER BY year DESC, pieces DESC
    """
    ).fetchall()

    if not result:
        print("⚠️  No data found in database. Cannot create FAISS index.")
        return

    # Create enhanced text representations
    enhanced_texts = []
    for row in result:
        details = json.loads(row[0])
        name = row[1] or ""
        theme = row[2] or ""
        year = row[3] or ""
        pieces = row[4] or ""

        # Create optimized text representation (shorter to avoid token limits)
        enhanced_text = f"LEGO Set: {name} | Theme: {theme} | Year: {year} | Pieces: {pieces} | Details: {json.dumps(details, ensure_ascii=False)[:500]}"
        enhanced_texts.append(enhanced_text)

    print(f"  Creating index for {len(enhanced_texts)} records...")

    try:
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        vectorstore = FAISS.from_texts(enhanced_texts, embeddings)

        # Save the FAISS index
        vectorstore.save_local("./faiss_index")
        print("  Enhanced FAISS index created and saved successfully")

    except Exception as e:
        print(f"  Error creating FAISS index: {e}")


def main():
    """Enhanced main function"""
    print("🧱 Enhanced LEGO Data Loader")
    print("=" * 50)

    # Initialize database
    conn = initialize_database()

    # Fetch theme mappings (commented out for now)
    # themes = fetch_rebrickable_themes()

    # Fetch data from all sources with enhanced limits
    # Skip Rebrickable and BrickOwl for now (need API keys)
    rebrickable_sets = fetch_rebrickable_enhanced(1000)  # Increased to 1000
    brickset_sets = fetch_brickset_enhanced(1000)  # Increased to 1000
    # brickowl_sets = fetch_brickowl_enhanced(200)

    # Save to database
    if rebrickable_sets:
        save_to_database_enhanced(conn, rebrickable_sets, "rebrickable")
    if brickset_sets:
        save_to_database_enhanced(conn, brickset_sets, "brickset")
    # if brickowl_sets:
    #     save_to_database_enhanced(conn, brickowl_sets, "brickowl")

    # Commit changes
    conn.commit()

    # Show enhanced summary
    stats = conn.execute(
        """
        SELECT 
            COUNT(*) as total_records,
            COUNT(DISTINCT source) as sources,
            COUNT(DISTINCT theme) as themes,
            AVG(pieces) as avg_pieces,
            MIN(year) as oldest_year,
            MAX(year) as newest_year
        FROM lego_data
    """
    ).fetchone()

    print("\n📊 Enhanced Summary:")
    print(f"   Total Records: {stats[0]}")
    print(f"   Data Sources: {stats[1]}")
    print(f"   Unique Themes: {stats[2]}")
    print(f"   Average Pieces: {stats[3]:.0f}")
    print(f"   Year Range: {stats[4]} - {stats[5]}")

    # Create enhanced FAISS index
    if stats[0] > 0:
        create_faiss_index_enhanced(conn)

    # Cleanup
    conn.close()
    print("\n✅ Enhanced data loading complete!")


if __name__ == "__main__":
    main()
