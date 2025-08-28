# 🚀 Panduan Deployment ke Vercel

## Masalah yang Diperbaiki

Error `404: NOT_FOUND` yang terjadi saat deployment ke Vercel telah diperbaiki dengan menambahkan konfigurasi yang tepat.

## File yang Ditambahkan

### 1. `vercel.json`
File konfigurasi utama untuk Vercel yang menentukan:
- Build configuration
- Routing rules
- Environment variables
- Function settings

### 2. `api/index.py`
Handler serverless untuk menjalankan aplikasi Streamlit di Vercel.

### 3. `requirements-vercel.txt`
Dependensi yang dioptimalkan untuk deployment Vercel (tanpa selenium, playwright, dll).

### 4. `runtime.txt`
Menentukan versi Python yang digunakan (Python 3.9.18).

### 5. `.vercelignore`
Mengecualikan file yang tidak diperlukan saat deployment.

## Langkah Deployment

### 1. Persiapan
```bash
# Pastikan semua file konfigurasi ada
ls vercel.json api/index.py requirements-vercel.txt runtime.txt
```

### 2. Deploy ke Vercel
```bash
# Install Vercel CLI jika belum ada
npm i -g vercel

# Login ke Vercel
vercel login

# Deploy
vercel --prod
```

### 3. Konfigurasi Environment Variables (Opsional)
Jika aplikasi memerlukan environment variables:
```bash
vercel env add VARIABLE_NAME
```

## Perbedaan dengan Local Development

### Dependencies
- **Local**: Menggunakan `requirements.txt` (full dependencies)
- **Vercel**: Menggunakan `requirements-vercel.txt` (optimized)

### Features yang Tidak Tersedia di Vercel
- Selenium scraping (memerlukan browser)
- Playwright automation
- CrewAI integration
- Ollama/LLM services

### Features yang Tersedia di Vercel
- Basic URL analysis
- Data visualization dengan Plotly
- Export functionality
- UI interface

## Troubleshooting

### Error 404 NOT_FOUND
✅ **Diperbaiki** dengan konfigurasi `vercel.json` yang tepat.

### Build Timeout
Jika build timeout, coba:
1. Kurangi dependencies di `requirements-vercel.txt`
2. Tingkatkan `maxDuration` di `vercel.json`

### Memory Limit
Jika memory limit exceeded:
1. Optimasi kode untuk mengurangi memory usage
2. Gunakan Vercel Pro plan untuk memory lebih besar

### Function Size Limit
Jika function terlalu besar:
1. Hapus dependencies yang tidak perlu
2. Gunakan `.vercelignore` untuk exclude file besar

## Monitoring

Setelah deployment berhasil:
1. Check function logs di Vercel dashboard
2. Monitor performance metrics
3. Test semua fitur yang tersedia

## Alternatif Deployment

Jika Vercel tidak cocok, pertimbangkan:
- **Streamlit Cloud**: Native untuk Streamlit apps
- **Heroku**: Dengan Procfile
- **Railway**: Modern alternative
- **Google Cloud Run**: Containerized deployment

## Support

Jika masih ada masalah:
1. Check Vercel function logs
2. Verify semua file konfigurasi
3. Test local terlebih dahulu dengan `requirements-vercel.txt`