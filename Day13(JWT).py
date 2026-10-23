from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET_KEY = settings.secret_key          # from .env, long random string
ALGORITHM = 'HS256'
EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')
router = APIRouter(prefix='/auth', tags=['Auth'])

def create_access_token(user_id: int) -> str:
    payload = {
        'sub': str(user_id),
        'exp': datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@router.post('/register', status_code=201)
def register(data: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.scalar(select(models.User).where(models.User.email == data.email)):
        raise HTTPException(409, 'Email already registered')
    user = models.User(email=data.email, password_hash=password_hash.hash(data.password))
    db.add(user); db.commit()
    return {'message': 'User created'}

@router.post('/login')
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.scalar(select(models.User).where(models.User.email == form.username))
    if not user or not password_hash.verify(form.password, user.password_hash):
        raise HTTPException(401, 'Invalid credentials', headers={'WWW-Authenticate': 'Bearer'})
    return {'access_token': create_access_token(user.id), 'token_type': 'bearer'}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    error = HTTPException(401, 'Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload['sub'])
    except (InvalidTokenError, KeyError, ValueError):
        raise error
    user = db.get(models.User, user_id)
    if not user:
        raise error
    return user

    @router.get('/me')
def me(user: models.User = Depends(get_current_user)):
    return {'id': user.id, 'email': user.email}

@notes_router.get('/')
def my_notes(user = Depends(get_current_user), db = Depends(get_db)):
    return db.scalars(select(models.Note).where(models.Note.owner_id == user.id)).all()
