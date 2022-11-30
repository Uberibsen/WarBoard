from src.format import FilterResponse
from src.request import API
from src.led import WS2812
import constants.constants as constant
import json, time

casualty_rate_wardens = []
casualty_rate_colonials = []
count = 0

while True:
    try: 
        data_option = int(input("Enter 1 for live data. Enter 2 for example data: "))
        if data_option == 1 or 2:
            print("WarBoard: Initiating")
            break
        else:
            raise ValueError
    except ValueError:
        print("Please enter a valid number.")
        continue

if data_option == 1:
    while True:
        api_response_warreport = API.get_hex_info(constant.BASE_API_URL, constant.WARREPORT_MODIFIER)
        api_response_static = API.get_hex_info(constant.BASE_API_URL, constant.STATIC_MODIFIER)
        api_response_dynamic = API.get_hex_info(constant.BASE_API_URL, constant.DYNAMIC_MODIFIER)
        print("WarBoard: API fetch successful")
        
        # Filter API response
        json_object = json.dumps(FilterResponse.complete_response(
            api_response_static,
            api_response_dynamic,
            api_response_warreport,
            count,
            casualty_rate_wardens,
            casualty_rate_colonials),
            indent = 4)

        count = count + 1
        if count > 5:
            count = 0

        API.write_json(json_object)
        with open("data/data.json", "r") as filtered_data:
            WS2812.write_led_colors(json.load(filtered_data))
            print(f"WarBoard: Showing live data...\nWarBoard: Next fetch in 10 minutes")
        time.sleep(600) # 600 seconds by default (10 minutes)
        print("WarBoard: 10 minutes elapsed. Fetching new data...")

if data_option == 2:
    print("WarBoard: Running example data")
    while True:
        with open("example/example.json", "r") as example_data:
            WS2812.write_led_colors(json.load(example_data))
            break