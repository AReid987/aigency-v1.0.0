
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2CIBearer
from jose import jwt
from pydantic import BaseModel
from typing import Optional

# This is a placeholder for your Auth0 domain and API audience
AUTH0_DOMAIN = "YOUR_AUTH0_DOMAIN"  # e.g., "dev-yourtenant.us.auth0.com"
API_AUDIENCE = "YOUR_AUTH0_API_AUDIENCE"  # e.g., "https://your-api-identifier"
ALGORITHMS = ["RS256"]

oauth2_scheme = OAuth2CIBearer(tokenUrl="/api/auth/login")

class TokenData(BaseModel):
    sub: Optional[str] = None

async def get_current_auth0_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        unverified_header = jwt.get_unverified_header(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if unverified_header["alg"] == "RS256":
        try:
            jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
            jwks = await jwt.get_jwks(jwks_url)
            payload = jwt.decode(
                token,
                jwks,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {e}",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unsupported algorithm",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenData(sub=payload["sub"])
