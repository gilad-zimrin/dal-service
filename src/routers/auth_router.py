from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm

from src.core.security import verify_password, create_access_token, Token
from src.managers import CompanyManager, CustomerManager

security_router = APIRouter(prefix="/auth", tags=["auth"])


@security_router.post("/login", response_model=Token)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    company_manager: CompanyManager = request.app.state.postgres_managers['Company']
    user = await company_manager.get_by_username(form_data.username)
    if not user:
        customer_manager: CompanyManager = request.app.state.postgres_managers['Customer']
        user = await customer_manager.get_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": form_data.username, "role": user.get("role", "user")})
    return {"access_token": access_token, "token_type": "bearer"}