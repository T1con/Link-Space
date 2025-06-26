#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script cho các chức năng cộng đồng mới
"""

import sys
import os

# Thêm thư mục src vào path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_community_features():
    """Test các chức năng cộng đồng mới"""
    print("🧪 Testing Community Features...")
    
    try:
        from community_features import CommunityFeatures
        
        # Khởi tạo
        features = CommunityFeatures()
        print("✅ CommunityFeatures initialized successfully")
        
        # Test tạo chủ đề
        print("\n📝 Testing Topic Creation...")
        topic_id = features.create_topic("4d49a97b", "Test Topic", "This is a test topic", "T1con")
        print(f"✅ Topic created with ID: {topic_id}")
        
        # Test tạo bình chọn
        print("\n📊 Testing Poll Creation...")
        poll_id = features.create_poll("4d49a97b", "Test Poll", ["Option 1", "Option 2", "Option 3"], "T1con")
        print(f"✅ Poll created with ID: {poll_id}")
        
        # Test tạo sự kiện
        print("\n🎉 Testing Event Creation...")
        event_id = features.create_event("4d49a97b", "Test Event", "This is a test event", "Test Location", "2024-12-31 18:00:00", "T1con")
        print(f"✅ Event created with ID: {event_id}")
        
        # Test bảng xếp hạng
        print("\n🏆 Testing Leaderboard...")
        leaderboard = features.get_community_leaderboard("4d49a97b")
        print(f"✅ Leaderboard loaded: {len(leaderboard)} members")
        
        # Test vote
        print("\n🗳️ Testing Poll Voting...")
        success, message = features.vote_poll(poll_id, 0, "T1con")
        print(f"✅ Vote result: {message}")
        
        # Test join event
        print("\n✅ Testing Event Joining...")
        success, message = features.join_event(event_id, "T1con")
        print(f"✅ Join result: {message}")
        
        print("\n🎉 All tests passed successfully!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all required files are in the src/ directory")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def test_ui_components():
    """Test các component UI"""
    print("\n🖥️ Testing UI Components...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from CommunityWindow import CommunityWindow
        
        app = QApplication(sys.argv)
        print("✅ QApplication created successfully")
        
        window = CommunityWindow("T1con")
        print("✅ CommunityWindow created successfully")
        
        print("✅ UI components test passed!")
        
    except ImportError as e:
        print(f"❌ UI Import error: {e}")
    except Exception as e:
        print(f"❌ UI test failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting Community Features Test Suite...")
    print("=" * 50)
    
    # Test backend features
    test_community_features()
    
    # Test UI components
    test_ui_components()
    
    print("\n" + "=" * 50)
    print("🏁 Test Suite Completed!") 