# 🧱 LEGO RAG Search Engine

A modern **Retrieval-Augmented Generation (RAG)** system for LEGO data, powered by AI and semantic search. Discover, analyze, and explore LEGO sets across multiple data sources with intelligent search capabilities.

## 🚀 Quick Start - Launch in Gitpod

**[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/rogerolowski/grok-alex-lego-rag1)**

**⚡ Instant setup (2-3 minutes):**
1. ✅ **Pre-built database** with 1,338+ LEGO records
2. ✅ **Pre-built FAISS index** for instant search
3. ✅ **Optimized dependencies** (CPU-only, no CUDA)
4. ✅ **Launch enhanced Streamlit app** on port 8080

---

## 🎯 Key Features

### **🔍 Advanced Search**
- **AI-Powered**: GPT-4 with semantic retrieval
- **Query Optimization**: Theme, size, year, price-specific strategies
- **Hybrid Search**: Semantic + keyword combination
- **Smart Filtering**: Advanced filters and similarity thresholds

### **📊 Rich Data Sources**
- **2 Major APIs**: Rebrickable (748 sets) + Brickset (1,110 sets)
- **1,338+ Records**: Comprehensive LEGO database
- **25+ Themes**: Star Wars, Technic, City, Creator, Architecture, Marvel, Harry Potter, Disney, Ninjago, Friends, and more
- **Multi-Year Coverage**: 1977-2025 releases (48 years of LEGO!)

### **🎨 Professional UI/UX**
- **Modern Design**: Gradient headers, card layouts, custom CSS
- **Interactive Analytics**: Plotly charts and visualizations
- **Search History**: Remember and reuse queries
- **Advanced Filters**: Theme, year, price, piece count ranges
- **Real-time Stats**: Database metrics and performance monitoring

### **⚡ Performance**
- **DuckDB**: Fast columnar storage
- **FAISS**: Optimized vector similarity search
- **uv**: 10x faster Python package management
- **CPU-Optimized**: No GPU/CUDA required, perfect for cloud
- **Instant Startup**: Pre-built database and FAISS index

---

## 🛠️ Tech Stack

```
Frontend: Streamlit + Plotly + Custom CSS
Backend: Python + LangChain + OpenAI
Package Manager: uv + conda (10x faster than pip)
Database: DuckDB (columnar storage)
Vector Search: FAISS (CPU-optimized)
APIs: 10+ LEGO data sources
```

---

## 📋 Prerequisites

### **Required**
- **Gitpod Account** (free at [gitpod.io](https://gitpod.io))

### **Optional** (for enhanced features)
- **OpenAI API Key** ([Get Here](https://platform.openai.com/api-keys))
- **Rebrickable API Key** ([Get Here](https://rebrickable.com/api/))
- **Brickset API Key** ([Register Here](https://brickset.com))
- **BrickOwl API Key** ([Get Here](https://www.brickowl.com))
- **BrickLink Token** ([Get Here](https://www.bricklink.com/v3/api.page))

---

## 🔧 Configuration (Optional)

### **API Keys for Enhanced Features**
Set these in Gitpod Project Settings → Variables:

```env
OPENAI_API_KEY=your_openai_key_here
REBRICKABLE_API_KEY=your_rebrickable_key_here
BRICKSET_API_KEY=your_brickset_key_here
BRICKSET_USERNAME=your_brickset_username
BRICKSET_PASSWORD=your_brickset_password
BRICKOWL_API_KEY=your_brickowl_key_here
BRICKLINK_TOKEN=your_bricklink_token_here
RAG_MODE=prod
PIP_CACHE_DIR=/workspace/.cache/pip
UV_CACHE_DIR=/workspace/.cache/uv
```

> **💡 Note**: The app works without API keys, but you'll get enhanced data and features with them.

---

## 🎮 Usage

### **Getting Started**
1. **Click** the Gitpod button above
2. **Wait** for the workspace to load (~30 seconds)
3. **Start searching** - the app opens automatically

### **Example Queries**
- "What are the best Star Wars LEGO sets?"
- "Show me Technic vehicles with motors"
- "Find expensive collector sets from 2024"
- "LEGO Architecture sets under $100"
- "Marvel superhero sets for kids"
- "Harry Potter themed LEGO sets"
- "Disney princess LEGO sets"
- "Ninjago sets with many pieces"

### **Features**
- **Smart Search**: Natural language queries with AI responses
- **Visual Analytics**: Interactive charts and data visualization
- **Advanced Filters**: Multi-criteria filtering and sorting
- **Search History**: Track and reuse previous queries
- **Performance Dashboard**: Real-time system metrics

---

## 📊 Data Sources & Coverage

| Source | Records | Focus | Features |
|--------|---------|-------|----------|
| **Rebrickable** | 748 | General sets | Comprehensive catalog, all themes |
| **Brickset** | 1,110 | Recent releases | User ratings, reviews, 2015-2025 |
| **Total** | **1,338** | **Complete coverage** | **25+ themes, 48 years of LEGO** |

**Themes Available:** Star Wars, Technic, City, Creator, Architecture, Marvel, Harry Potter, Disney, Ninjago, Friends, Minecraft, Speed Champions, Ideas, Expert, and more!

---

## 📁 Project Structure

```
grok-alex-lego-rag1/
├── app.py                   # 🎨 Enhanced Streamlit app
├── search_optimizer.py      # 🔍 Search optimization tool
├── load_data.py             # 📊 Enhanced data loader
├── api_integrations.py      # 🌐 Multi-source API integration
├── debug_setup.py          # 🔧 Comprehensive debug tool
├── pyproject.toml          # 📦 uv project configuration (optimized)
├── uv.lock                 # 🔒 Locked dependencies
├── .gitpod.yml             # 🚀 Gitpod configuration
├── .gitpod.Dockerfile      # 🐳 Optimized Docker image
├── .dockerignore           # 🚫 Docker build optimization
├── lego_data.duckdb        # 🗄️ Pre-built DuckDB database (1,338 records)
├── faiss_index/            # 🔍 Pre-built FAISS vector index
└── .env                    # 🔑 API keys (create this)
```

---

## 🔧 Debug & Troubleshooting

### **Quick Debug**
```bash
uv run python debug_setup.py
```

### **Common Issues**
- **❌ OpenAI API key not found**: Add to `.env` file
- **❌ No data in database**: Database is pre-built, should work immediately
- **❌ FAISS index missing**: Index is pre-built, should work immediately
- **❌ API connection failed**: Verify keys and internet connection
- **❌ CUDA errors**: Optimized for CPU-only, no GPU required

---

## 🚀 Available Apps

### **Main Applications**
```bash
# Enhanced main app (recommended)
uv run streamlit run app.py

# Search optimization tool
uv run streamlit run search_optimizer.py
```

### **Data loading utilities**
```bash
uv run python load_data.py
uv run python api_integrations.py
```

### **Debug & Maintenance**
```bash
# Comprehensive system check
uv run python debug_setup.py

# Database statistics
uv run python -c "import duckdb; conn = duckdb.connect('lego_data.duckdb'); print(conn.execute('SELECT COUNT(*) FROM lego_data').fetchone()[0])"

# Update dependencies
uv lock --upgrade

# Install dev dependencies
uv sync --dev
```

---

## 🔮 Future Enhancements

### **Planned Features**
- **🎤 Voice Search**: Speech-to-text integration
- **📸 Image Recognition**: Set identification from photos
- **💰 Price Tracking**: Historical price analysis
- **👥 Social Features**: User reviews and ratings
- **📱 Mobile App**: Native mobile application
- **🔌 API Endpoints**: RESTful API for developers
- **🤖 ML Recommendations**: Personalized suggestions
- **⚡ Real-time Updates**: Live data synchronization

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Submit** a pull request

---

## 📄 License

[MIT License](LICENSE)

---

## 🎯 Quick Launch

**[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/rogerolowski/grok-alex-lego-rag1)**

Alex