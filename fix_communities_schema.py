#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tự động sửa schema communities.json: đảm bảo mọi cộng đồng đều có trường avatar và cover.
"""
import json
import os

COMMUNITIES_FILE = 'data/communities.json'


def fix_communities_schema():
    if not os.path.exists(COMMUNITIES_FILE):
        print(f"File {COMMUNITIES_FILE} không tồn tại!")
        return
    
    with open(COMMUNITIES_FILE, 'r', encoding='utf-8') as f:
        communities = json.load(f)
    
    changed = False
    for community in communities:
        if 'avatar' not in community:
            community['avatar'] = ''
            changed = True
        if 'cover' not in community:
            community['cover'] = ''
            changed = True
    
    if changed:
        with open(COMMUNITIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(communities, f, indent=4, ensure_ascii=False)
        print('Đã cập nhật schema cho các cộng đồng thiếu trường avatar/cover.')
    else:
        print('Tất cả cộng đồng đã có đủ trường avatar và cover.')

if __name__ == '__main__':
    fix_communities_schema() 