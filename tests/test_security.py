from jose import jwt
from backend.app.core import security

def test_password_hashing():
    password = "mysecretpassword"
    hashed_password = security.get_password_hash(password)
    
    assert hashed_password != password
    assert security.verify_password(password, hashed_password)
    assert not security.verify_password("wrongpassword", hashed_password)

def test_create_and_validate_csrf_token():
    csrf_token = security.create_csrf_token()

    assert isinstance(csrf_token, str)
    
    assert security.validate_csrf_token(csrf_token) is True
    
    invalid_token = csrf_token + "invalid"
    assert security.validate_csrf_token(invalid_token) is False
    
    wrong_key_token = jwt.encode(
        {"purpose": "csrf"}, "WRONG_KEY", algorithm=security.ALGORITHM
    )
    assert security.validate_csrf_token(wrong_key_token) is False