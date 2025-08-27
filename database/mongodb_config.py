import os
from pymongo import MongoClient
from datetime import datetime
from typing import Dict, List, Optional
import streamlit as st

class MongoDBConfig:
    def __init__(self):
        # Konfigurasi MongoDB - bisa diubah sesuai kebutuhan
        self.connection_string = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.database_name = os.getenv('MONGODB_DATABASE', 'socialcount_db')
        self.collection_name = 'video_summaries'
        self.client = None
        self.db = None
        self.collection = None
    
    def connect(self):
        """Membuat koneksi ke MongoDB"""
        try:
            self.client = MongoClient(self.connection_string)
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            # Test koneksi
            self.client.admin.command('ping')
            return True
        except Exception as e:
            st.error(f"Gagal terhubung ke MongoDB: {str(e)}")
            return False
    
    def disconnect(self):
        """Menutup koneksi MongoDB"""
        if self.client:
            self.client.close()
    
    def insert_video_data(self, video_data: Dict) -> bool:
        """Menyimpan data video ke database"""
        try:
            if not self.collection:
                if not self.connect():
                    return False
            
            # Menambahkan timestamp jika belum ada
            if 'created_at' not in video_data:
                video_data['created_at'] = datetime.now()
            
            result = self.collection.insert_one(video_data)
            return result.inserted_id is not None
        except Exception as e:
            st.error(f"Gagal menyimpan data: {str(e)}")
            return False
    
    def get_all_videos(self, start_date: Optional[datetime] = None, 
                      end_date: Optional[datetime] = None) -> List[Dict]:
        """Mengambil semua data video dengan filter tanggal opsional"""
        try:
            if not self.collection:
                if not self.connect():
                    return []
            
            query = {}
            if start_date and end_date:
                query['waktu_penghitungan'] = {
                    '$gte': start_date,
                    '$lte': end_date
                }
            elif start_date:
                query['waktu_penghitungan'] = {'$gte': start_date}
            elif end_date:
                query['waktu_penghitungan'] = {'$lte': end_date}
            
            cursor = self.collection.find(query).sort('waktu_penghitungan', -1)
            return list(cursor)
        except Exception as e:
            st.error(f"Gagal mengambil data: {str(e)}")
            return []
    
    def get_video_count(self) -> int:
        """Menghitung jumlah total video dalam database"""
        try:
            if not self.collection:
                if not self.connect():
                    return 0
            return self.collection.count_documents({})
        except Exception as e:
            st.error(f"Gagal menghitung data: {str(e)}")
            return 0
    
    def delete_video(self, video_id: str) -> bool:
        """Menghapus video berdasarkan ID"""
        try:
            if not self.collection:
                if not self.connect():
                    return False
            
            from bson import ObjectId
            result = self.collection.delete_one({'_id': ObjectId(video_id)})
            return result.deleted_count > 0
        except Exception as e:
            st.error(f"Gagal menghapus data: {str(e)}")
            return False
    
    def update_video(self, video_id: str, update_data: Dict) -> bool:
        """Memperbarui data video"""
        try:
            if not self.collection:
                if not self.connect():
                    return False
            
            from bson import ObjectId
            update_data['updated_at'] = datetime.now()
            result = self.collection.update_one(
                {'_id': ObjectId(video_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            st.error(f"Gagal memperbarui data: {str(e)}")
            return False

# Instance global untuk digunakan di seluruh aplikasi
mongo_db = MongoDBConfig()