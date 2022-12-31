from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class DenyUnauthorized(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send_json({'action': 'auth'})
        await self.close()

class WSTodoemAuth(JWTStatelessUserAuthentication):
    
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store the ASGI application we were passed
        self.app = app


    async def get_cookies(self, headers):
        for header in headers:
            if header[0] == b'cookie':
                return header[1].decode()
        
        return None
    
    async def get_raw_token(self, cookies: str):
        for cookie in cookies.split('; '):
            if cookie.startswith('token='):
                token = cookie.split('=')
                return token[1]
        
        return None
    

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        try:
            headers = scope.get('headers', [])
            
            cookies = await self.get_cookies(headers)
            
            if cookies is None:
                raise


            raw_token = await self.get_raw_token(cookies)
            
            if raw_token is None:
                raise
            
            validated_token = self.get_validated_token(raw_token)
            
            scope['user'] = self.get_user(validated_token)
            
            return await self.app(scope, receive, send)
        except:
            denier = DenyUnauthorized()
            return await denier(scope, receive, send)
            