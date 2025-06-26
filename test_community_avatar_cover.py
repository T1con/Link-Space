#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tự động test chức năng Avatar và Ảnh bìa cho Cộng đồng
"""

import os
import json
import shutil
import tempfile
from datetime import datetime
from community_features import CommunityFeatures

class CommunityAvatarCoverTester:
    def __init__(self):
        self.cf = CommunityFeatures()
        self.test_results = []
        self.test_communities = []
        
    def log_test(self, test_name, success, message=""):
        """Ghi log kết quả test"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        print(f"{status} {test_name}: {message}")
        return success
    
    def create_test_image(self, filename, size=(100, 100)):
        """Tạo file ảnh test"""
        try:
            # Tạo file ảnh đơn giản bằng cách copy từ file có sẵn
            test_image_path = os.path.join("data", "covers", "T1con.jpg")
            if os.path.exists(test_image_path):
                shutil.copy2(test_image_path, filename)
                return True
            else:
                # Tạo file ảnh giả
                with open(filename, 'w') as f:
                    f.write("fake_image_data")
                return True
        except Exception as e:
            print(f"Lỗi tạo file ảnh test: {e}")
            return False
    
    def test_create_community(self):
        """Test tạo cộng đồng mới"""
        print("\n=== TEST TẠO CỘNG ĐỒNG ===")
        
        # Test 1: Tạo cộng đồng với thông tin đầy đủ
        community_id = self.cf.create_community(
            name="Test Community 1",
            description="Cộng đồng test số 1",
            admin="test_user"
        )
        
        if community_id:
            community = self.cf.get_community_by_id(community_id)
            if community:
                success = (
                    community['name'] == "Test Community 1" and
                    community['description'] == "Cộng đồng test số 1" and
                    community['admin'] == "test_user" and
                    community.get('avatar') == "" and
                    community.get('cover') == "" and
                    "test_user" in community['members']
                )
                self.test_communities.append(community_id)
                return self.log_test("Tạo cộng đồng mới", success, f"ID: {community_id}")
        
        return self.log_test("Tạo cộng đồng mới", False, "Không thể tạo cộng đồng")
    
    def test_update_community_info(self):
        """Test cập nhật thông tin cộng đồng"""
        print("\n=== TEST CẬP NHẬT THÔNG TIN ===")
        
        if not self.test_communities:
            return self.log_test("Cập nhật thông tin", False, "Không có cộng đồng để test")
        
        community_id = self.test_communities[0]
        
        # Test cập nhật thông tin
        success = self.cf.update_community_info(
            community_id, 
            "Test Community Updated", 
            "Mô tả đã được cập nhật"
        )
        
        if success:
            community = self.cf.get_community_by_id(community_id)
            if community:
                info_updated = (
                    community['name'] == "Test Community Updated" and
                    community['description'] == "Mô tả đã được cập nhật"
                )
                return self.log_test("Cập nhật thông tin", info_updated, "Thông tin đã được cập nhật")
        
        return self.log_test("Cập nhật thông tin", False, "Không thể cập nhật thông tin")
    
    def test_upload_avatar(self):
        """Test upload avatar"""
        print("\n=== TEST UPLOAD AVATAR ===")
        
        if not self.test_communities:
            return self.log_test("Upload avatar", False, "Không có cộng đồng để test")
        
        community_id = self.test_communities[0]
        
        # Tạo file ảnh test
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            test_image_path = tmp_file.name
        
        if not self.create_test_image(test_image_path):
            return self.log_test("Upload avatar", False, "Không thể tạo file ảnh test")
        
        try:
            # Test upload avatar
            avatar_filename = f"test_community_{community_id}_avatar_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            success = self.cf.update_community_avatar(community_id, avatar_filename)
            
            if success:
                community = self.cf.get_community_by_id(community_id)
                if community and community.get('avatar') == avatar_filename:
                    return self.log_test("Upload avatar", True, f"Avatar: {avatar_filename}")
            
            return self.log_test("Upload avatar", False, "Không thể upload avatar")
            
        finally:
            # Dọn dẹp file test
            if os.path.exists(test_image_path):
                os.unlink(test_image_path)
    
    def test_upload_cover(self):
        """Test upload ảnh bìa"""
        print("\n=== TEST UPLOAD ẢNH BÌA ===")
        
        if not self.test_communities:
            return self.log_test("Upload ảnh bìa", False, "Không có cộng đồng để test")
        
        community_id = self.test_communities[0]
        
        # Tạo file ảnh test
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            test_image_path = tmp_file.name
        
        if not self.create_test_image(test_image_path):
            return self.log_test("Upload ảnh bìa", False, "Không thể tạo file ảnh test")
        
        try:
            # Test upload ảnh bìa
            cover_filename = f"test_community_{community_id}_cover_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            success = self.cf.update_community_cover(community_id, cover_filename)
            
            if success:
                community = self.cf.get_community_by_id(community_id)
                if community and community.get('cover') == cover_filename:
                    return self.log_test("Upload ảnh bìa", True, f"Cover: {cover_filename}")
            
            return self.log_test("Upload ảnh bìa", False, "Không thể upload ảnh bìa")
            
        finally:
            # Dọn dẹp file test
            if os.path.exists(test_image_path):
                os.unlink(test_image_path)
    
    def test_permissions(self):
        """Test quyền truy cập"""
        print("\n=== TEST QUYỀN TRUY CẬP ===")
        
        if not self.test_communities:
            return self.log_test("Test quyền", False, "Không có cộng đồng để test")
        
        community_id = self.test_communities[0]
        
        # Test admin permissions
        is_admin = self.cf.is_community_admin(community_id, "test_user")
        is_member = self.cf.is_community_member(community_id, "test_user")
        is_not_admin = not self.cf.is_community_admin(community_id, "other_user")
        is_not_member = not self.cf.is_community_member(community_id, "other_user")
        
        success = is_admin and is_member and is_not_admin and is_not_member
        
        return self.log_test("Test quyền", success, 
                           f"Admin: {is_admin}, Member: {is_member}, Not Admin: {is_not_admin}, Not Member: {is_not_member}")
    
    def test_data_integrity(self):
        """Test tính toàn vẹn dữ liệu"""
        print("\n=== TEST TÍNH TOÀN VẸN DỮ LIỆU ===")
        
        # Test load communities
        communities = self.cf.load_communities()
        if not isinstance(communities, list):
            return self.log_test("Tính toàn vẹn dữ liệu", False, "Communities không phải list")
        
        # Test cấu trúc dữ liệu
        for community in communities:
            required_fields = ['id', 'name', 'description', 'admin', 'members']
            for field in required_fields:
                if field not in community:
                    return self.log_test("Tính toàn vẹn dữ liệu", False, f"Thiếu field: {field}")
            
            # Test avatar và cover fields
            if 'avatar' not in community:
                return self.log_test("Tính toàn vẹn dữ liệu", False, "Thiếu field: avatar")
            if 'cover' not in community:
                return self.log_test("Tính toàn vẹn dữ liệu", False, "Thiếu field: cover")
        
        return self.log_test("Tính toàn vẹn dữ liệu", True, f"Kiểm tra {len(communities)} cộng đồng")
    
    def test_error_handling(self):
        """Test xử lý lỗi"""
        print("\n=== TEST XỬ LÝ LỖI ===")
        
        # Test với community_id không tồn tại
        non_existent_id = "nonexistent"
        
        # Test update avatar với ID không tồn tại
        avatar_result = self.cf.update_community_avatar(non_existent_id, "test.jpg")
        if not avatar_result:
            self.log_test("Xử lý lỗi - Avatar ID không tồn tại", True, "Đúng hành vi")
        else:
            self.log_test("Xử lý lỗi - Avatar ID không tồn tại", False, "Không xử lý lỗi đúng")
        
        # Test update cover với ID không tồn tại
        cover_result = self.cf.update_community_cover(non_existent_id, "test.jpg")
        if not cover_result:
            self.log_test("Xử lý lỗi - Cover ID không tồn tại", True, "Đúng hành vi")
        else:
            self.log_test("Xử lý lỗi - Cover ID không tồn tại", False, "Không xử lý lỗi đúng")
        
        # Test update info với ID không tồn tại
        info_result = self.cf.update_community_info(non_existent_id, "Test", "Test")
        if not info_result:
            self.log_test("Xử lý lỗi - Info ID không tồn tại", True, "Đúng hành vi")
        else:
            self.log_test("Xử lý lỗi - Info ID không tồn tại", False, "Không xử lý lỗi đúng")
        
        return True
    
    def test_web_integration(self):
        """Test tích hợp web"""
        print("\n=== TEST TÍCH HỢP WEB ===")
        
        # Kiểm tra các file template
        template_files = [
            "templates/communities.html",
            "templates/edit_community.html"
        ]
        
        for template_file in template_files:
            if os.path.exists(template_file):
                self.log_test(f"Template {template_file}", True, "File tồn tại")
            else:
                self.log_test(f"Template {template_file}", False, "File không tồn tại")
        
        # Kiểm tra route trong mobile_app.py
        try:
            with open("mobile_app.py", "r", encoding="utf-8") as f:
                content = f.read()
                
            required_routes = [
                "/community/<community_id>/upload_avatar",
                "/community/<community_id>/upload_cover", 
                "/community/<community_id>/edit"
            ]
            
            for route in required_routes:
                if route in content:
                    self.log_test(f"Route {route}", True, "Route tồn tại")
                else:
                    self.log_test(f"Route {route}", False, "Route không tồn tại")
                    
        except Exception as e:
            self.log_test("Kiểm tra routes", False, f"Lỗi đọc file: {e}")
        
        return True
    
    def cleanup_test_data(self):
        """Dọn dẹp dữ liệu test"""
        print("\n=== DỌN DẸP DỮ LIỆU TEST ===")
        
        communities = self.cf.load_communities()
        updated_communities = []
        
        for community in communities:
            # Xóa các cộng đồng test
            if (community.get('name', '').startswith('Test Community') or 
                community.get('admin') == 'test_user'):
                print(f"Xóa cộng đồng test: {community['name']} (ID: {community['id']})")
                continue
            updated_communities.append(community)
        
        # Lưu lại danh sách đã dọn dẹp
        with open(self.cf.communities_file, 'w', encoding='utf-8') as f:
            json.dump(updated_communities, f, indent=4, ensure_ascii=False)
        
        print(f"Đã dọn dẹp {len(communities) - len(updated_communities)} cộng đồng test")
    
    def generate_report(self):
        """Tạo báo cáo test"""
        print("\n" + "="*60)
        print("📊 BÁO CÁO KẾT QUẢ TEST")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Tổng số test: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Tỷ lệ thành công: {(passed_tests/total_tests*100):.1f}%")
        
        print("\n📋 CHI TIẾT KẾT QUẢ:")
        for result in self.test_results:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['test']}: {result['message']}")
        
        # Lưu báo cáo vào file
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=4, ensure_ascii=False)
        
        print(f"\n📄 Báo cáo đã được lưu vào: {report_file}")
        
        if failed_tests == 0:
            print("\n🎉 TẤT CẢ TEST ĐỀU THÀNH CÔNG!")
        else:
            print(f"\n⚠️ Có {failed_tests} test thất bại, vui lòng kiểm tra lại.")
    
    def run_all_tests(self):
        """Chạy tất cả test"""
        print("🚀 BẮT ĐẦU TỰ ĐỘNG TEST CHỨC NĂNG AVATAR VÀ ẢNH BÌA CỘNG ĐỒNG")
        print("="*70)
        
        # Chạy các test
        self.test_create_community()
        self.test_update_community_info()
        self.test_upload_avatar()
        self.test_upload_cover()
        self.test_permissions()
        self.test_data_integrity()
        self.test_error_handling()
        self.test_web_integration()
        
        # Dọn dẹp và tạo báo cáo
        self.cleanup_test_data()
        self.generate_report()

def main():
    """Hàm chính"""
    tester = CommunityAvatarCoverTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 