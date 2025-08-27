import pandas as pd
import io
from datetime import datetime
from typing import List, Dict
import streamlit as st
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows

class DataExporter:
    def __init__(self):
        pass
    
    def prepare_data_for_export(self, video_data: List[Dict]) -> pd.DataFrame:
        """Menyiapkan data untuk ekspor dengan format yang rapi"""
        if not video_data:
            return pd.DataFrame()
        
        # Konversi data MongoDB ke format yang lebih mudah dibaca
        export_data = []
        for video in video_data:
            row = {
                'ID': str(video.get('_id', '')),
                'Nama Pembuat Video': video.get('nama_pembuat', ''),
                'Nama Akun': video.get('nama_akun', ''),
                'URL Video': video.get('url_video', ''),
                'Platform': video.get('platform', ''),
                'Judul Video': video.get('title', ''),
                'Deskripsi': video.get('description', '')[:100] + '...' if video.get('description', '') else '',
                'Views': video.get('views', 0),
                'Likes': video.get('likes', 0),
                'Comments': video.get('comments', 0),
                'Shares': video.get('shares', 0),
                'Duration': video.get('duration', ''),
                'Upload Date': video.get('upload_date', ''),
                'Waktu Penghitungan': video.get('waktu_penghitungan', ''),
                'Created At': video.get('created_at', ''),
                'Updated At': video.get('updated_at', '')
            }
            export_data.append(row)
        
        df = pd.DataFrame(export_data)
        
        # Format tanggal untuk tampilan yang lebih baik
        date_columns = ['Waktu Penghitungan', 'Created At', 'Updated At']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
        
        return df
    
    def export_to_csv(self, video_data: List[Dict]) -> bytes:
        """Ekspor data ke format CSV"""
        df = self.prepare_data_for_export(video_data)
        if df.empty:
            return b''
        
        # Konversi ke CSV dengan encoding UTF-8
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False, encoding='utf-8')
        return csv_buffer.getvalue().encode('utf-8')
    
    def export_to_excel(self, video_data: List[Dict]) -> bytes:
        """Ekspor data ke format Excel dengan styling"""
        df = self.prepare_data_for_export(video_data)
        if df.empty:
            return b''
        
        # Buat workbook Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Data Video Summary"
        
        # Styling untuk header
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_alignment = Alignment(horizontal="center", vertical="center")
        
        # Tambahkan data ke worksheet
        for r in dataframe_to_rows(df, index=False, header=True):
            ws.append(r)
        
        # Apply styling ke header
        for cell in ws[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
        
        # Auto-adjust column width
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)  # Max width 50
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # Simpan ke buffer
        excel_buffer = io.BytesIO()
        wb.save(excel_buffer)
        excel_buffer.seek(0)
        return excel_buffer.getvalue()
    
    def create_download_link(self, data: bytes, filename: str, file_format: str) -> None:
        """Membuat link download untuk file"""
        if file_format.lower() == 'csv':
            mime_type = 'text/csv'
        elif file_format.lower() == 'excel':
            mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        else:
            mime_type = 'application/octet-stream'
        
        st.download_button(
            label=f"📥 Download {file_format.upper()}",
            data=data,
            file_name=filename,
            mime=mime_type,
            use_container_width=True
        )
    
    def generate_filename(self, file_format: str, prefix: str = "video_data") -> str:
        """Generate nama file dengan timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = 'csv' if file_format.lower() == 'csv' else 'xlsx'
        return f"{prefix}_{timestamp}.{extension}"
    
    def prepare_summary_statistics(self, video_data: List[Dict]) -> pd.DataFrame:
        """Menyiapkan data ringkasan statistik sesuai format referensi Vietnam/Chinese"""
        if not video_data:
            return pd.DataFrame()
        
        # Kelompokkan data per kreator
        creator_stats = {}
        
        for video in video_data:
            creator_name = video.get('nama_pembuat', 'Unknown')
            platform = video.get('platform', 'Unknown').lower()
            
            if creator_name not in creator_stats:
                creator_stats[creator_name] = {
                    'facebook': {'post': 0, 'like': 0, 'comment': 0, 'share': 0},
                    'zalo': {'post': 0, 'like': 0, 'comment': 0, 'share': 0},
                    'youtube': {'post': 0, 'like': 0, 'comment': 0, 'share': 0}
                }
            
            # Map platform names
            platform_key = 'facebook' if 'facebook' in platform else \
                          'youtube' if 'youtube' in platform else \
                          'zalo' if 'zalo' in platform else 'facebook'
            
            # Increment metrics
            creator_stats[creator_name][platform_key]['post'] += 1
            creator_stats[creator_name][platform_key]['like'] += video.get('likes', 0)
            creator_stats[creator_name][platform_key]['comment'] += video.get('comments', 0)
            creator_stats[creator_name][platform_key]['share'] += video.get('shares', 0)
        
        # Buat DataFrame dengan header sesuai referensi
        summary_data = []
        for creator, stats in creator_stats.items():
            row = {
                'Tên KD\n業務名稱': creator,
                # Facebook columns
                'FB Post\nPO文': stats['facebook']['post'],
                'FB Like\n喜歡': stats['facebook']['like'],
                'FB Comment\n評論': stats['facebook']['comment'],
                'FB Share\n分享': stats['facebook']['share'],
                # Zalo columns
                'Zalo Post\nPO文': stats['zalo']['post'],
                'Zalo Like\n喜歡': stats['zalo']['like'],
                'Zalo Comment\n評論': stats['zalo']['comment'],
                # Youtube columns
                'YT Post\nPO文': stats['youtube']['post'],
                'YT Like\n喜歡': stats['youtube']['like'],
                'YT Comment\n評論': stats['youtube']['comment'],
                # Total columns
                'Tổng Post': stats['facebook']['post'] + stats['zalo']['post'] + stats['youtube']['post'],
                'Tổng Like': stats['facebook']['like'] + stats['zalo']['like'] + stats['youtube']['like'],
                'Tổng Comment': stats['facebook']['comment'] + stats['zalo']['comment'] + stats['youtube']['comment']
            }
            summary_data.append(row)
        
        return pd.DataFrame(summary_data)
    
    def export_summary_to_excel(self, video_data: List[Dict]) -> bytes:
        """Ekspor ringkasan statistik ke format Excel sesuai referensi"""
        df = self.prepare_summary_statistics(video_data)
        if df.empty:
            return b''
        
        # Buat workbook Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Ringkasan Statistik"
        
        # Header utama (row 1)
        ws.merge_cells('A1:N1')
        ws['A1'] = 'BẢNG TỔNG KẾT LƯỢT LIKE, VIEW CÁC KÊNH\n各網頁統計表'
        ws['A1'].font = Font(bold=True, size=14)
        ws['A1'].alignment = Alignment(horizontal="center", vertical="center")
        
        # Info tanggal (row 2)
        current_date = datetime.now().strftime('%d/%m/%Y')
        ws['A2'] = 'Ngày lập biểu:\n製表日期'
        ws['B2'] = 'Thời gian\n時間'
        ws['C2'] = current_date
        
        # Header platform (row 3)
        ws['A3'] = 'Ứng Dụng\n應用\n\nTên KD\n業務名稱'
        ws['B3'] = 'Facebook'
        ws['F3'] = 'Zalo'
        ws['I3'] = 'Youtube'
        ws['L3'] = 'Tổng'
        
        # Merge cells untuk platform headers
        ws.merge_cells('B3:E3')  # Facebook
        ws.merge_cells('F3:H3')  # Zalo
        ws.merge_cells('I3:K3')  # Youtube
        ws.merge_cells('L3:N3')  # Tổng
        
        # Header metrics (row 4)
        metrics_headers = [
            '', 'Post\nPO文', 'Like\n喜歡', 'Comment\n評論', 'Share\n分享',
            'Post\nPO文', 'Like\n喜歡', 'Comment\n評論',
            'Post\nPO文', 'Like\n喜歡', 'Comment\n評論',
            'Post', 'Like', 'Comment'
        ]
        
        for col, header in enumerate(metrics_headers, 1):
            ws.cell(row=4, column=col, value=header)
        
        # Tambahkan data mulai dari row 5
        for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=False), 5):
            for c_idx, value in enumerate(row, 1):
                ws.cell(row=r_idx, column=c_idx, value=value)
        
        # Styling
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
        # Apply styling ke headers
        for row in [3, 4]:
            for col in range(1, 15):
                cell = ws.cell(row=row, column=col)
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
        
        # Auto-adjust column width
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 25)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # Simpan ke buffer
        excel_buffer = io.BytesIO()
        wb.save(excel_buffer)
        excel_buffer.seek(0)
        return excel_buffer.getvalue()
    
    def display_export_summary(self, video_data: List[Dict]) -> None:
        """Menampilkan ringkasan data yang akan diekspor"""
        if not video_data:
            st.warning("📭 Tidak ada data untuk diekspor")
            return
        
        total_videos = len(video_data)
        platforms = set(video.get('platform', 'Unknown') for video in video_data)
        date_range = self._get_date_range(video_data)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Video", total_videos)
        
        with col2:
            st.metric("Platform", len(platforms))
        
        with col3:
            if date_range:
                st.metric("Rentang Tanggal", f"{date_range['days']} hari")
        
        # Tampilkan platform yang ada
        if platforms:
            st.write("**Platform yang tersedia:**", ", ".join(sorted(platforms)))
        
        if date_range:
            st.write(f"**Periode data:** {date_range['start']} - {date_range['end']}")
    
    def _get_date_range(self, video_data: List[Dict]) -> Dict:
        """Mendapatkan rentang tanggal dari data"""
        dates = []
        for video in video_data:
            waktu = video.get('waktu_penghitungan')
            if waktu:
                if isinstance(waktu, str):
                    try:
                        dates.append(pd.to_datetime(waktu))
                    except:
                        pass
                else:
                    dates.append(waktu)
        
        if not dates:
            return None
        
        min_date = min(dates)
        max_date = max(dates)
        days_diff = (max_date - min_date).days
        
        return {
            'start': min_date.strftime('%Y-%m-%d'),
            'end': max_date.strftime('%Y-%m-%d'),
            'days': days_diff
        }

# Instance global untuk digunakan di seluruh aplikasi
data_exporter = DataExporter()