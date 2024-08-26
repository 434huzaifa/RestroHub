from api.index import app
from ninja_extra import api_controller, route

@api_controller("/user",tags=['User'])
class UserAPI:
    @route.get("")
    def create_owner(self):
        pass