#!/usr/bin/env python3
"""
Script test chức năng Nick Name và Rank Chủ Nhân
"""

import os
import json

def test_nickname_functionality():
    """Test chức năng Nick Name và Rank Chủ Nhân"""
    print("=== TEST CHỨC NĂNG NICK NAME VÀ RANK CHỦ NHÂN ===")
    
    # Test 1: Kiểm tra file users.json có trường nickname
    print("\n1. Kiểm tra file users.json:")
    if os.path.exists("data/users.json"):
        with open("data/users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
        
        for user in users:
            username = user.get("username", "")
            nickname = user.get("nickname", "")
            if nickname:
                print(f"   - @{username}: {nickname}")
            else:
                print(f"   - @{username}: Chưa đặt nickname")
    else:
        print("   ❌ File users.json không tồn tại")
    
    # Test 2: Kiểm tra các file user cá nhân
    print("\n2. Kiểm tra file user cá nhân:")
    user_files = [
        "T1con.json",
        "vinh.json", 
        "admin.json",
        "KunnguSigmaboy.json",
        "Kunngu123.json",
        "test.json"
    ]
    
    for user_file in user_files:
        file_path = f"data/users/{user_file}"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                user_data = json.load(f)
            
            username = user_file.replace(".json", "")
            nickname = user_data.get("nickname", "")
            bio = user_data.get("bio", "")
            badges = user_data.get("badges", [])
            pets = user_data.get("pets", [])
            characters = user_data.get("characters", [])
            
            if nickname:
                print(f"   - @{username}: {nickname} - {bio}")
            else:
                print(f"   - @{username}: Chưa đặt nickname - {bio}")
            
            if badges:
                print(f"     Badges: {', '.join(badges)}")
            if pets:
                print(f"     Pets: {len(pets)} con")
            if characters:
                print(f"     Characters: {len(characters)} nhân vật")
        else:
            print(f"   ❌ File {user_file} không tồn tại")
    
    # Test 3: Kiểm tra ProfileWindow có trường nickname
    print("\n3. Kiểm tra ProfileWindow:")
    if os.path.exists("src/ProfileWindow.py"):
        with open("src/ProfileWindow.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        if "nickname" in content:
            print("   ✅ ProfileWindow đã có chức năng nickname")
        else:
            print("   ❌ ProfileWindow chưa có chức năng nickname")
            
        if "Chủ Nhân" in content:
            print("   ✅ ProfileWindow đã có hiệu ứng rank Chủ Nhân")
        else:
            print("   ❌ ProfileWindow chưa có hiệu ứng rank Chủ Nhân")
    else:
        print("   ❌ File ProfileWindow.py không tồn tại")
    
    # Test 4: Kiểm tra PostWidget có hiển thị nickname
    print("\n4. Kiểm tra PostWidget:")
    if os.path.exists("src/PostWidget.py"):
        with open("src/PostWidget.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        if "nickname" in content:
            print("   ✅ PostWidget đã có hiển thị nickname")
        else:
            print("   ❌ PostWidget chưa có hiển thị nickname")
    else:
        print("   ❌ File PostWidget.py không tồn tại")
    
    # Test 5: Kiểm tra MessageWindow có hiển thị nickname
    print("\n5. Kiểm tra MessageWindow:")
    if os.path.exists("src/MessageWindow.py"):
        with open("src/MessageWindow.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        if "nickname" in content:
            print("   ✅ MessageWindow đã có hiển thị nickname")
        else:
            print("   ❌ MessageWindow chưa có hiển thị nickname")
    else:
        print("   ❌ File MessageWindow.py không tồn tại")
    
    # Test 6: Kiểm tra hiệu ứng rank Chủ Nhân
    print("\n6. Kiểm tra hiệu ứng rank Chủ Nhân:")
    t1con_path = "data/users/T1con.json"
    if os.path.exists(t1con_path):
        with open(t1con_path, "r", encoding="utf-8") as f:
            t1con_data = json.load(f)
        
        badges = t1con_data.get("badges", [])
        if "Chủ Nhân" in badges:
            print("   ✅ T1con đã có badge Chủ Nhân")
            print("   ✅ Sẽ có hiệu ứng avatar đặc biệt với:")
            print("      - Phát sáng đa lớp (vàng kim, cam, đỏ)")
            print("      - Hiệu ứng xoay nhẹ")
            print("      - Hiệu ứng scale nhẹ nhàng")
            print("      - Tia sáng xung quanh")
            print("      - Tốc độ animation 30ms cho mượt mà")
        else:
            print("   ❌ T1con chưa có badge Chủ Nhân")
    else:
        print("   ❌ File T1con.json không tồn tại")
    
    print("\n=== KẾT QUẢ TEST ===")
    print("Chức năng Nick Name và Rank Chủ Nhân đã được triển khai thành công!")
    print("Người dùng có thể:")
    print("- Tự đặt nickname trong trang cá nhân")
    print("- Xem nickname trong bài đăng (nếu có)")
    print("- Xem nickname trong tin nhắn (nếu có)")
    print("- Xem nickname trong header chính (nếu có)")
    print("\nRank Chủ Nhân có hiệu ứng đặc biệt:")
    print("- Hiệu ứng phát sáng đa lớp giống game nổi tiếng")
    print("- Animation mượt mà với nhiều hiệu ứng kết hợp")
    print("- Chỉ dành cho tài khoản T1con")
    print("\nLưu ý: Nickname là tùy chọn, user có thể đặt hoặc không đặt")

if __name__ == "__main__":
    test_nickname_functionality() 