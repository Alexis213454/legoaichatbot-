#!/usr/bin/env python3
"""
Debug script to verify all connections and API keys for LEGO RAG system
Run this script to diagnose any setup issues before running the main app.
"""

import os
import sys

import requests
from dotenv import load_dotenv
import duckdb
from datetime import datetime


def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")


def print_success(message):
    """Print a success message"""
    print(f"✅ {message}")


def print_error(message):
    """Print an error message"""
    print(f"❌ {message}")


def print_warning(message):
    """Print a warning message"""
    print(f"⚠️  {message}")


def print_info(message):
    """Print an info message"""
    print(f"ℹ️  {message}")


def check_environment():
    """Check environment variables and .env file"""
    print_header("Environment Check")

    # Load environment variables with Gitpod fallback
    if os.getenv("IN_GITPOD") == "true":
        if os.path.exists(".env.gitpod"):
            print_success(".env.gitpod file found")
            load_dotenv(".env.gitpod")
        else:
            print_warning(
                ".env.gitpod file not found - using system environment variables"
            )
    else:
        if os.path.exists(".env"):
            print_success(".env file found")
            load_dotenv(".env")
        else:
            print_warning(".env file not found - using system environment variables")

    # Check required API keys
    required_keys = {
        "OPENAI_API_KEY": "OpenAI API Key",
        "REBRICKABLE_API_KEY": "Rebrickable API Key",
        "BRICKSET_API_KEY": "Brickset API Key",
        "BRICKSET_USERNAME": "Brickset Username",
        "BRICKSET_PASSWORD": "Brickset Password",
        "BRICKOWL_API_KEY": "BrickOwl API Key",
    }

    missing_keys = []
    for key, description in required_keys.items():
        value = os.getenv(key)
        if value:
            # Mask the key for security
            masked_value = (
                value[:4] + "*" * (len(value) - 8) + value[-4:]
                if len(value) > 8
                else "****"
            )
            print_success(f"{description}: {masked_value}")
        else:
            print_error(f"{description}: NOT FOUND")
            missing_keys.append(key)

    if missing_keys:
        print_warning(
            f"Missing {len(missing_keys)} API keys. Some features may not work."
        )
        return False
    else:
        print_success("All API keys found!")
        return True


def test_openai_connection():
    """Test OpenAI API connection"""
    print_header("OpenAI API Test")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print_error("OpenAI API key not found")
        return False

    try:
        # Test with a simple completion
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 10,
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30,
        )

        if response.status_code == 200:
            print_success("OpenAI API connection successful")
            return True
        else:
            print_error(f"OpenAI API error: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print_error(f"OpenAI API connection failed: {e}")
        return False


def test_rebrickable_connection():
    """Test Rebrickable API connection"""
    print_header("Rebrickable API Test")

    api_key = os.getenv("REBRICKABLE_API_KEY")
    if not api_key:
        print_error("Rebrickable API key not found")
        return False

    try:
        url = "https://rebrickable.com/api/v3/lego/sets/"
        headers = {"Authorization": f"key {api_key}"}
        params = {"page_size": 1}

        response = requests.get(url, headers=headers, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                set_name = data["results"][0].get("name", "Unknown")
                print_success(
                    f"Rebrickable API connection successful - Sample set: {set_name}"
                )
                return True
            else:
                print_error("Rebrickable API returned no results")
                return False
        else:
            print_error(
                f"Rebrickable API error: {response.status_code} - {response.text}"
            )
            return False

    except Exception as e:
        print_error(f"Rebrickable API connection failed: {e}")
        return False


def test_brickset_connection():
    """Test Brickset API connection"""
    print_header("Brickset API Test")

    api_key = os.getenv("BRICKSET_API_KEY")
    username = os.getenv("BRICKSET_USERNAME")
    password = os.getenv("BRICKSET_PASSWORD")

    if not all([api_key, username, password]):
        print_error("Brickset API credentials not found")
        return False

    try:
        # Test login
        login_url = "https://brickset.com/api/v3.asmx/login"
        login_params = {"apiKey": api_key, "username": username, "password": password}

        response = requests.get(login_url, params=login_params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                print_success("Brickset API login successful")
                return True
            else:
                print_error(f"Brickset login failed: {data}")
                return False
        else:
            print_error(f"Brickset API error: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print_error(f"Brickset API connection failed: {e}")
        return False


def test_brickowl_connection():
    """Test BrickOwl API connection"""
    print_header("BrickOwl API Test")

    api_key = os.getenv("BRICKOWL_API_KEY")
    if not api_key:
        print_error("BrickOwl API key not found")
        return False

    try:
        url = "https://api.brickowl.com/v1/catalog/list"
        params = {"key": api_key, "type": "Set", "limit": 1}

        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                set_name = data["results"][0].get("name", "Unknown")
                print_success(
                    f"BrickOwl API connection successful - Sample set: {set_name}"
                )
                return True
            else:
                print_error("BrickOwl API returned no results")
                return False
        else:
            print_error(f"BrickOwl API error: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print_error(f"BrickOwl API connection failed: {e}")
        return False


def test_database_connection():
    """Test DuckDB database connection"""
    print_header("DuckDB Database Test")

    try:
        # Test database connection
        conn = duckdb.connect("lego_data.duckdb")
        print_success("DuckDB connection successful")

        # Check if table exists
        result = conn.execute(
            """
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_name = 'lego_data'
        """
        ).fetchone()

        if result[0] > 0:
            print_success("lego_data table exists")

            # Check record count
            count_result = conn.execute("SELECT COUNT(*) FROM lego_data").fetchone()
            record_count = count_result[0] if count_result else 0
            print_info(f"Database contains {record_count} records")

            # Check data sources
            sources_result = conn.execute(
                """
                SELECT source, COUNT(*) as count 
                FROM lego_data 
                GROUP BY source
            """
            ).fetchall()

            if sources_result:
                print_info("Data sources:")
                for source, count in sources_result:
                    print_info(f"  - {source}: {count} records")
            else:
                print_warning("No data sources found")
        else:
            print_warning("lego_data table does not exist")

        conn.close()
        return True

    except Exception as e:
        print_error(f"DuckDB connection failed: {e}")
        return False


def test_faiss_index():
    """Test FAISS index"""
    print_header("FAISS Index Test")

    faiss_index_path = "./faiss_index"

    if os.path.exists(f"{faiss_index_path}/index.faiss") and os.path.exists(
        f"{faiss_index_path}/index.pkl"
    ):
        print_success("FAISS index files found")

        try:
            # Try to load the index
            from langchain_openai import OpenAIEmbeddings
            from langchain_community.vectorstores import FAISS

            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                print_error("OpenAI API key required to test FAISS index")
                return False

            embeddings = OpenAIEmbeddings(openai_api_key=api_key)
            vectorstore = FAISS.load_local(faiss_index_path, embeddings)

            # Test similarity search
            docs = vectorstore.similarity_search("test", k=1)
            print_success(f"FAISS index loaded successfully - {len(docs)} test results")
            return True

        except Exception as e:
            print_error(f"FAISS index loading failed: {e}")
            return False
    else:
        print_warning("FAISS index files not found")
        return False


def test_python_packages():
    """Test required Python packages"""
    print_header("Python Packages Test")

    required_packages = [
        "streamlit",
        "langchain",
        "langchain_openai",
        "langchain_community",
        "faiss",
        "duckdb",
        "sentence_transformers",
        "numpy",
        "scipy",
        "sklearn",
        "pydantic",
        "requests",
        "python-dotenv",
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print_success(f"{package} - OK")
        except ImportError:
            print_error(f"{package} - MISSING")
            missing_packages.append(package)

    if missing_packages:
        print_warning(f"Missing {len(missing_packages)} packages")
        return False
    else:
        print_success("All required packages installed!")
        return True


def generate_summary_report(results):
    """Generate a summary report"""
    print_header("Summary Report")

    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    failed_tests = total_tests - passed_tests

    print("📊 Test Results:")
    print(f"   Total Tests: {total_tests}")
    print(f"   ✅ Passed: {passed_tests}")
    print(f"   ❌ Failed: {failed_tests}")
    print(f"   📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")

    if failed_tests == 0:
        print_success("🎉 All tests passed! Your setup is ready to go.")
        return True
    else:
        print_warning("⚠️  Some tests failed. Please check the issues above.")

        # Provide specific recommendations
        print("\n🔧 Recommendations:")
        if not results.get("environment", False):
            print("   - Check your .env file and API keys")
        if not results.get("openai", False):
            print("   - Verify your OpenAI API key and billing status")
        if not results.get("database", False):
            print("   - Run the data loader: python load_data.py")
        if not results.get("faiss", False):
            print("   - Run the data loader to create FAISS index")
        if not results.get("packages", False):
            print("   - Install missing packages: uv sync")

        return False


def test_performance_metrics():
    """Test performance-related configurations"""
    print_header("Performance Metrics Test")

    # Check uv configuration
    try:
        import tomllib

        with open("pyproject.toml", "rb") as f:
            config = tomllib.load(f)

        uv_config = config.get("tool", {}).get("uv", {})
        if uv_config.get("resolution") == "highest":
            print_success("uv: Fast resolution enabled")
        else:
            print_warning("uv: Consider enabling fast resolution")

        if uv_config.get("index-strategy") == "unsafe-best-match":
            print_success("uv: Parallel downloads enabled")
        else:
            print_warning("uv: Consider enabling parallel downloads")

    except Exception as e:
        print_warning(f"Could not check uv config: {e}")

    # Check cache directories
    cache_dirs = [
        "/workspace/.cache/pip",
        "/workspace/.cache/uv",
        ".cache/pip",
        ".cache/uv",
    ]
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            print_success(f"Cache directory exists: {cache_dir}")
        else:
            print_info(f"Cache directory not found: {cache_dir}")

    # Check environment variables
    env_vars = ["PIP_CACHE_DIR", "UV_CACHE_DIR", "DOCKER_BUILDKIT"]
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print_success(f"Environment variable set: {var}={value}")
        else:
            print_info(f"Environment variable not set: {var}")

    return True


def main():
    """Main debug function"""
    print("🧱 LEGO RAG System - Debug Setup")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Run all tests
    results = {}

    results["environment"] = check_environment()
    results["packages"] = test_python_packages()
    results["openai"] = test_openai_connection()
    results["rebrickable"] = test_rebrickable_connection()
    results["brickset"] = test_brickset_connection()
    results["brickowl"] = test_brickowl_connection()
    results["database"] = test_database_connection()
    results["faiss"] = test_faiss_index()
    results["performance"] = test_performance_metrics()

    # Generate summary
    success = generate_summary_report(results)

    print(f"\n{'='*60}")
    if success:
        print("🚀 Ready to run: streamlit run app.py")
    else:
        print("🔧 Please fix the issues above before running the app")
    print(f"{'='*60}")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
