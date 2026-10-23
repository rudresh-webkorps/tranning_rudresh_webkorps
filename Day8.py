import json
import hashlib
import secrets
from datetime import datetime, timezone
from pathlib import Path

DB_FILE = Path('users.json')

# ---------- storage layer ----------
def load_users() -> list[dict]:
    if not DB_FILE.exists():
        return []
    try:
        with DB_FILE.open(encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print('Warning: users.json is corrupted. Starting empty.')
        return []

def save_users(users: list[dict]) -> None:
    tmp = DB_FILE.with_suffix('.tmp')
    with tmp.open('w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)
    tmp.replace(DB_FILE)   # atomic swap: file is never half-written

# ---------- security ----------
def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), 200_000)
    return digest.hex(), salt

# ---------- CRUD ----------
def add_user(name: str, email: str, password: str) -> dict:
    users = load_users()
    if any(u['email'].lower() == email.lower() for u in users):
        raise ValueError('Email already registered')
    pw_hash, salt = hash_password(password)
    user = {
        'id': max((u['id'] for u in users), default=0) + 1,
        'name': name.strip(),
        'email': email.lower().strip(),
        'password_hash': pw_hash,
        'salt': salt,
        'created_at': datetime.now(timezone.utc).isoformat(),
    }
    users.append(user)
    save_users(users)
    return user

def get_user(user_id: int) -> dict | None:
    return next((u for u in load_users() if u['id'] == user_id), None)

def update_user(user_id: int, **changes) -> bool:
    users = load_users()
    for u in users:
        if u['id'] == user_id:
            u.update({k: v for k, v in changes.items() if k in ('name', 'email')})
            save_users(users)
            return True
    return False

def delete_user(user_id: int) -> bool:
    users = load_users()
    remaining = [u for u in users if u['id'] != user_id]
    if len(remaining) == len(users):
        return False
    save_users(remaining)
    return True

def verify_login(email: str, password: str) -> bool:
    for u in load_users():
        if u['email'] == email.lower():
            h, _ = hash_password(password, u['salt'])
            return secrets.compare_digest(h, u['password_hash'])
    return False

# ---------- menu ----------
def main() -> None:
    while True:
        print('1.Add  2.List  3.Update  4.Delete  5.Login test  0.Exit')
        choice = input('Choose: ').strip()
        try:
            if choice == '1':
                u = add_user(input('Name: '), input('Email: '), input('Password: '))
                print('Created user', u['id'])
            elif choice == '2':
                for u in load_users():
                    print(u['id'], u['name'], u['email'])
            elif choice == '3':
                ok = update_user(int(input('ID: ')), name=input('New name: '))
                print('Updated' if ok else 'Not found')
            elif choice == '4':
                print('Deleted' if delete_user(int(input('ID: '))) else 'Not found')
            elif choice == '5':
                print('OK' if verify_login(input('Email: '), input('Password: ')) else 'Wrong')
            elif choice == '0':
                break
        except ValueError as e:
            print('Error:', e)

if __name__ == '__main__':
    main()
