2. Current User Dependency (Authentication)

"""
    Dependency to get the current user from the access_token cookie.
    It validates the JWT, checks its payload, and fetches the user from the database.
    Raises HTTPException if the user is not authenticated or the token is invalid.
    """