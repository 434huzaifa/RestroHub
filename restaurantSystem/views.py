from django.shortcuts import render
from ninja_extra import NinjaExtraAPI,api_controller,route
# Create your views here.
app=NinjaExtraAPI()

# @api_controller('/test',tags=['Test'],permissions=[])
# class TestingApi:
#     @route("",)