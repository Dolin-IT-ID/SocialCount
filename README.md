# 📊 SocialCount - Social Media Analytics with AI

SocialCount adalah aplikasi analisis media sosial yang menggunakan AI untuk mengumpulkan dan menganalisis statistik dari YouTube, TikTok, dan Facebook. Aplikasi ini menggunakan CrewAI untuk orkestrasi AI dan Llama2 melalui Ollama untuk analisis mendalam.

## ✨ Fitur Utama

- 🎥 **YouTube Analytics**: Views, likes, comments, dan metadata
- 🎵 **TikTok Analytics**: Views, likes, shares, comments
- 👥 **Facebook Analytics**: Views, reactions, shares, comments
- 🤖 **AI-Powered Analysis**: Menggunakan Llama2 untuk insights mendalam
- 🔄 **Batch Processing**: Analisis multiple URL sekaligus
- 📊 **Interactive Dashboard**: Web interface dengan Streamlit
- 💻 **CLI Interface**: Command-line tool untuk automation
- 📈 **Visualizations**: Grafik dan chart untuk data visualization

## 🛠️ Teknologi yang Digunakan

- **CrewAI**: AI agent orchestration
- **Ollama + Llama2**: Local AI model untuk analisis
- **Selenium**: Web scraping untuk data collection
- **Streamlit**: Web interface
- **Plotly**: Data visualization
- **Pandas**: Data processing

## 📋 Prerequisites

### 1. Python 3.8+
```bash
python --version
```

### 2. Ollama Installation
1. Download dan install Ollama dari [https://ollama.ai/](https://ollama.ai/)
2. Install Llama2 model:
```bash
ollama pull llama2
```

### 3. Chrome Browser
Selenium memerlukan Chrome browser untuk web scraping.

## 🚀 Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd SocialCount
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment
```bash
cp .env.example .env
```

Edit file `.env` sesuai konfigurasi Anda:
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
HEADLESS_BROWSER=true
```

### 4. Verify Installation
```bash
python main.py --check
```

## 💻 Penggunaan

### Web Interface (Recommended)
```bash
# Jalankan aplikasi web
python main.py --web
# atau
streamlit run app.py
```

Buka browser dan akses `http://localhost:8501`

### Command Line Interface

#### Analisis URL Tunggal
```bash
python main.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

#### Analisis Multiple URLs
```bash
# Dari file
echo "https://www.youtube.com/watch?v=dQw4w9WgXcQ" > urls.txt
echo "https://www.tiktok.com/@user/video/123456" >> urls.txt
python main.py --file urls.txt
```

#### Mode Interaktif
```bash
python main.py
```

#### Verbose Output
```bash
python main.py --url "..." --verbose
```

#### Save Results
```bash
python main.py --url "..." --output results.json
```

## 📁 Struktur Proyek

```
SocialCount/
├── app.py                 # Streamlit web application
├── main.py               # CLI interface
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── README.md            # Documentation
│
├── utils/               # Utility modules
│   ├── __init__.py
│   └── url_detector.py  # URL validation and platform detection
│
├── scrapers/            # Web scraping modules
│   ├── __init__.py
│   ├── base_scraper.py  # Base scraper class
│   ├── youtube_scraper.py
│   ├── tiktok_scraper.py
│   └── facebook_scraper.py
│
└── services/            # AI and orchestration services
    ├── __init__.py
    ├── ollama_service.py    # Ollama/Llama2 integration
    └── crew_service.py      # CrewAI agents and tasks
```

## 🤖 AI Agents

Aplikasi menggunakan 3 AI agents yang bekerja secara berkolaborasi:

1. **Data Collector Agent**: Mengumpulkan data dari platform media sosial
2. **Data Analyst Agent**: Menganalisis metrics dan menghitung engagement rates
3. **Insights Generator Agent**: Menghasilkan rekomendasi dan insights actionable

## 📊 Supported Platforms

### YouTube 🎥
- Views count
- Likes count
- Comments count
- Video title
- Channel name
- Upload date

### TikTok 🎵
- Views count
- Likes count
- Shares count
- Comments count
- Video description
- Author username

### Facebook 👥
- Views count (untuk video)
- Reactions count
- Shares count
- Comments count
- Post content
- Page/author name

## ⚙️ Configuration

### Environment Variables
```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Browser Configuration
HEADLESS_BROWSER=true
SELENIUM_TIMEOUT=30

# Rate Limiting
REQUEST_DELAY=2
MAX_RETRIES=3

# Optional: Social Media API Keys
YOUTUBE_API_KEY=your_api_key
FACEBOOK_ACCESS_TOKEN=your_token
TIKTOK_API_KEY=your_api_key
```

### Browser Settings
- Default: Headless Chrome
- Timeout: 30 seconds
- User-Agent: Modern Chrome browser

## 🔧 Troubleshooting

### Common Issues

#### 1. Ollama Service Not Available
```bash
# Check if Ollama is running
ollama list

# Start Ollama service
ollama serve

# Pull Llama2 model if not available
ollama pull llama2
```

#### 2. Chrome Driver Issues
```bash
# Update Chrome browser to latest version
# WebDriver will be automatically downloaded
```

#### 3. Scraping Failures
- Beberapa platform memiliki anti-bot protection
- Coba gunakan mode non-headless untuk debugging
- Periksa koneksi internet

#### 4. Rate Limiting
- Sesuaikan `REQUEST_DELAY` di config
- Gunakan proxy jika diperlukan
- Hindari terlalu banyak request bersamaan

### Debug Mode
```bash
# Run dengan verbose output
python main.py --url "..." --verbose

# Check service status
python main.py --check
```

## 📈 Performance Tips

1. **Batch Processing**: Gunakan multiple URL analysis untuk efisiensi
2. **Headless Mode**: Aktifkan untuk performa lebih baik
3. **Rate Limiting**: Sesuaikan delay antar request
4. **Model Optimization**: Gunakan model Ollama yang lebih ringan jika diperlukan

## 🔒 Privacy & Ethics

- Aplikasi hanya mengumpulkan data publik
- Tidak menyimpan credentials atau data pribadi
- Mengikuti robots.txt dan rate limiting
- Gunakan secara bertanggung jawab

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

MIT License - lihat file LICENSE untuk detail.

## 🆘 Support

Jika mengalami masalah:
1. Periksa troubleshooting guide
2. Check GitHub issues
3. Create new issue dengan detail error

## 🔮 Future Features

- [ ] Instagram support
- [ ] Twitter/X integration
- [ ] Advanced analytics dashboard
- [ ] Export to Excel/PDF
- [ ] Scheduled analysis
- [ ] API endpoints
- [ ] Docker containerization

---

**Made with ❤️ using CrewAI and Llama2**