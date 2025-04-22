from fastapi import APIRouter, Depends,  Request, HTTPException, status, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from Schemas.userSchema import UserCreate, UserOut, Token, UserLogin
from models.userModel import User
from database import get_db
from utils import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()

@router.post("/register", response_model = UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if not user.username or not user.email or not user.password:
        return JSONResponse(status_code=400, content={"message": "All feilds are required"})
    exsting_user = db.query(User).filter(User.username == user.username).first()
    if exsting_user:
        return JSONResponse(status_code=400, content={"message": "Username already exists"})
    
    hashed_password = hash_password(user.password)

    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return JSONResponse(status_code=200, content={
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "role": new_user.role,
            "is_activate": new_user.is_active
        },
        "message": "User registered successfully"
        })

    

@router.post("/login", response_model = Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    if not user.username or not user.password:
        return JSONResponse(status_code=400, content={"message": "All feilds are required"})
    
    existing_user = db.query(User).filter(User.username == user.username).first()
    if not existing_user:
        return JSONResponse(status_code=400, content={"message": "Invalid credentials"})
    
    if not verify_password(user.password, existing_user.hashed_password):
        return JSONResponse(status_code=400, content={"message": "Invalid credentials"})
    
    #user acitve
    existing_user.is_active = True
    db.commit()


    access_token = create_access_token(data={"sub": user.username})

    return JSONResponse(status_code=200, content={
        "user": {
            "user_id": existing_user.id,
            "username": existing_user.username,
            "email": existing_user.email,
            "role": existing_user.role
        },
        "access_token": access_token,
        "message": "Login successfully"
    })
    

@router.get("/profile")
def get_profile(request: Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if auth_header is None or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )       
    
    token = auth_header.split(" ")[1]
    if not token:
        return JSONResponse(status_code=401, content={"message": "Not authorized"})
    
       # Define the credentials_exception to pass in
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
   
    user = get_current_user(token, credentials_exception, db, User)

    return JSONResponse(status_code=200, content={
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_activate": user.is_active
        }
    })


@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)):

    user = get_current_user(request, db, User)
    #user active
    user.is_active = False
    db.commit()
    response.delete_cookie(key="Authorization")
    return JSONResponse(status_code=200, content={"message": "Logged out successfully"})

    