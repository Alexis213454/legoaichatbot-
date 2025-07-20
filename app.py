import os
import json
import plotly.express as px

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
import duckdb
import streamlit as st
import pandas as pd


# Load environment variables with Gitpod fallback
if os.getenv("IN_GITPOD") == "true":
    load_dotenv(".env.gitpod")
else:
    load_dotenv(".env")  # Your default dev secrets

openai_api_key = os.getenv("OPENAI_API_KEY")

# Page configuration
st.set_page_config(
    page_title="🧱 LEGO RAG Search Engine",
    page_icon="🧱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
<style>
    .main-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #FF6B6B;
    }
    .search-box {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .result-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .theme-filter {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


# Initialize database and models
@st.cache_resource
def initialize_system():
    """Initialize the system with caching"""
    try:
        conn = duckdb.connect("lego_data.duckdb")
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        
        # Load FAISS index with security setting for pickle files
        import pickle
        import faiss
        from langchain_community.vectorstores import FAISS
        
        # Set allow_dangerous_deserialization for trusted local files
        vectorstore = FAISS.load_local(
            "./faiss_index", 
            embeddings,
            allow_dangerous_deserialization=True
        )
        llm = ChatOpenAI(model_name="gpt-4", openai_api_key=openai_api_key)
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever()
        )
        return conn, vectorstore, qa_chain
    except Exception as e:
        st.error(f"❌ System initialization failed: {e}")
        return None, None, None


# Initialize system
conn, vectorstore, qa_chain = initialize_system()

if conn is None:
    st.error("❌ Please ensure your data is loaded and API keys are configured.")
    st.stop()

# Cache database queries
@st.cache_data
def get_themes():
    """Get distinct themes from database"""
    try:
        if conn is None:
            return ["All Themes"]
        themes = conn.execute(
            "SELECT DISTINCT theme FROM lego_data WHERE theme IS NOT NULL"
        ).fetchall()
        return ["All Themes"] + [theme[0] for theme in themes]
    except Exception as e:
        st.error(f"Error fetching themes: {e}")
        return ["All Themes"]

@st.cache_data
def get_years():
    """Get distinct years from database"""
    try:
        if conn is None:
            return []
        years = conn.execute(
            "SELECT DISTINCT year FROM lego_data WHERE year IS NOT NULL ORDER BY year"
        ).fetchall()
        return [year[0] for year in years]
    except Exception as e:
        st.error(f"Error fetching years: {e}")
        return []

@st.cache_data
def get_database_stats():
    """Get database statistics"""
    try:
        if conn is None:
            return [0, 0, 0, 0, 0, 0, 0]
        stats = conn.execute(
            """
            SELECT 
                COUNT(*) as total_records,
                COUNT(DISTINCT source) as sources,
                COUNT(DISTINCT theme) as themes,
                AVG(pieces) as avg_pieces,
                MIN(year) as oldest_year,
                MAX(year) as newest_year,
                AVG(price) as avg_price
            FROM lego_data
        """
        ).fetchone()
        return stats
    except Exception as e:
        st.error(f"Error fetching database stats: {e}")
        return [0, 0, 0, 0, 0, 0, 0]

@st.cache_data
def get_theme_distribution():
    """Get theme distribution data"""
    try:
        if conn is None:
            return []
        theme_data = conn.execute(
            """
            SELECT theme, COUNT(*) as count 
            FROM lego_data 
            WHERE theme IS NOT NULL 
            GROUP BY theme 
            ORDER BY count DESC 
            LIMIT 10
        """
        ).fetchall()
        return theme_data
    except Exception as e:
        st.error(f"Error fetching theme distribution: {e}")
        return []

@st.cache_data
def get_year_distribution():
    """Get year distribution data"""
    try:
        if conn is None:
            return []
        year_data = conn.execute(
            """
            SELECT year, COUNT(*) as count 
            FROM lego_data 
            WHERE year IS NOT NULL 
            GROUP BY year 
            ORDER BY year
        """
        ).fetchall()
        return year_data
    except Exception as e:
        st.error(f"Error fetching year distribution: {e}")
        return []


# Performance monitoring
@st.cache_data
def get_performance_metrics():
    """Get system performance metrics"""
    try:
        # Database metrics
        if conn is None:
            db_count = 0
        else:
            db_count = conn.execute("SELECT COUNT(*) FROM lego_data").fetchone()[0]

        # Cache status
        cache_dirs = [
            "/workspace/.cache/pip",
            "/workspace/.cache/uv",
            ".cache/pip",
            ".cache/uv",
        ]
        cache_status = {}
        for cache_dir in cache_dirs:
            cache_status[cache_dir] = os.path.exists(cache_dir)

        # Environment info
        env_info = {
            "RAG_MODE": os.getenv("RAG_MODE", "dev"),
            "PIP_CACHE_DIR": os.getenv("PIP_CACHE_DIR"),
            "UV_CACHE_DIR": os.getenv("UV_CACHE_DIR"),
            "IN_GITPOD": os.getenv("IN_GITPOD", "false"),
        }

        return {
            "db_records": db_count,
            "cache_status": cache_status,
            "env_info": env_info,
        }
    except Exception as e:
        return {"error": str(e)}


# Header
st.markdown(
    """
<div class="main-header">
    <h1>🧱 LEGO RAG Search Engine</h1>
    <p>Discover LEGO sets with AI-powered semantic search across multiple sources</p>
</div>
""",
    unsafe_allow_html=True,
)

# Sidebar with enhanced features
with st.sidebar:
    st.header("⚙️ Search Configuration")

    # Search parameters
    search_k = st.slider("Number of results", min_value=1, max_value=20, value=5)
    similarity_threshold = st.slider(
        "Similarity threshold", min_value=0.0, max_value=1.0, value=0.7, step=0.1
    )

    # Advanced filters
    with st.expander("🔍 Advanced Filters"):
        # Theme filter
        theme_options = get_themes()
        selected_theme = st.selectbox("Theme", theme_options)

        # Year range
        year_options = get_years()
        if year_options:
            year_range = st.select_slider(
                "Year Range",
                options=year_options,
                value=(min(year_options), max(year_options)),
            )

        # Piece count range
        pieces_range = st.slider("Piece Count Range", 0, 5000, (0, 5000))

        # Price range
        price_range = st.slider("Price Range ($)", 0.0, 1000.0, (0.0, 1000.0))

    # Search history
    with st.expander("📚 Search History"):
        if "search_history" not in st.session_state:
            st.session_state.search_history = []

        for i, query in enumerate(st.session_state.search_history[-5:]):
            if st.button(f"🔍 {query[:30]}...", key=f"history_{i}"):
                st.session_state.current_query = query
                st.rerun()

    # Performance dashboard
    with st.expander("⚡ Performance Dashboard"):
        metrics = get_performance_metrics()

        if "error" not in metrics:
            st.metric("Database Records", metrics["db_records"])

            # Cache status
            st.write("**Cache Status:**")
            for cache_dir, exists in metrics["cache_status"].items():
                status = "✅" if exists else "❌"
                st.write(f"{status} {cache_dir}")

            # Environment info
            st.write("**Environment:**")
            st.write(f"Mode: {metrics['env_info']['RAG_MODE']}")
            st.write(f"Gitpod: {metrics['env_info']['IN_GITPOD']}")
        else:
            st.error(f"Error loading metrics: {metrics['error']}")

    # Quick actions
    st.markdown("---")
    st.markdown("**🚀 Quick Actions**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 View Analytics", type="secondary"):
            st.session_state.show_analytics = True

    with col2:
        if st.button("🔄 Refresh Data", type="secondary"):
            import subprocess

            with st.spinner("Refreshing data..."):
                result = subprocess.run(
                    ["python", "load_data.py"], capture_output=True, text=True
                )
                st.success("Data refreshed!")

# Main content area
col1, col2 = st.columns([3, 1])

with col1:
    # Enhanced search interface
    st.markdown('<div class="search-box">', unsafe_allow_html=True)

    # Search input with suggestions
    query = st.text_input(
        "🔍 Ask about LEGO sets:",
        placeholder="e.g., What are the best Star Wars LEGO sets?",
        key="search_input",
    )

    # Search suggestions
    suggestions = [
        "Star Wars sets with many pieces",
        "Recent 2024 releases",
        "Sets for beginners",
        "Expensive collector sets",
        "Technic vehicles",
        "Harry Potter themed sets",
    ]

    st.markdown("**💡 Quick suggestions:**")
    suggestion_cols = st.columns(3)
    for i, suggestion in enumerate(suggestions):
        with suggestion_cols[i % 3]:
            if st.button(suggestion, key=f"sugg_{i}"):
                query = suggestion
                st.session_state.current_query = suggestion
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    # Search button
    search_button = st.button("🚀 Search", type="primary", use_container_width=True)

    # Voice input (placeholder for future enhancement)
    if st.button("🎤 Voice Search", use_container_width=True):
        st.info("Voice search coming soon!")

# Handle search
if (query and search_button) or "current_query" in st.session_state:
    if "current_query" in st.session_state:
        query = st.session_state.current_query
        del st.session_state.current_query

    # Add to search history
    if query not in st.session_state.search_history:
        st.session_state.search_history.append(query)

    with st.spinner("🔍 Searching LEGO database..."):
        try:
            # Get AI response
            response = qa_chain.run(query)

            # Display results in tabs
            tab1, tab2, tab3 = st.tabs(
                ["🤖 AI Response", "📚 Source Documents", "📊 Analytics"]
            )

            with tab1:
                st.subheader("AI-Generated Answer")
                st.markdown(response)

                # Add feedback buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("👍 Helpful"):
                        st.success("Thanks for your feedback!")
                with col2:
                    if st.button("👎 Not Helpful"):
                        st.info("We'll improve our responses!")
                with col3:
                    if st.button("🔄 Regenerate"):
                        st.rerun()

            with tab2:
                st.subheader(f"📚 Top {search_k} Related Records")

                # Get search results
                docs = vectorstore.similarity_search_with_score(query, k=search_k)

                # Filter by similarity threshold
                filtered_docs = [
                    (doc, score) for doc, score in docs if score > similarity_threshold
                ]

                if not filtered_docs:
                    st.warning(
                        "No results found with the current similarity threshold. Try lowering it."
                    )
                else:
                    for i, (doc, score) in enumerate(filtered_docs, 1):
                        with st.expander(f"Record {i} (Score: {score:.3f})"):
                            try:
                                data = json.loads(doc.page_content)

                                # Create a nice card layout
                                col1, col2 = st.columns([2, 1])

                                with col1:
                                    st.markdown(
                                        f"**{data.get('name', 'Unknown Set')}**"
                                    )
                                    st.markdown(
                                        f"**Set Number:** {data.get('set_number', 'N/A')}"
                                    )
                                    st.markdown(
                                        f"**Theme:** {data.get('theme', 'N/A')}"
                                    )
                                    st.markdown(f"**Year:** {data.get('year', 'N/A')}")

                                with col2:
                                    if data.get("pieces"):
                                        st.metric("Pieces", data["pieces"])
                                    if data.get("price"):
                                        st.metric("Price", f"${data['price']}")
                                    if data.get("rating"):
                                        st.metric("Rating", f"{data['rating']}/5")

                                # Show full data in collapsible section
                                with st.expander("📋 Full Details"):
                                    st.json(data)

                            except Exception:
                                st.text(doc.page_content[:500] + "...")

            with tab3:
                st.subheader("📊 Search Analytics")

                # Get analytics data
                analytics_data = []
                for doc, score in filtered_docs:
                    try:
                        data = json.loads(doc.page_content)
                        analytics_data.append(
                            {
                                "name": data.get("name", "Unknown"),
                                "theme": data.get("theme", "Unknown"),
                                "year": data.get("year", 0),
                                "pieces": data.get("pieces", 0),
                                "price": data.get("price", 0),
                                "score": score,
                            }
                        )
                    except Exception:
                        continue

                if analytics_data:
                    df = pd.DataFrame(analytics_data)

                    # Create visualizations
                    col1, col2 = st.columns(2)

                    with col1:
                        # Theme distribution
                        theme_counts = df["theme"].value_counts()
                        fig_theme = px.pie(
                            values=theme_counts.values,
                            names=theme_counts.index,
                            title="Results by Theme",
                        )
                        st.plotly_chart(fig_theme, use_container_width=True)

                    with col2:
                        # Year distribution
                        fig_year = px.histogram(
                            df, x="year", title="Results by Year", nbins=10
                        )
                        st.plotly_chart(fig_year, use_container_width=True)

                    # Pieces vs Price scatter plot
                    fig_scatter = px.scatter(
                        df,
                        x="pieces",
                        y="price",
                        hover_data=["name", "theme"],
                        title="Pieces vs Price",
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True)

                    # Summary statistics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Results", len(df))
                    with col2:
                        st.metric("Avg Pieces", f"{df['pieces'].mean():.0f}")
                    with col3:
                        st.metric("Avg Price", f"${df['price'].mean():.2f}")
                    with col4:
                        st.metric("Avg Score", f"{df['score'].mean():.3f}")

        except Exception as e:
            st.error(f"❌ Search failed: {str(e)}")
            st.exception(e)

# Show analytics dashboard if requested
if st.session_state.get("show_analytics", False):
    st.session_state.show_analytics = False

    st.subheader("📊 LEGO Database Analytics")

    # Get database statistics using cached function
    stats = get_database_stats()

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", stats[0])
    with col2:
        st.metric("Data Sources", stats[1])
    with col3:
        st.metric("Unique Themes", stats[2])
    with col4:
        st.metric("Avg Pieces", f"{stats[3]:.0f}")

    # Create visualizations
    col1, col2 = st.columns(2)

    with col1:
        # Theme distribution using cached function
        theme_data = get_theme_distribution()

        if theme_data:
            df_themes = pd.DataFrame(theme_data, columns=["Theme", "Count"])
            fig = px.bar(df_themes, x="Theme", y="Count", title="Top 10 Themes")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Year distribution using cached function
        year_data = get_year_distribution()

        if year_data:
            df_years = pd.DataFrame(year_data, columns=["Year", "Count"])
            fig = px.line(df_years, x="Year", y="Count", title="Sets by Year")
            st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    """
<div style="text-align: center; color: #666;">
    <p>🧱 Built with ❤️ for the LEGO community | Powered by AI & Semantic Search</p>
</div>
""",
    unsafe_allow_html=True,
)

# Note: Connection is managed by Streamlit's caching system
# Don't close it here as cached functions may still need it
