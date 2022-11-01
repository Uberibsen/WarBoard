from src.format import FilterResponse
from src.request import API
import constants.constants as constant
import json

api_response_warreport = API.get_hex_info(constant.BASE_API_URL, constant.WARREPORT_MODIFIER)
api_response_static = API.get_hex_info(constant.BASE_API_URL, constant.STATIC_MODIFIER)
api_response_dynamic = API.get_hex_info(constant.BASE_API_URL, constant.DYNAMIC_MODIFIER)

# Filter API response
json_object = json.dumps(FilterResponse.captured_towns(
    api_response_static,
    api_response_dynamic,
    api_response_warreport),
    indent = 4)

API.write_json(json_object)