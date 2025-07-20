import os
import json
import duckdb
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

from langchain_openai import ChatOpenAI
import streamlit as st

# Load environment variables
# Load environment variables with Gitpod fallback
if os.getenv("IN_GITPOD") == "true":
    load_dotenv(".env.gitpod")
else:
    load_dotenv(".env")  # Your default dev secrets
openai_api_key = os.getenv("OPENAI_API_KEY")


class SearchOptimizer:
    def __init__(self):
        self.conn = duckdb.connect("lego_data.duckdb")
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.vectorstore = FAISS.load_local("./faiss_index", self.embeddings)

    def test_search_parameters(
        self, query, k_values=[3, 5, 10], similarity_thresholds=[0.7, 0.8, 0.9]
    ):
        """Test different search parameters"""
        results = {}

        for k in k_values:
            for threshold in similarity_thresholds:
                docs = self.vectorstore.similarity_search_with_score(query, k=k)
                # Filter by similarity threshold
                filtered_docs = [doc for doc, score in docs if score > threshold]

                results[f"k={k}, threshold={threshold}"] = {
                    "docs": filtered_docs,
                    "count": len(filtered_docs),
                    "avg_score": (
                        sum(score for _, score in docs) / len(docs) if docs else 0
                    ),
                }

        return results

    def create_enhanced_retriever(self, search_type="hybrid"):
        """Create enhanced retriever with different strategies"""

        if search_type == "hybrid":
            # Combine semantic and keyword search
            return self._create_hybrid_retriever()
        elif search_type == "contextual":
            # Use contextual compression
            return self._create_contextual_retriever()
        elif search_type == "filtered":
            # Use filtered search
            return self._create_filtered_retriever()
        else:
            return self.vectorstore.as_retriever()

    def _create_hybrid_retriever(self):
        """Create hybrid semantic + keyword retriever"""
        # This would combine FAISS with traditional keyword search
        # For now, return enhanced FAISS retriever
        return self.vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 10, "score_threshold": 0.8},
        )

    def _create_contextual_retriever(self):
        """Create contextual compression retriever"""
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)
        compressor = LLMChainExtractor.from_llm(llm)

        base_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 10})
        return ContextualCompressionRetriever(
            base_compressor=compressor, base_retriever=base_retriever
        )

    def _create_filtered_retriever(self):
        """Create filtered retriever"""
        # This would allow filtering by theme, year, pieces, etc.
        return self.vectorstore.as_retriever(search_kwargs={"k": 10, "filter": {}})

    def optimize_for_query_type(self, query):
        """Optimize search based on query type"""

        # Analyze query type
        query_lower = query.lower()

        if any(
            word in query_lower
            for word in ["star wars", "marvel", "harry potter", "disney"]
        ):
            # Theme-specific query
            return self._optimize_theme_search(query)
        elif any(
            word in query_lower for word in ["big", "large", "small", "pieces", "parts"]
        ):
            # Size-specific query
            return self._optimize_size_search(query)
        elif any(
            word in query_lower for word in ["2024", "2023", "2022", "recent", "old"]
        ):
            # Year-specific query
            return self._optimize_year_search(query)
        elif any(
            word in query_lower for word in ["expensive", "cheap", "price", "cost"]
        ):
            # Price-specific query
            return self._optimize_price_search(query)
        else:
            # General query
            return self._optimize_general_search(query)

    def _optimize_theme_search(self, query):
        """Optimize for theme-specific searches"""
        return self.vectorstore.as_retriever(
            search_kwargs={"k": 15, "score_threshold": 0.7}
        )

    def _optimize_size_search(self, query):
        """Optimize for size-specific searches"""
        return self.vectorstore.as_retriever(
            search_kwargs={"k": 20, "score_threshold": 0.6}
        )

    def _optimize_year_search(self, query):
        """Optimize for year-specific searches"""
        return self.vectorstore.as_retriever(
            search_kwargs={"k": 10, "score_threshold": 0.8}
        )

    def _optimize_price_search(self, query):
        """Optimize for price-specific searches"""
        return self.vectorstore.as_retriever(
            search_kwargs={"k": 12, "score_threshold": 0.75}
        )

    def _optimize_general_search(self, query):
        """Optimize for general searches"""
        return self.vectorstore.as_retriever(
            search_kwargs={"k": 8, "score_threshold": 0.8}
        )

    def get_search_analytics(self, query, results):
        """Analyze search results quality"""
        analytics = {
            "query_length": len(query.split()),
            "result_count": len(results),
            "themes_found": set(),
            "years_found": set(),
            "avg_pieces": 0,
            "data_quality_score": 0,
        }

        pieces_list = []
        quality_scores = []

        for doc in results:
            try:
                data = json.loads(doc.page_content)
                analytics["themes_found"].add(data.get("theme", "Unknown"))
                analytics["years_found"].add(data.get("year", "Unknown"))

                pieces = data.get("pieces", 0)
                if pieces:
                    pieces_list.append(pieces)

                quality_score = data.get("data_quality_score", 0)
                if quality_score:
                    quality_scores.append(quality_score)

            except Exception:
                continue

        if pieces_list:
            analytics["avg_pieces"] = sum(pieces_list) / len(pieces_list)
        if quality_scores:
            analytics["data_quality_score"] = sum(quality_scores) / len(quality_scores)

        analytics["themes_found"] = len(analytics["themes_found"])
        analytics["years_found"] = len(analytics["years_found"])

        return analytics


def main():
    """Main function for search optimization"""
    st.title("🔍 Search Optimization Tool")

    optimizer = SearchOptimizer()

    # Test queries
    test_queries = [
        "Star Wars LEGO sets",
        "Big sets with many pieces",
        "Recent 2024 releases",
        "Expensive collector sets",
        "Sets for kids",
        "Technic vehicles",
    ]

    st.subheader("Test Search Parameters")

    query = st.selectbox("Choose a test query:", test_queries)
    custom_query = st.text_input("Or enter your own query:")

    if custom_query:
        query = custom_query

    if st.button("🔍 Test Search Parameters"):
        with st.spinner("Testing search parameters..."):
            results = optimizer.test_search_parameters(query)

            st.subheader("Search Results Analysis")

            # Display results in a table
            data = []
            for params, result in results.items():
                data.append(
                    {
                        "Parameters": params,
                        "Results Found": result["count"],
                        "Average Score": f"{result['avg_score']:.3f}",
                    }
                )

            st.table(data)

            # Show best parameters
            best_params = max(results.items(), key=lambda x: x[1]["avg_score"])
            st.success(
                f"Best parameters: {best_params[0]} (Score: {best_params[1]['avg_score']:.3f})"
            )

    st.subheader("Optimized Search Strategies")

    strategy = st.selectbox(
        "Choose search strategy:",
        [
            "General",
            "Theme-specific",
            "Size-specific",
            "Year-specific",
            "Price-specific",
            "Hybrid",
            "Contextual",
        ],
    )

    if st.button("🚀 Test Optimized Search"):
        with st.spinner("Running optimized search..."):
            if strategy == "General":
                retriever = optimizer._optimize_general_search(query)
            elif strategy == "Theme-specific":
                retriever = optimizer._optimize_theme_search(query)
            elif strategy == "Size-specific":
                retriever = optimizer._optimize_size_search(query)
            elif strategy == "Year-specific":
                retriever = optimizer._optimize_year_search(query)
            elif strategy == "Price-specific":
                retriever = optimizer._optimize_price_search(query)
            elif strategy == "Hybrid":
                retriever = optimizer._create_hybrid_retriever()
            elif strategy == "Contextual":
                retriever = optimizer._create_contextual_retriever()

            docs = retriever.get_relevant_documents(query)
            analytics = optimizer.get_search_analytics(query, docs)

            st.subheader("Search Analytics")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Results Found", analytics["result_count"])
            with col2:
                st.metric("Themes Found", analytics["themes_found"])
            with col3:
                st.metric("Years Found", analytics["years_found"])
            with col4:
                st.metric("Avg Pieces", f"{analytics['avg_pieces']:.0f}")

            st.subheader("Top Results")
            for i, doc in enumerate(docs[:5], 1):
                with st.expander(f"Result {i}"):
                    try:
                        data = json.loads(doc.page_content)
                        st.json(data)
                    except Exception:
                        st.text(doc.page_content[:500] + "...")


if __name__ == "__main__":
    main()
