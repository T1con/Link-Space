import os
import json
import uuid
from datetime import datetime, timedelta
from collections import Counter

class CommunityFeatures:
    def __init__(self):
        self.communities_file = "data/communities.json"
        self.topics_file = "data/community_topics.json"
        self.polls_file = "data/community_polls.json"
        self.events_file = "data/community_events.json"
        self.leaderboard_file = "data/community_leaderboard.json"
        
        # Khởi tạo các file nếu chưa tồn tại
        self.init_data_files()
    
    def init_data_files(self):
        """Khởi tạo các file dữ liệu nếu chưa tồn tại"""
        files = [
            (self.topics_file, []),
            (self.polls_file, []),
            (self.events_file, []),
            (self.leaderboard_file, {})
        ]
        
        for file_path, default_data in files:
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(default_data, f, indent=4, ensure_ascii=False)
    
    # ==================== CHỦ ĐỀ THẢO LUẬN (TOPICS) ====================
    
    def create_topic(self, community_id, title, content, author):
        """Tạo chủ đề thảo luận mới"""
        topic = {
            "id": str(uuid.uuid4())[:8],
            "community_id": community_id,
            "title": title,
            "content": content,
            "author": author,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "comments": [],
            "likes": [],
            "views": 0
        }
        
        topics = self.load_topics()
        topics.append(topic)
        self.save_topics(topics)
        
        # Cập nhật điểm cho người tạo chủ đề
        self.update_leaderboard(author, "create_topic", 10)
        
        return topic["id"]
    
    def add_topic_comment(self, topic_id, content, author):
        """Thêm bình luận vào chủ đề"""
        topics = self.load_topics()
        for topic in topics:
            if topic["id"] == topic_id:
                comment = {
                    "id": str(uuid.uuid4())[:8],
                    "content": content,
                    "author": author,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "likes": []
                }
                topic["comments"].append(comment)
                self.save_topics(topics)
                
                # Cập nhật điểm cho người bình luận
                self.update_leaderboard(author, "comment", 2)
                return True
        return False
    
    def like_topic(self, topic_id, username):
        """Like/unlike chủ đề"""
        topics = self.load_topics()
        for topic in topics:
            if topic["id"] == topic_id:
                if username in topic["likes"]:
                    topic["likes"].remove(username)
                else:
                    topic["likes"].append(username)
                    # Cập nhật điểm cho người tạo chủ đề
                    self.update_leaderboard(topic["author"], "receive_like", 1)
                self.save_topics(topics)
                return True
        return False
    
    def get_community_topics(self, community_id):
        """Lấy danh sách chủ đề của cộng đồng"""
        topics = self.load_topics()
        return [t for t in topics if t["community_id"] == community_id]
    
    def get_topic_by_id(self, topic_id):
        """Lấy thông tin chủ đề theo ID"""
        topics = self.load_topics()
        for topic in topics:
            if topic["id"] == topic_id:
                return topic
        return None
    
    def load_topics(self):
        """Load danh sách chủ đề"""
        if os.path.exists(self.topics_file):
            with open(self.topics_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_topics(self, topics):
        """Lưu danh sách chủ đề"""
        with open(self.topics_file, 'w', encoding='utf-8') as f:
            json.dump(topics, f, indent=4, ensure_ascii=False)
    
    # ==================== BÌNH CHỌN (POLLS) ====================
    
    def create_poll(self, community_id, question, options, author, duration_days=7):
        """Tạo cuộc bình chọn mới"""
        poll = {
            "id": str(uuid.uuid4())[:8],
            "community_id": community_id,
            "question": question,
            "options": [{"text": opt, "votes": 0, "voters": []} for opt in options],
            "author": author,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "end_date": (datetime.now() + timedelta(days=duration_days)).strftime("%Y-%m-%d %H:%M:%S"),
            "voters": []  # Danh sách người đã bình chọn
        }
        
        polls = self.load_polls()
        polls.append(poll)
        self.save_polls(polls)
        
        # Cập nhật điểm cho người tạo bình chọn
        self.update_leaderboard(author, "create_poll", 5)
        
        return poll["id"]
    
    def vote_poll(self, poll_id, option_index, username):
        """Bình chọn trong cuộc thăm dò"""
        polls = self.load_polls()
        for poll in polls:
            if poll["id"] == poll_id:
                # Kiểm tra xem đã bình chọn chưa
                if username in poll["voters"]:
                    return False, "Bạn đã bình chọn rồi!"
                
                # Kiểm tra thời hạn
                end_date = datetime.strptime(poll["end_date"], "%Y-%m-%d %H:%M:%S")
                if datetime.now() > end_date:
                    return False, "Cuộc bình chọn đã kết thúc!"
                
                # Thêm bình chọn
                if 0 <= option_index < len(poll["options"]):
                    poll["options"][option_index]["votes"] += 1
                    poll["options"][option_index]["voters"].append(username)
                    poll["voters"].append(username)
                    self.save_polls(polls)
                    
                    # Cập nhật điểm cho người bình chọn
                    self.update_leaderboard(username, "vote", 1)
                    return True, "Bình chọn thành công!"
                else:
                    return False, "Lựa chọn không hợp lệ!"
        return False, "Không tìm thấy cuộc bình chọn!"
    
    def get_community_polls(self, community_id):
        """Lấy danh sách bình chọn của cộng đồng"""
        polls = self.load_polls()
        return [p for p in polls if p["community_id"] == community_id]
    
    def get_poll_results(self, poll_id):
        """Lấy kết quả bình chọn"""
        polls = self.load_polls()
        for poll in polls:
            if poll["id"] == poll_id:
                total_votes = sum(opt["votes"] for opt in poll["options"])
                results = []
                for opt in poll["options"]:
                    percentage = (opt["votes"] / total_votes * 100) if total_votes > 0 else 0
                    results.append({
                        "text": opt["text"],
                        "votes": opt["votes"],
                        "percentage": round(percentage, 1)
                    })
                return results
        return []
    
    def load_polls(self):
        """Load danh sách bình chọn"""
        if os.path.exists(self.polls_file):
            with open(self.polls_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_polls(self, polls):
        """Lưu danh sách bình chọn"""
        with open(self.polls_file, 'w', encoding='utf-8') as f:
            json.dump(polls, f, indent=4, ensure_ascii=False)
    
    # ==================== SỰ KIỆN CỘNG ĐỒNG (EVENTS) ====================
    
    def create_event(self, community_id, title, description, location, event_date, author, max_participants=None):
        """Tạo sự kiện mới"""
        event = {
            "id": str(uuid.uuid4())[:8],
            "community_id": community_id,
            "title": title,
            "description": description,
            "location": location,
            "event_date": event_date,
            "author": author,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "participants": [author],  # Tác giả tự động tham gia
            "max_participants": max_participants,
            "status": "upcoming"  # upcoming, ongoing, completed, cancelled
        }
        
        events = self.load_events()
        events.append(event)
        self.save_events(events)
        
        # Cập nhật điểm cho người tạo sự kiện
        self.update_leaderboard(author, "create_event", 15)
        
        return event["id"]
    
    def join_event(self, event_id, username):
        """Tham gia sự kiện"""
        events = self.load_events()
        for event in events:
            if event["id"] == event_id:
                if username in event["participants"]:
                    return False, "Bạn đã tham gia sự kiện này rồi!"
                
                if event["max_participants"] and len(event["participants"]) >= event["max_participants"]:
                    return False, "Sự kiện đã đầy người tham gia!"
                
                event["participants"].append(username)
                self.save_events(events)
                
                # Cập nhật điểm cho người tham gia
                self.update_leaderboard(username, "join_event", 3)
                return True, "Tham gia sự kiện thành công!"
        return False, "Không tìm thấy sự kiện!"
    
    def leave_event(self, event_id, username):
        """Rời khỏi sự kiện"""
        events = self.load_events()
        for event in events:
            if event["id"] == event_id:
                if username in event["participants"]:
                    event["participants"].remove(username)
                    self.save_events(events)
                    return True, "Đã rời khỏi sự kiện!"
        return False, "Không tìm thấy sự kiện!"
    
    def get_community_events(self, community_id):
        """Lấy danh sách sự kiện của cộng đồng"""
        events = self.load_events()
        return [e for e in events if e["community_id"] == community_id]
    
    def get_upcoming_events(self, community_id, days=30):
        """Lấy sự kiện sắp tới trong X ngày"""
        events = self.get_community_events(community_id)
        cutoff_date = datetime.now() + timedelta(days=days)
        upcoming = []
        
        for event in events:
            try:
                event_date = datetime.strptime(event["event_date"], "%Y-%m-%d %H:%M:%S")
                if datetime.now() <= event_date <= cutoff_date:
                    upcoming.append(event)
            except:
                continue
        
        return sorted(upcoming, key=lambda x: x["event_date"])
    
    def load_events(self):
        """Load danh sách sự kiện"""
        if os.path.exists(self.events_file):
            with open(self.events_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_events(self, events):
        """Lưu danh sách sự kiện"""
        with open(self.events_file, 'w', encoding='utf-8') as f:
            json.dump(events, f, indent=4, ensure_ascii=False)
    
    # ==================== BẢNG XẾP HẠNG (LEADERBOARD) ====================
    
    def update_leaderboard(self, username, action, points):
        """Cập nhật điểm cho thành viên"""
        leaderboard = self.load_leaderboard()
        
        if username not in leaderboard:
            leaderboard[username] = {
                "total_points": 0,
                "actions": {},
                "level": 1
            }
        
        # Cập nhật điểm tổng
        leaderboard[username]["total_points"] += points
        
        # Cập nhật số lần thực hiện hành động
        if action not in leaderboard[username]["actions"]:
            leaderboard[username]["actions"][action] = 0
        leaderboard[username]["actions"][action] += 1
        
        # Tính level (mỗi 100 điểm = 1 level)
        leaderboard[username]["level"] = (leaderboard[username]["total_points"] // 100) + 1
        
        self.save_leaderboard(leaderboard)
    
    def get_community_leaderboard(self, community_id, limit=10):
        """Lấy bảng xếp hạng của cộng đồng"""
        # Lấy danh sách thành viên cộng đồng
        communities = self.load_communities()
        community = None
        for c in communities:
            if c["id"] == community_id:
                community = c
                break
        
        if not community:
            return []
        
        # Lấy điểm của các thành viên
        leaderboard = self.load_leaderboard()
        member_scores = []
        
        for member in community.get("members", []):
            if member in leaderboard:
                member_scores.append({
                    "username": member,
                    "points": leaderboard[member]["total_points"],
                    "level": leaderboard[member]["level"],
                    "actions": leaderboard[member]["actions"]
                })
            else:
                member_scores.append({
                    "username": member,
                    "points": 0,
                    "level": 1,
                    "actions": {}
                })
        
        # Sắp xếp theo điểm cao nhất
        member_scores.sort(key=lambda x: x["points"], reverse=True)
        return member_scores[:limit]
    
    def get_user_stats(self, username):
        """Lấy thống kê của người dùng"""
        leaderboard = self.load_leaderboard()
        if username in leaderboard:
            return leaderboard[username]
        return {
            "total_points": 0,
            "actions": {},
            "level": 1
        }
    
    def load_leaderboard(self):
        """Load bảng xếp hạng"""
        if os.path.exists(self.leaderboard_file):
            with open(self.leaderboard_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_leaderboard(self, leaderboard):
        """Lưu bảng xếp hạng"""
        with open(self.leaderboard_file, 'w', encoding='utf-8') as f:
            json.dump(leaderboard, f, indent=4, ensure_ascii=False)
    
    # ==================== HÀM TIỆN ÍCH ====================
    
    def load_communities(self):
        """Load danh sách cộng đồng"""
        if os.path.exists(self.communities_file):
            with open(self.communities_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def get_community_by_id(self, community_id):
        """Lấy thông tin cộng đồng theo ID"""
        communities = self.load_communities()
        for community in communities:
            if community["id"] == community_id:
                return community
        return None
    
    def create_community(self, name, description, admin):
        """Tạo cộng đồng mới"""
        communities = self.load_communities()
        new_community = {
            "id": str(uuid.uuid4())[:8],
            "name": name,
            "description": description,
            "admin": admin,
            "members": [admin],
            "avatar": "",  # Avatar mặc định
            "cover": "",   # Ảnh bìa mặc định
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        communities.append(new_community)
        
        with open(self.communities_file, 'w', encoding='utf-8') as f:
            json.dump(communities, f, indent=4, ensure_ascii=False)
        
        return new_community["id"]
    
    def update_community_avatar(self, community_id, avatar_filename):
        """Cập nhật avatar cho cộng đồng"""
        communities = self.load_communities()
        for community in communities:
            if community["id"] == community_id:
                community["avatar"] = avatar_filename
                with open(self.communities_file, 'w', encoding='utf-8') as f:
                    json.dump(communities, f, indent=4, ensure_ascii=False)
                return True
        return False
    
    def update_community_cover(self, community_id, cover_filename):
        """Cập nhật ảnh bìa cho cộng đồng"""
        communities = self.load_communities()
        for community in communities:
            if community["id"] == community_id:
                community["cover"] = cover_filename
                with open(self.communities_file, 'w', encoding='utf-8') as f:
                    json.dump(communities, f, indent=4, ensure_ascii=False)
                return True
        return False
    
    def update_community_info(self, community_id, name, description):
        """Cập nhật thông tin cộng đồng"""
        communities = self.load_communities()
        for community in communities:
            if community["id"] == community_id:
                community["name"] = name
                community["description"] = description
                with open(self.communities_file, 'w', encoding='utf-8') as f:
                    json.dump(communities, f, indent=4, ensure_ascii=False)
                return True
        return False
    
    def is_community_member(self, community_id, username):
        """Kiểm tra xem user có phải thành viên cộng đồng không"""
        community = self.get_community_by_id(community_id)
        if community:
            return username in community.get("members", [])
        return False
    
    def is_community_admin(self, community_id, username):
        """Kiểm tra xem user có phải admin cộng đồng không"""
        community = self.get_community_by_id(community_id)
        if community:
            return community.get("admin") == username
        return False 