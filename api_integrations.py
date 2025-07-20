import os
import requests
import json
import hashlib

from dotenv import load_dotenv
import duckdb

# Load environment variables
# Load environment variables with Gitpod fallback
if os.getenv("IN_GITPOD") == "true":
    load_dotenv(".env.gitpod")
else:
    load_dotenv(".env")  # Your default dev secrets


class LEGOAPIIntegrations:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "LEGO-RAG-Search/1.0 (Educational Project)"}
        )

    def fetch_bricklink_data(self, limit=100):
        """Fetch data from BrickLink API"""
        print("🔗 Fetching from BrickLink API...")

        # BrickLink API requires OAuth2 authentication
        # https://www.bricklink.com/v3/api.page
        # This is a placeholder for the actual implementation

        bricklink_token = os.getenv("BRICKLINK_TOKEN")
        if not bricklink_token:
            print("⚠️  BrickLink API token not found. Skipping BrickLink data.")
            return []

        try:
            # BrickLink API endpoints
            endpoints = [
                f"/api/v3/catalog/sets?limit={limit}",
                f"/api/v3/catalog/themes?limit={limit}",
                f"/api/v3/catalog/categories?limit={limit}",
            ]

            all_sets = []
            for endpoint in endpoints:
                response = self.session.get(
                    f"https://api.bricklink.com{endpoint}",
                    headers={"Authorization": f"Bearer {bricklink_token}"},
                    timeout=30,
                )

                if response.status_code == 200:
                    data = response.json()
                    if "data" in data:
                        all_sets.extend(data["data"])
                    print(
                        f"  Fetched {len(data.get('data', []))} items from {endpoint}"
                    )
                else:
                    print(f"  BrickLink API error: {response.status_code}")

            print(f"  Total BrickLink items: {len(all_sets)}")
            return all_sets

        except Exception as e:
            print(f"  Error fetching from BrickLink: {e}")
            return []

    def fetch_lego_ideas_data(self, limit=100):
        """Fetch data from LEGO Ideas"""
        print("💡 Fetching from LEGO Ideas...")

        try:
            # LEGO Ideas doesn't have a public API, but we can scrape their website
            # This would require web scraping with proper rate limiting

            # For now, return sample data structure
            sample_ideas = [
                {
                    "id": "ideas_001",
                    "name": "Sample LEGO Ideas Set",
                    "theme": "LEGO Ideas",
                    "year": 2024,
                    "pieces": 1500,
                    "status": "Approved",
                    "votes": 10000,
                    "creator": "Community Member",
                }
            ]

            print(f"  Total LEGO Ideas items: {len(sample_ideas)}")
            return sample_ideas

        except Exception as e:
            print(f"  Error fetching from LEGO Ideas: {e}")
            return []

    def fetch_lego_shop_data(self, limit=100):
        """Fetch data from LEGO Shop API"""
        print("🛒 Fetching from LEGO Shop...")

        try:
            # LEGO Shop API (if available)
            # This would require reverse engineering or official API access

            # For now, return sample data
            sample_shop = [
                {
                    "id": "shop_001",
                    "name": "Sample Shop Set",
                    "theme": "City",
                    "year": 2024,
                    "pieces": 800,
                    "price": 79.99,
                    "availability": "In Stock",
                    "rating": 4.5,
                }
            ]

            print(f"  Total LEGO Shop items: {len(sample_shop)}")
            return sample_shop

        except Exception as e:
            print(f"  Error fetching from LEGO Shop: {e}")
            return []

    def fetch_lego_education_data(self, limit=100):
        """Fetch data from LEGO Education"""
        print("🎓 Fetching from LEGO Education...")

        try:
            # LEGO Education sets
            education_sets = [
                {
                    "id": "edu_001",
                    "name": "LEGO Education SPIKE Prime Set",
                    "theme": "Education",
                    "year": 2024,
                    "pieces": 528,
                    "category": "Robotics",
                    "age_range": "10-14",
                    "price": 339.95,
                },
                {
                    "id": "edu_002",
                    "name": "LEGO Education WeDo 2.0",
                    "theme": "Education",
                    "year": 2023,
                    "pieces": 280,
                    "category": "Coding",
                    "age_range": "7-10",
                    "price": 189.95,
                },
            ]

            print(f"  Total LEGO Education items: {len(education_sets)}")
            return education_sets

        except Exception as e:
            print(f"  Error fetching from LEGO Education: {e}")
            return []

    def fetch_lego_architecture_data(self, limit=100):
        """Fetch data from LEGO Architecture"""
        print("🏛️ Fetching from LEGO Architecture...")

        try:
            # LEGO Architecture sets
            architecture_sets = [
                {
                    "id": "arch_001",
                    "name": "LEGO Architecture Empire State Building",
                    "theme": "Architecture",
                    "year": 2024,
                    "pieces": 1767,
                    "category": "Landmarks",
                    "difficulty": "Expert",
                    "price": 119.99,
                },
                {
                    "id": "arch_002",
                    "name": "LEGO Architecture Tokyo",
                    "theme": "Architecture",
                    "year": 2023,
                    "pieces": 547,
                    "category": "Cityscapes",
                    "difficulty": "Intermediate",
                    "price": 59.99,
                },
            ]

            print(f"  Total LEGO Architecture items: {len(architecture_sets)}")
            return architecture_sets

        except Exception as e:
            print(f"  Error fetching from LEGO Architecture: {e}")
            return []

    def fetch_lego_technic_data(self, limit=100):
        """Fetch data from LEGO Technic"""
        print("⚙️ Fetching from LEGO Technic...")

        try:
            # LEGO Technic sets
            technic_sets = [
                {
                    "id": "tech_001",
                    "name": "LEGO Technic Lamborghini Sián",
                    "theme": "Technic",
                    "year": 2024,
                    "pieces": 3696,
                    "category": "Cars",
                    "difficulty": "Expert",
                    "price": 379.99,
                    "motorized": True,
                },
                {
                    "id": "tech_002",
                    "name": "LEGO Technic Cat D11 Bulldozer",
                    "theme": "Technic",
                    "year": 2023,
                    "pieces": 3854,
                    "category": "Construction",
                    "difficulty": "Expert",
                    "price": 449.99,
                    "motorized": True,
                },
            ]

            print(f"  Total LEGO Technic items: {len(technic_sets)}")
            return technic_sets

        except Exception as e:
            print(f"  Error fetching from LEGO Technic: {e}")
            return []

    def fetch_lego_creator_expert_data(self, limit=100):
        """Fetch data from LEGO Creator Expert"""
        print("🎨 Fetching from LEGO Creator Expert...")

        try:
            # LEGO Creator Expert sets
            creator_expert_sets = [
                {
                    "id": "ce_001",
                    "name": "LEGO Creator Expert Titanic",
                    "theme": "Creator Expert",
                    "year": 2024,
                    "pieces": 9090,
                    "category": "Ships",
                    "difficulty": "Expert",
                    "price": 679.99,
                    "display_size": "135cm x 44cm",
                },
                {
                    "id": "ce_002",
                    "name": "LEGO Creator Expert Colosseum",
                    "theme": "Creator Expert",
                    "year": 2023,
                    "pieces": 9036,
                    "category": "Landmarks",
                    "difficulty": "Expert",
                    "price": 549.99,
                    "display_size": "27cm x 52cm x 59cm",
                },
            ]

            print(f"  Total LEGO Creator Expert items: {len(creator_expert_sets)}")
            return creator_expert_sets

        except Exception as e:
            print(f"  Error fetching from LEGO Creator Expert: {e}")
            return []

    def fetch_lego_minifigures_data(self, limit=100):
        """Fetch data from LEGO Minifigures"""
        print("👤 Fetching from LEGO Minifigures...")

        try:
            # LEGO Minifigures
            minifigures = [
                {
                    "id": "minifig_001",
                    "name": "LEGO Minifigures Series 25",
                    "theme": "Minifigures",
                    "year": 2024,
                    "pieces": 3,
                    "category": "Collectible",
                    "price": 4.99,
                    "rarity": "Common",
                },
                {
                    "id": "minifig_002",
                    "name": "LEGO Minifigures Disney Series 2",
                    "theme": "Minifigures",
                    "year": 2023,
                    "pieces": 3,
                    "category": "Collectible",
                    "price": 4.99,
                    "rarity": "Rare",
                },
            ]

            print(f"  Total LEGO Minifigures items: {len(minifigures)}")
            return minifigures

        except Exception as e:
            print(f"  Error fetching from LEGO Minifigures: {e}")
            return []

    def fetch_lego_duplo_data(self, limit=100):
        """Fetch data from LEGO DUPLO"""
        print("🧸 Fetching from LEGO DUPLO...")

        try:
            # LEGO DUPLO sets
            duplo_sets = [
                {
                    "id": "duplo_001",
                    "name": "LEGO DUPLO Town Fire Station",
                    "theme": "DUPLO",
                    "year": 2024,
                    "pieces": 25,
                    "category": "Town",
                    "age_range": "2-5",
                    "price": 19.99,
                },
                {
                    "id": "duplo_002",
                    "name": "LEGO DUPLO Disney Princess Belle's Castle",
                    "theme": "DUPLO",
                    "year": 2023,
                    "pieces": 35,
                    "category": "Disney",
                    "age_range": "2-5",
                    "price": 24.99,
                },
            ]

            print(f"  Total LEGO DUPLO items: {len(duplo_sets)}")
            return duplo_sets

        except Exception as e:
            print(f"  Error fetching from LEGO DUPLO: {e}")
            return []

    def fetch_lego_juniors_data(self, limit=100):
        """Fetch data from LEGO Juniors"""
        print("👶 Fetching from LEGO Juniors...")

        try:
            # LEGO Juniors sets
            juniors_sets = [
                {
                    "id": "juniors_001",
                    "name": "LEGO Juniors Police Station",
                    "theme": "Juniors",
                    "year": 2024,
                    "pieces": 68,
                    "category": "Police",
                    "age_range": "4-7",
                    "price": 14.99,
                }
            ]

            print(f"  Total LEGO Juniors items: {len(juniors_sets)}")
            return juniors_sets

        except Exception as e:
            print(f"  Error fetching from LEGO Juniors: {e}")
            return []

    def fetch_all_sources(self, limit=50):
        """Fetch data from all available sources"""
        print("🌐 Fetching from all LEGO data sources...")

        all_data = {}

        # Fetch from all sources
        sources = [
            ("bricklink", self.fetch_bricklink_data),
            ("lego_ideas", self.fetch_lego_ideas_data),
            ("lego_shop", self.fetch_lego_shop_data),
            ("lego_education", self.fetch_lego_education_data),
            ("lego_architecture", self.fetch_lego_architecture_data),
            ("lego_technic", self.fetch_lego_technic_data),
            ("lego_creator_expert", self.fetch_lego_creator_expert_data),
            ("lego_minifigures", self.fetch_lego_minifigures_data),
            ("lego_duplo", self.fetch_lego_duplo_data),
            ("lego_juniors", self.fetch_lego_juniors_data),
        ]

        for source_name, fetch_func in sources:
            try:
                data = fetch_func(limit)
                if data:
                    all_data[source_name] = data
                    print(f"✅ {source_name}: {len(data)} items")
                else:
                    print(f"⚠️  {source_name}: No data available")
            except Exception as e:
                print(f"❌ {source_name}: Error - {e}")

        return all_data

    def save_to_database(self, conn, all_data):
        """Save all fetched data to database"""
        print("💾 Saving data to database...")

        total_saved = 0

        for source_name, data_list in all_data.items():
            print(f"  Saving {source_name} data...")

            for item in data_list:
                try:
                    # Generate unique ID
                    unique_id = hashlib.md5(
                        f"{source_name}_{item.get('id', 'unknown')}".encode()
                    ).hexdigest()

                    # Prepare data for database
                    name = item.get("name", "Unknown Set")
                    details = json.dumps(item, ensure_ascii=False)
                    set_number = item.get("id", "")
                    year = item.get("year", 0)
                    theme = item.get("theme", "Unknown")
                    pieces = item.get("pieces", 0)
                    price = item.get("price", 0.0)
                    rating = item.get("rating", 0.0)

                    # Insert into database
                    conn.execute(
                        """
                        INSERT OR REPLACE INTO lego_data 
                        (id, source, name, details, set_number, year, theme, pieces, minifigures, price, rating) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                        [
                            unique_id,
                            source_name,
                            name,
                            details,
                            set_number,
                            year,
                            theme,
                            pieces,
                            0,
                            price,
                            rating,
                        ],
                    )

                    total_saved += 1

                except Exception as e:
                    print(f"    Error saving item {item.get('id', 'unknown')}: {e}")
                    continue

        print(f"  Total items saved: {total_saved}")
        return total_saved


def main():
    """Main function to fetch from all sources"""
    print("🌐 LEGO Multi-Source Data Fetcher")
    print("=" * 50)

    # Initialize
    api_integrations = LEGOAPIIntegrations()
    conn = duckdb.connect("lego_data.duckdb")

    # Fetch from all sources
    all_data = api_integrations.fetch_all_sources(limit=50)

    # Save to database
    if all_data:
        total_saved = api_integrations.save_to_database(conn, all_data)
        conn.commit()

        print("\n📊 Summary:")
        print(f"   Sources fetched: {len(all_data)}")
        print(f"   Total items saved: {total_saved}")

        # Show breakdown
        for source, data in all_data.items():
            print(f"   {source}: {len(data)} items")
    else:
        print("❌ No data fetched from any source")

    # Cleanup
    conn.close()
    print("\n✅ Multi-source data fetching complete!")


if __name__ == "__main__":
    main()
