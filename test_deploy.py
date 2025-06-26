import sys
import os
import importlib
import json

MODULES_TO_TEST = [
    'main',
    'run_app',
    'src.MainWindow',
    'src.LoginWindow',
    'src.ProfileWindow',
    'src.SettingsWindow',
    'src.CommunityWindow',
    'src.MessageWindow',
    'src.PostWidget',
    'src.RegisterWindow',
    'src.community_features',
    'src.community_dialogs',
    'src.common',
    'src.utils',
]

JSON_FILES_TO_TEST = [
    'data/communities.json',
    'data/users.json',
    'data/posts.json',
    'data/messages.json',
    'data/pets.json',
    'data/characters.json',
    'data/community_events.json',
    'data/community_leaderboard.json',
    'data/community_polls.json',
    'data/community_topics.json',
    'data/stories.json',
]

FAILED = False

def test_imports():
    global FAILED
    print('--- Testing imports ---')
    for module in MODULES_TO_TEST:
        try:
            importlib.import_module(module)
            print(f'OK: {module}')
        except Exception as e:
            print(f'FAIL: {module} -> {e}')
            FAILED = True

def test_json_files():
    global FAILED
    print('\n--- Testing JSON files ---')
    for path in JSON_FILES_TO_TEST:
        if not os.path.exists(path):
            print(f'WARN: {path} does not exist')
            continue
        try:
            with open(path, encoding='utf-8') as f:
                json.load(f)
            print(f'OK: {path}')
        except Exception as e:
            print(f'FAIL: {path} -> {e}')
            FAILED = True

def test_flask_app():
    global FAILED
    print('\n--- Testing Flask app startup ---')
    try:
        from main import app
        with app.app_context():
            print('OK: Flask app context loaded')
    except Exception as e:
        print(f'FAIL: Flask app startup -> {e}')
        FAILED = True

def main():
    test_imports()
    test_json_files()
    test_flask_app()
    if FAILED:
        print('\nSome tests FAILED. Please check above.')
        sys.exit(1)
    else:
        print('\nAll tests PASSED.')
        sys.exit(0)

if __name__ == '__main__':
    main() 