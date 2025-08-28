# Mandarin Chinese language configuration
# 中文（简体）语言配置

LANGUAGE_CONFIG = {
    "language_name": "中文（简体）",
    "language_code": "zh",
    "flag": "🇨🇳",
    
    # Header and Title
    "app_title": "🎬 多平台视频详情提取器",
    "app_subtitle": "使用AI技术深度分析YouTube、TikTok和Facebook视频",
    
    # Navigation Tabs
    "tab_extract": "🎬 视频提取",
    "tab_batch": "📊 批量分析",
    "tab_history": "📚 历史记录",
    "tab_database": "🗄️ 数据库与导出",
    
    # Main Form Labels
    "creator_name": "👤 视频创作者姓名：",
    "creator_placeholder": "请输入视频创作者/制作者姓名",
    "creator_help": "视频创作者或制作者姓名",
    
    "calculation_date": "📅 计算日期：",
    "calculation_time": "⏰ 计算时间：",
    "date_help": "进行视频计算/分析的日期",
    "time_help": "进行视频计算/分析的时间",
    
    "video_url": "🔗 输入视频URL：",
    "url_placeholder": "https://www.youtube.com/watch?v=... 或 https://www.tiktok.com/@user/video/... 或 https://www.facebook.com/watch/?v=...",
    "url_help": "支持YouTube、TikTok和Facebook的URL",
    
    "account_name": "📱 账户名称：",
    "account_placeholder": "@用户名",
    "account_help": "平台账户名/用户名",
    
    # Buttons
    "extract_button": "🚀 提取详情",
    "vlm_analysis": "🤖 VLM分析",
    "save_data": "💾 保存数据",
    "add_to_database": "💾 添加到数据库",
    "extract_all": "🚀 提取全部",
    "load_data": "📊 加载数据",
    
    # Messages
    "url_required": "⚠️ 请先输入视频URL",
    "invalid_platform": "无法检测平台。请确保URL来自YouTube、TikTok或Facebook",
    "empty_url": "URL不能为空",
    "extraction_success": "✅ 提取成功！",
    "extraction_failed": "❌ 提取失败",
    "save_success": "✅ 数据已成功保存到MongoDB数据库！",
    "save_failed": "❌ 保存数据到数据库失败",
    "fill_required_fields": "⚠️ 保存到数据库前请填写视频创作者姓名和账户名称",
    
    # Sidebar
    "sidebar_title": "🎯 支持的平台",
    "sidebar_vlm": "🧠 VLM功能",
    "sidebar_usage": "📋 使用方法",
    
    # Platform Features
    "youtube_features": [
        "📊 观看量、点赞、评论",
        "📅 上传日期",
        "⏱️ 视频时长",
        "👤 频道信息",
        "📝 完整描述"
    ],
    "tiktok_features": [
        "❤️ 点赞和分享",
        "💬 评论数量",
        "👀 观看次数",
        "🎵 音乐信息",
        "#️⃣ 标签"
    ],
    "facebook_features": [
        "👍 反应",
        "💬 评论",
        "🔄 分享",
        "📊 互动指标",
        "📅 发布日期"
    ],
    
    # Tab content
    'tab_extract': '🎬 单个视频详细提取',
    'creator_name': '👤 视频创作者姓名:',
    'creator_placeholder': '输入视频创作者/制作者姓名',
    'creator_help': '视频创作者或制作者的姓名',
    'calculation_date': '📅 计算日期:',
    'date_help': '进行视频计算/分析的日期',
    'calculation_time': '⏰ 计算时间:',
    'time_help': '进行视频计算/分析的时间',
    'url_input': '🔗 输入视频URL:',
    'url_placeholder': 'https://www.youtube.com/watch?v=... 或 https://www.tiktok.com/@user/video/... 或 https://www.facebook.com/watch/?v=...',
    'url_help': '支持来自YouTube、TikTok和Facebook的URL',
    'extract_button': '🚀 提取详情',
    
    # Batch Analysis
    'tab_batch': '📊 批量分析多个URL',
    'batch_info': '此功能允许您同时分析多个视频',
    'batch_urls': '📝 输入URL（每行一个）:',
    'batch_placeholder': 'https://www.youtube.com/watch?v=...\nhttps://www.tiktok.com/@user/video/...\nhttps://www.facebook.com/watch/?v=...',
    'batch_extract': '🚀 提取全部',
    'batch_vlm': '🤖 批量VLM分析',
    
    # History Tab
    'history_empty': '📝 暂无提取历史记录。开始提取您的第一个视频吧！',
    'history_title': '📚 提取历史',
    'video_count': '个视频',
    'total_videos': '📊 总视频数',
    'total_views': '👀 总观看数',
    'total_likes': '👍 总点赞数',
    'title_label': '标题',
    'platform_label': '平台',
    'clear_history': '🗑️ 清除历史',
    
    # Database Tab
    'tab_database': '🗄️ 数据库与数据导出',
    'check_db_connection': '🔄 检查数据库连接',
    'checking_mongodb': '正在检查MongoDB连接...',
    'mongodb_success': '✅ MongoDB连接成功！',
    'mongodb_failed': '❌ MongoDB连接失败',
    'total_db_videos': '📊 数据库中的视频总数',
    'tips_label': '提示',
    'mongodb_tips': '请确保MongoDB在您的系统中运行',
    'filter_data': '🔍 数据筛选',
    'start_date': '📅 开始日期：',
    'start_date_help': '选择数据筛选的开始日期',
    'end_date': '📅 结束日期：',
    'end_date_help': '选择数据筛选的结束日期',
    'load_data': '📊 加载数据',
    'loading_data': '📥 正在从数据库加载数据...',
    'data_summary': '📈 数据摘要',
    'data_preview': '👀 数据预览',
    'show_data_table': '📋 在表格中显示数据',
    'select_columns': '选择要显示的列：',
    'select_min_column': '⚠️ 请至少选择一列进行显示',
    'no_data_display': '📭 没有数据可显示',
    'export_data': '📥 导出数据',
    'export_format': '导出格式',
    'select_export_format': '选择导出格式：',
    'export_format_help': 'Excel详细：每个视频的完整数据\nExcel摘要：符合越南/中文参考的统计格式',
    'format_preview': '格式预览',
    'summary_format_info': '📊 按创作者统计摘要格式，使用越南/中文标题符合参考文件',
    'detail_format_info': '📋 每个视频的详细格式，使用印尼语标题',
    'csv_format_info': '📄 原始数据的标准CSV格式',
    'export_failed': '❌ 导出文件失败',
    'no_data_range': '📭 所选日期范围内没有数据',
    'click_load_data': '👆 点击\'加载数据\'从数据库显示数据',
    
    # Status Messages
    'vlm_active': '✅ VLM：已激活',
    'ai_ready': '🧠 AI分析已就绪',
    'vlm_inactive': '❌ VLM：未激活',
    'ai_unavailable': '⚠️ AI分析不可用',
    'stats_unavailable': '统计数据不可用',
    'history_cleared': '✅ 历史记录已清除！',
    'extraction_success': '🎉 提取成功！',
    'fill_creator_warning': '⚠️ 保存到数据库前请填写视频创作者姓名和账户名',
    'data_saved_success': '✅ 数据已成功保存到MongoDB数据库！',
    'data_save_failed': '❌ 数据保存到数据库失败',
    'enter_url_warning': '⚠️ 请先输入视频URL',
    'no_valid_urls': '⚠️ 未找到有效的URL',
    'enter_urls_first': '⚠️ 请先输入URL',
    
    # VLM Features
    "vlm_features": [
        "📊 互动分析",
        "📈 性能预测",
        "🎯 内容推荐",
        "📝 自动摘要",
        "🔍 深度洞察"
    ],
    
    # Usage Instructions
    "usage_steps": [
        "📝 输入视频URL",
        "🚀 点击'提取详情'按钮",
        "⏳ 等待提取过程",
        "📊 查看结果和分析",
        "🤖 获取AI洞察（如果VLM激活）",
        "💾 如需要可保存结果"
    ],
    
    # Batch Analysis
    "batch_title": "📊 多URL批量分析",
    "batch_info": "💡 此功能允许您同时分析多个视频",
    "batch_input": "📝 输入URL（每行一个）：",
    "batch_placeholder": "https://www.youtube.com/watch?v=...\nhttps://www.tiktok.com/@user/video/...\nhttps://www.facebook.com/watch/?v=...",
    
    # Database & Export
    "database_title": "🗄️ 数据库与数据导出",
    "filter_data": "🔍 筛选数据",
    "start_date": "📅 开始日期：",
    "end_date": "📅 结束日期：",
    "start_date_help": "选择筛选数据的开始日期",
    "end_date_help": "选择筛选数据的结束日期",
    
    "data_summary": "📈 数据摘要",
    "data_preview": "👀 数据预览",
    "show_table": "📋 在表格中显示数据",
    "select_columns": "选择要显示的列：",
    "min_one_column": "⚠️ 请至少选择一列显示",
    "no_data": "📭 没有数据可显示",
    
    "export_data": "📥 导出数据",
    "export_format": "**导出格式：**",
    "export_preview": "**格式预览：**",
    "export_action": "**导出操作：**",
    
    "format_csv": "CSV",
    "format_excel_detail": "Excel详细",
    "format_excel_summary": "Excel摘要",
    
    "format_help": "Excel详细：每个视频的完整数据\nExcel摘要：按参考越南/中文格式的统计格式",
    
    "preview_summary": "📊 按创作者统计摘要格式，使用越南/中文标题符合参考文件",
    "preview_detail": "📋 每个视频的详细完整格式，使用中文标题",
    "preview_csv": "📄 原始数据的标准CSV格式",
    
    "export_button": "📥 导出为{}",
    "preparing_file": "📦 正在准备{}文件...",
    "file_ready": "✅ {}文件已准备好下载！",
    "export_failed": "❌ 创建导出文件失败",
    "export_error": "❌ 导出时出错：{}",
    
    "platform_stats": "📊 平台统计",
    
    # Loading and Status Messages
    "loading_data": "📥 从数据库加载数据...",
    "saving_data": "💾 保存到数据库...",
    "extracting": "🔄 提取视频数据...",
    "analyzing": "🤖 使用VLM分析...",
    
    # Error Messages
    "vlm_unavailable": "VLM不可用于分析",
    "connection_error": "❌ 连接错误",
    "processing_error": "❌ 处理时出错",
    
    # Data Fields
    "video_title": "视频标题",
    "video_description": "描述",
    "views": "观看量",
    "likes": "点赞",
    "comments": "评论",
    "shares": "分享",
    "duration": "时长",
    "upload_date": "上传日期",
    "platform": "平台",
    "created_at": "创建于",
    "updated_at": "更新于",
    
    # Download
    "download_data": "💾 下载数据",
    "download_json": "📥 下载JSON数据",
    
    # Language Switcher
    "language_selector": "🌐 语言 / Language",
    "select_language": "选择语言",
    
    # Status and notification messages
    'export_format_excel_detail': '包含每个视频完整详细信息的Excel文件',
    'export_format_csv': '可用Excel或其他电子表格应用程序打开的CSV文件',
    'export_failed': '导出数据失败',
    'no_data_in_range': '所选日期范围内没有数据',
    'load_data_first': '请先加载数据',
    'vlm_status_active': 'VLM 活跃',
    'vlm_status_inactive': 'VLM 未活跃',
    'ai_ready': 'AI 就绪',
    'ai_unavailable': 'AI 不可用',
    'statistics_unavailable': '统计数据不可用',
    'history_cleared': '历史记录已成功清除',
    'extraction_success': '数据提取成功',
    'warning_missing_creator': '警告：视频创作者姓名为空。保存到数据库前请填写。',
    'warning_missing_account': '警告：账户名称为空。保存到数据库前请填写。',
    'data_saved_success': '数据已成功保存到MongoDB',
    'data_save_failed': '保存数据到MongoDB失败',
    'warning_enter_url': '请先输入视频URL',
    'batch_no_valid_urls': '未找到有效的URL',
    'batch_enter_urls': '请先输入URL',
    
    # Export headers
    'export_id': 'ID',
    'export_creator_name': '视频创作者姓名',
    'export_account_name': '账户名称',
    'export_video_url': '视频URL',
    'export_platform': '平台',
    'export_video_title': '视频标题',
    'export_description': '描述',
    'export_views': '观看次数',
    'export_likes': '点赞数',
    'export_comments': '评论数',
    'export_shares': '分享数',
    'export_duration': '时长',
    'export_upload_date': '上传日期',
    'export_calculation_time': '计算时间',
    'export_created_at': '创建时间',
    'export_updated_at': '更新时间',
    
    # Summary export headers
    'summary_creator_name': '创作者姓名',
    'summary_fb_post': 'FB 贴文',
    'summary_fb_view': 'FB 观看',
    'summary_fb_like': 'FB 按赞',
    'summary_fb_comment': 'FB 留言',
    'summary_fb_share': 'FB 分享',
    'summary_zalo_post': 'Zalo 贴文',
    'summary_zalo_view': 'Zalo 观看',
    'summary_zalo_like': 'Zalo 按赞',
    'summary_zalo_comment': 'Zalo 留言',
    'summary_zalo_share': 'Zalo 分享',
    'summary_yt_post': 'YT 贴文',
    'summary_yt_view': 'YT 观看',
    'summary_yt_like': 'YT 按赞',
    'summary_yt_comment': 'YT 留言',
    'summary_yt_share': 'YT 分享',
    'summary_total_post': '总贴文',
    'summary_total_view': '总观看',
    'summary_total_like': '总按赞',
    'summary_total_comment': '总留言',
    'summary_total_share': '总分享',
    
    # Summary export labels
    'summary_main_header': '社交媒体互动统计表',
    'summary_export_date': '导出日期：{date}',
    'summary_date_label': '制表日期',
    'summary_time_label': '时间',
    'summary_total': '总计',
    'summary_post': '贴文',
    'summary_view': '观看',
    'summary_like': '按赞',
    'summary_comment': '留言',
    'summary_share': '分享',
    
    # Export summary display
    'export_no_data': '📭 没有数据可导出',
    'export_total_videos': '总视频数',
    'export_platforms': '平台',
    'export_date_range': '日期范围',
    'export_days_format': '{days} 天',
    'export_available_platforms': '可用平台',
    'export_data_period': '数据期间'
}