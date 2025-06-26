#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo script cho các chức năng cộng đồng mới
"""

import sys
import os

# Thêm thư mục src vào path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def demo_community_features():
    """Demo các chức năng cộng đồng mới"""
    print("🎮 Demo Community Features")
    print("=" * 50)
    
    try:
        # Import và khởi tạo
        from community_features import CommunityFeatures
        features = CommunityFeatures()
        
        community_id = "4d49a97b"  # ID của cộng đồng hiện có
        test_user = "T1con"
        
        print(f"🏠 Community ID: {community_id}")
        print(f"👤 Test User: {test_user}")
        
        # 1. Demo tạo chủ đề
        print("\n📝 Demo: Tạo chủ đề thảo luận")
        topic_id = features.create_topic(
            community_id, 
            "Chủ đề thảo luận mới", 
            "Đây là nội dung chủ đề thảo luận mới được tạo bởi hệ thống.", 
            test_user
        )
        print(f"✅ Đã tạo chủ đề với ID: {topic_id}")
        
        # 2. Demo tạo bình chọn
        print("\n📊 Demo: Tạo bình chọn")
        poll_id = features.create_poll(
            community_id,
            "Bạn thích tính năng nào nhất?",
            ["Chủ đề thảo luận", "Bình chọn", "Sự kiện", "Bảng xếp hạng"],
            test_user,
            7  # 7 ngày
        )
        print(f"✅ Đã tạo bình chọn với ID: {poll_id}")
        
        # 3. Demo tạo sự kiện
        print("\n🎉 Demo: Tạo sự kiện")
        event_id = features.create_event(
            community_id,
            "Sự kiện gặp mặt cộng đồng",
            "Sự kiện gặp mặt các thành viên cộng đồng để trao đổi và kết nối.",
            "Hà Nội, Việt Nam",
            "2024-12-31 18:00:00",
            test_user,
            50  # Tối đa 50 người
        )
        print(f"✅ Đã tạo sự kiện với ID: {event_id}")
        
        # 4. Demo bình chọn
        print("\n🗳️ Demo: Tham gia bình chọn")
        success, message = features.vote_poll(poll_id, 0, test_user)
        print(f"✅ Kết quả bình chọn: {message}")
        
        # 5. Demo tham gia sự kiện
        print("\n✅ Demo: Tham gia sự kiện")
        success, message = features.join_event(event_id, test_user)
        print(f"✅ Kết quả tham gia: {message}")
        
        # 6. Demo bảng xếp hạng
        print("\n🏆 Demo: Xem bảng xếp hạng")
        leaderboard = features.get_community_leaderboard(community_id)
        print(f"✅ Bảng xếp hạng có {len(leaderboard)} thành viên:")
        for i, member in enumerate(leaderboard[:5]):  # Top 5
            print(f"   {i+1}. @{member['username']} - Level {member['level']} ({member['points']} điểm)")
        
        # 7. Demo thống kê cá nhân
        print("\n📊 Demo: Thống kê cá nhân")
        stats = features.get_user_stats(test_user)
        print(f"✅ Thống kê của @{test_user}:")
        print(f"   - Level: {stats['level']}")
        print(f"   - Tổng điểm: {stats['total_points']}")
        print(f"   - Số hành động: {len(stats['actions'])}")
        
        print("\n🎉 Demo hoàn thành thành công!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Hãy đảm bảo các file cần thiết đã được tạo trong thư mục src/")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

def demo_ui():
    """Demo giao diện cộng đồng"""
    print("\n🖥️ Demo: Giao diện cộng đồng")
    print("=" * 50)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from src.CommunityWindow import CommunityWindow
        
        app = QApplication(sys.argv)
        print("✅ QApplication khởi tạo thành công")
        
        window = CommunityWindow("T1con")
        print("✅ CommunityWindow khởi tạo thành công")
        print("📱 Các tab có sẵn:")
        print("   - 🏠 Cộng đồng: Quản lý danh sách cộng đồng")
        print("   - 📝 Chủ đề: Tạo và thảo luận chủ đề")
        print("   - 📊 Bình chọn: Tạo và tham gia bình chọn")
        print("   - 🎉 Sự kiện: Tạo và tham gia sự kiện")
        print("   - 🏆 Xếp hạng: Xem bảng xếp hạng thành viên")
        
        print("\n💡 Hướng dẫn sử dụng:")
        print("   1. Chọn tab '🏠 Cộng đồng' để tạo cộng đồng mới")
        print("   2. Chọn cộng đồng trong các tab khác để sử dụng chức năng")
        print("   3. Các chức năng sẽ tự động cập nhật điểm và xếp hạng")
        
        # Hiển thị window
        window.show()
        print("✅ Giao diện đã được hiển thị!")
        
        # Chạy ứng dụng
        print("🔄 Đang chạy ứng dụng... (Nhấn Ctrl+C để thoát)")
        sys.exit(app.exec())
        
    except ImportError as e:
        print(f"❌ UI Import error: {e}")
    except Exception as e:
        print(f"❌ UI demo failed: {e}")

if __name__ == "__main__":
    print("🚀 Community Features Demo")
    print("=" * 50)
    
    # Demo backend features
    demo_community_features()
    
    # Demo UI
    demo_ui() 