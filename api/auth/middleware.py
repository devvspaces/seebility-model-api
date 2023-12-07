from channels.db import database_sync_to_async

# TODO: Implement a ticket based middleware authentication
# 1. Generate ticket using jwt
# 2. Send ticket to client
# 3. Client sends ticket to server
# 4. Server verifies ticket
# 5. If ticket is valid, server sends response
# 6. If ticket is invalid, server sends error response
# then client can request a new ticket

# @database_sync_to_async
# def get_user(user_id):
#     try:
#         return User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         return AnonymousUser()

# class QueryAuthMiddleware:
#     """
#     Custom middleware (insecure) that takes user IDs from the query string.
#     """

#     def __init__(self, app):
#         # Store the ASGI application we were passed
#         self.app = app

#     async def __call__(self, scope, receive, send):
#         # Look up user from query string (you should also do things like
#         # checking if it is a valid user ID, or if scope["user"] is already
#         # populated).
#         jwt = scope["jwt"]
#         return await self.app(scope, receive, send)
