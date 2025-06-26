#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo các tính năng cộng đồng mới cho Link Space Web
"""

import json
import os
from community_features import CommunityFeatures
from datetime import datetime

def demo_community_features():
    """Demo các tính năng cộng đồng mới"""
    print("🚀 Demo các tính năng cộng đồng mới cho Link Space Web")
    print("=" * 60)
    
    # Khởi tạo CommunityFeatures
    cf = CommunityFeatures()
    
    # Tạo dữ liệu mẫu
    print("\n📝 Tạo dữ liệu mẫu...")
    
    # Tạo cộng đồng mẫu nếu chưa có
    communities = cf.load_communities()
    if not communities:
        sample_community = {
            "id": "demo_comm_001",
            "name": "Cộng đồng Game",
            "description": "Nơi chia sẻ về game và giải trí",
            "admin": "admin",
            "members": ["admin", "user1", "user2", "user3"]
        }
        communities.append(sample_community)
        with open(cf.communities_file, 'w', encoding='utf-8') as f:
            json.dump(communities, f, indent=4, ensure_ascii=False)
        print("✅ Đã tạo cộng đồng mẫu: Cộng đồng Game")
    
    community_id = "demo_comm_001"
    
    # Demo 1: Chủ đề thảo luận
    print("\n💬 Demo 1: Chủ đề thảo luận")
    print("-" * 30)
    
    # Tạo chủ đề
    topic_id = cf.create_topic(
        community_id=community_id,
        title="Game yêu thích nhất 2024",
        content="Các bạn thích game nào nhất trong năm 2024? Chia sẻ kinh nghiệm chơi game nhé!",
        author="user1"
    )
    print(f"✅ Đã tạo chủ đề: Game yêu thích nhất 2024 (ID: {topic_id})")
    
    # Thêm bình luận
    cf.add_topic_comment(topic_id, "Mình thích Genshin Impact, đồ họa đẹp quá!", "user2")
    cf.add_topic_comment(topic_id, "League of Legends vẫn là số 1 với mình", "user3")
    print("✅ Đã thêm 2 bình luận")
    
    # Like chủ đề
    cf.like_topic(topic_id, "user2")
    cf.like_topic(topic_id, "user3")
    print("✅ Đã like chủ đề")
    
    # Hiển thị chủ đề
    topic = cf.get_topic_by_id(topic_id)
    if topic:
        print(f"📊 Thống kê chủ đề:")
        print(f"   - Tiêu đề: {topic['title']}")
        print(f"   - Tác giả: {topic['author']}")
        print(f"   - Số bình luận: {len(topic['comments'])}")
        print(f"   - Số like: {len(topic['likes'])}")
    else:
        print("❌ Không tìm thấy chủ đề")
    
    # Demo 2: Bình chọn
    print("\n📊 Demo 2: Bình chọn")
    print("-" * 30)
    
    # Tạo bình chọn
    poll_id = cf.create_poll(
        community_id=community_id,
        question="Bạn thích thể loại game nào nhất?",
        options=["RPG", "FPS", "MOBA", "Strategy", "Puzzle"],
        author="user2",
        duration_days=14
    )
    print(f"✅ Đã tạo bình chọn: Bạn thích thể loại game nào nhất? (ID: {poll_id})")
    
    # Bình chọn
    cf.vote_poll(poll_id, 0, "user1")  # RPG
    cf.vote_poll(poll_id, 1, "user3")  # FPS
    cf.vote_poll(poll_id, 0, "admin")  # RPG
    print("✅ Đã có 3 người bình chọn")
    
    # Hiển thị kết quả
    results = cf.get_poll_results(poll_id)
    print("📊 Kết quả bình chọn:")
    for result in results:
        print(f"   - {result['text']}: {result['votes']} phiếu ({result['percentage']}%)")
    
    # Demo 3: Sự kiện
    print("\n📅 Demo 3: Sự kiện")
    print("-" * 30)
    
    # Tạo sự kiện
    event_id = cf.create_event(
        community_id=community_id,
        title="Gặp gỡ game thủ",
        description="Buổi gặp gỡ offline để chơi game và giao lưu với các game thủ trong cộng đồng",
        location="Quán cà phê Game Zone, 123 Đường ABC, TP.HCM",
        event_date="2024-12-25 19:00:00",
        author="user3",
        max_participants=20
    )
    print(f"✅ Đã tạo sự kiện: Gặp gỡ game thủ (ID: {event_id})")
    
    # Tham gia sự kiện
    cf.join_event(event_id, "user1")
    cf.join_event(event_id, "user2")
    cf.join_event(event_id, "admin")
    print("✅ Đã có 4 người tham gia sự kiện")
    
    # Hiển thị sự kiện
    events = cf.get_community_events(community_id)
    if events:
        event = events[0]
        print(f"📅 Thông tin sự kiện:")
        print(f"   - Tên: {event['title']}")
        print(f"   - Địa điểm: {event['location']}")
        print(f"   - Thời gian: {event['event_date']}")
        print(f"   - Số người tham gia: {len(event['participants'])}/{event['max_participants']}")
        print(f"   - Danh sách: {', '.join(event['participants'])}")
    
    # Demo 4: Bảng xếp hạng
    print("\n🏆 Demo 4: Bảng xếp hạng")
    print("-" * 30)
    
    # Hiển thị bảng xếp hạng
    leaderboard = cf.get_community_leaderboard(community_id)
    print("🏆 Bảng xếp hạng cộng đồng:")
    for i, member in enumerate(leaderboard, 1):
        print(f"   {i}. @{member['username']} - {member['points']} điểm (Level {member['level']})")
        if member['actions']:
            actions_str = ', '.join([f"{action}: {count}" for action, count in member['actions'].items()])
            print(f"      Hành động: {actions_str}")
    
    # Thống kê cá nhân
    print("\n📈 Thống kê cá nhân:")
    for username in ["user1", "user2", "user3"]:
        stats = cf.get_user_stats(username)
        print(f"   @{username}: {stats['total_points']} điểm, Level {stats['level']}")
    
    print("\n🎉 Demo hoàn thành!")
    print("\n📋 Hướng dẫn sử dụng:")
    print("1. Chạy web app: python mobile_app.py")
    print("2. Truy cập: http://localhost:5000")
    print("3. Đăng nhập và vào trang Cộng đồng")
    print("4. Chọn cộng đồng 'Cộng đồng Game' để xem các tính năng")
    print("5. Thử tạo chủ đề, bình chọn, sự kiện mới")

def demo_community_avatar_cover():
    """Demo chức năng avatar và ảnh bìa cho cộng đồng"""
    
    print("=== DEMO CHỨC NĂNG AVATAR VÀ ẢNH BÌA CHO CỘNG ĐỒNG ===\n")
    
    # Khởi tạo CommunityFeatures
    cf = CommunityFeatures()
    
    # Tạo cộng đồng mới
    print("1. Tạo cộng đồng mới...")
    community_id = cf.create_community(
        name="Cộng đồng Demo",
        description="Cộng đồng để test chức năng avatar và ảnh bìa",
        admin="demo_user"
    )
    print(f"   ✅ Đã tạo cộng đồng với ID: {community_id}")
    
    # Lấy thông tin cộng đồng
    print("\n2. Lấy thông tin cộng đồng...")
    community = cf.get_community_by_id(community_id)
    if community:
        print(f"   ✅ Tên: {community['name']}")
        print(f"   ✅ Mô tả: {community['description']}")
        print(f"   ✅ Admin: {community['admin']}")
        print(f"   ✅ Avatar: {community.get('avatar', 'Chưa có')}")
        print(f"   ✅ Cover: {community.get('cover', 'Chưa có')}")
    
    # Demo cập nhật avatar (giả lập)
    print("\n3. Demo cập nhật avatar...")
    avatar_filename = f"community_{community_id}_avatar_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    if cf.update_community_avatar(community_id, avatar_filename):
        print(f"   ✅ Đã cập nhật avatar: {avatar_filename}")
    else:
        print("   ❌ Lỗi khi cập nhật avatar")
    
    # Demo cập nhật ảnh bìa (giả lập)
    print("\n4. Demo cập nhật ảnh bìa...")
    cover_filename = f"community_{community_id}_cover_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    if cf.update_community_cover(community_id, cover_filename):
        print(f"   ✅ Đã cập nhật ảnh bìa: {cover_filename}")
    else:
        print("   ❌ Lỗi khi cập nhật ảnh bìa")
    
    # Lấy thông tin cập nhật
    print("\n5. Thông tin cộng đồng sau khi cập nhật...")
    community = cf.get_community_by_id(community_id)
    if community:
        print(f"   ✅ Avatar: {community.get('avatar', 'Chưa có')}")
        print(f"   ✅ Cover: {community.get('cover', 'Chưa có')}")
    
    # Demo cập nhật thông tin
    print("\n6. Demo cập nhật thông tin cộng đồng...")
    if cf.update_community_info(community_id, "Cộng đồng Demo Updated", "Mô tả đã được cập nhật"):
        print("   ✅ Đã cập nhật thông tin cộng đồng")
    else:
        print("   ❌ Lỗi khi cập nhật thông tin")
    
    # Kiểm tra quyền
    print("\n7. Kiểm tra quyền...")
    print(f"   ✅ Là admin: {cf.is_community_admin(community_id, 'demo_user')}")
    print(f"   ✅ Là thành viên: {cf.is_community_member(community_id, 'demo_user')}")
    print(f"   ✅ Không phải admin: {cf.is_community_admin(community_id, 'other_user')}")
    
    # Hiển thị tất cả cộng đồng
    print("\n8. Danh sách tất cả cộng đồng...")
    communities = cf.load_communities()
    for i, comm in enumerate(communities, 1):
        print(f"   {i}. {comm['name']} (ID: {comm['id']})")
        print(f"      Avatar: {comm.get('avatar', 'Chưa có')}")
        print(f"      Cover: {comm.get('cover', 'Chưa có')}")
    
    print("\n=== HOÀN THÀNH DEMO ===")
    print("Để test trên web:")
    print("1. Chạy: python mobile_app.py")
    print("2. Truy cập: http://localhost:5000")
    print("3. Đăng nhập và vào trang Communities")
    print("4. Tạo cộng đồng mới hoặc chỉnh sửa cộng đồng hiện có")
    print("5. Upload avatar và ảnh bìa cho cộng đồng")

if __name__ == "__main__":
    demo_community_features()
    demo_community_avatar_cover() 