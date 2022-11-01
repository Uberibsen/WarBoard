import math

class FilterResponse:
    """Filtering API response"""
    def town_distance(x1, x2, y1, y2):
        """Calculates the distance between towns in static and dynamic API response"""
        return math.sqrt(abs(x1 - y1) ** 2 + abs(x2 - y2) ** 2)

    def captured_towns(static, dynamic, warreport):
        """Returns filtered API response and converted coordinates for town identification"""
        filtered_towns = {"timestamp": dynamic['lastUpdated'], "casualties": {}, "towns": {}}
        icons = [45, 46, 47, 56, 57, 58] # Town halls and relics

        # Add total faction casualties in hex 
        filtered_towns['casualties']['colonial'] = warreport['colonialCasualties']
        filtered_towns['casualties']['warden'] = warreport['wardenCasualties']

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
                filtered_towns["towns"][town] = faction_captured[lowest_index]
        return filtered_towns