import os
import re

def check_sensitive_data():
    sensitive_patterns = [
        r'[a-zA-Z0-9]{32,}',  # Long alphanumeric strings (API keys)
        r'password\s*=',
        r'secret\s*=',
        r'token\s*=',
    ]
    
    checked_files = []
    issues = []
    
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '__pycache__' in root or '.venv' in root:
            continue
            
        for file in files:
            if file in ['.env']:
                continue
            if file.endswith('.pyc'):
                continue
                
            filepath = os.path.join(root, file)
            
            if file.endswith(('.py', '.md', '.txt', '.json', '.yaml', '.yml')):
                checked_files.append(filepath)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        for pattern in sensitive_patterns:
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            if matches and file != '.env.example':
                                for match in matches:
                                    if 'your_' not in match.lower():
                                        issues.append({
                                            'file': filepath,
                                            'pattern': pattern,
                                            'match': match[:50] + '...' if len(match) > 50 else match
                                        })
                except Exception as e:
                    print(f"Warning: Could not read {filepath}: {e}")
    
    return checked_files, issues

def verify_files():
    required_files = [
        '.env.example',
        '.gitignore',
        'requirements.txt',
        'config.py',
        'README.md'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    return missing_files

def main():
    print("=" * 60)
    print("Security Verification Check")
    print("=" * 60)
    
    print("\n[1] Checking required files...")
    missing_files = verify_files()
    if missing_files:
        print(f"[X] Missing files: {missing_files}")
    else:
        print("[OK] All required files present")
    
    print("\n[2] Checking for sensitive data in code...")
    checked_files, issues = check_sensitive_data()
    
    if issues:
        print(f"[X] Found potential issues in {len(issues)} places:")
        for issue in issues:
            print(f"  - {issue['file']}: {issue['match']}")
    else:
        print(f"[OK] No sensitive data found in {len(checked_files)} checked files")
    
    print("\n[3] Checking .gitignore...")
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            content = f.read()
            if '.env' in content:
                print("[OK] .env is in .gitignore")
            else:
                print("[X] .env is NOT in .gitignore")
    
    print("\n" + "=" * 60)
    print("Security check complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
