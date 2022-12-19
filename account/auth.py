from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication

class WSTodoemAuth(JWTStatelessUserAuthentication):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store the ASGI application we were passed
        self.app = app
#! Implement later
    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        raw_token = self.get_raw_token(header)
        validated_token = self.get_validated_token(raw_token)
        scope['user'], token = self.authenticate(scope["headers"])

        return await self.app(scope, receive, send)