import urllib.request, json
from urllib.error import HTTPError, URLError

class API:
    """Class for API calls to the WarAPI"""
    def call(base_api_url, modifier):
        """Calls the WarAPI, returns response"""
        url_request = str(f"{base_api_url}{modifier}")
        try:
            response = urllib.request.urlopen(url_request)
            if (response.getcode() == 200):
                data = response.read()
                hex_response = json.loads(data)
                return hex_response
        except (HTTPError, URLError) as err:
            return False

    def get_hex_info(api, modifier):
        """Get specific hex info from the API call"""
        response = API.call(api, modifier)
        if response:
            return response
        else:
            return False

    def write_json(json_object):
        """Write json data to file"""
        with open("data/data.json", "w") as outfile:
            outfile.write(json_object)