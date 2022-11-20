import math

class FilterResponse:
    """Filtering API response"""
    def town_distance(x1, x2, y1, y2):
        """Calculates the distance between towns in static and dynamic API response"""
        return math.sqrt(abs(x1 - y1) ** 2 + abs(x2 - y2) ** 2)

    def captured_towns(static, dynamic):
        """Returns filtered API response and converted coordinates for town identification"""
        captured_towns = {}
        icons = [45, 46, 47, 56, 57, 58] # Town halls and relics

        # Takes x and y coordinates from both API responses, calculates nearest and assigns faction
        for static_item in static['mapTextItems']:
            deltas = []
            faction_captured = []
            if static_item['mapMarkerType'] == 'Major':
                town = static_item['text']
                x1 = static_item['x']
                y1 = static_item['y']
                for dynamic_item in dynamic['mapItems']:
                    if dynamic_item['iconType'] in icons:
                        x2 = dynamic_item['x']
                        y2 = dynamic_item['y']
                        faction_captured.append(dynamic_item['teamId'])
                        deltas.append(FilterResponse.town_distance(x1, y1, x2, y2))
                lowest_index = deltas.index(min(deltas))
                captured_towns[town] = faction_captured[lowest_index]
        return captured_towns

    def casuality_rate(warreport):
        """Returns the casuality rate pr. hour for each faction"""
        casuality_rate = {}
        try:
            casuality_rate['colonial'] = warreport['colonialCasualties'] - cas_rate_storage[0]
            casuality_rate['warden'] = warreport['wardenCasualties'] - cas_rate_storage[1]
        except UnboundLocalError:
            casuality_rate['colonial'] = 0
            casuality_rate['warden'] = 0
        cas_rate_storage = [warreport['colonialCasualties'], warreport['wardenCasualties']]

        return casuality_rate

    def complete_response(static, dynamic, warreport):
        """Returns the complete filtered API response for LED usage"""
        complete_response = {"timestamp": dynamic['lastUpdated'], "casuality_rate": {}, "towns": {}}
        complete_response['casuality_rate'] = FilterResponse.casuality_rate(warreport)
        complete_response['towns'] = FilterResponse.captured_towns(static, dynamic)
        return complete_response