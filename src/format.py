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

    def calculate_casualty_rate(count, cas, cas_list):
        """Appends each sum of casualties for pr. hour calculation"""
        if len(cas_list) > 6:
            deaths_per_hour = cas_list[count] = cas
            deaths_per_hour = (cas - cas_list[count + 1])       
        else:
            cas_list.append(cas)
            deaths_per_hour = cas_list[count] - cas_list[0]
        return deaths_per_hour

    def casualty_rate(warreport, count, casualties_w, casualties_c):
        """Returns the casualty rate pr. hour for each faction"""
        casualty_rate = {}
        casualty_rate['colonials'] = FilterResponse.calculate_casualty_rate(count, warreport['colonialCasualties'], casualties_c)
        casualty_rate['wardens'] = FilterResponse.calculate_casualty_rate(count, warreport['wardenCasualties'], casualties_w)
        return casualty_rate

    def complete_response(static, dynamic, warreport, count, casualties_w, casualties_c):
        """Returns the complete filtered API response for LED usage"""
        complete_response = {"timestamp": dynamic['lastUpdated'], "casualty_rate": {}, "towns": {}}
        complete_response['casualty_rate'] = FilterResponse.casualty_rate(warreport, count, casualties_w, casualties_c)
        complete_response['towns'] = FilterResponse.captured_towns(static, dynamic)
        return complete_response