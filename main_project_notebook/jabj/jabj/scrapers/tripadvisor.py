import re
import json
from operator import itemgetter
from collections import defaultdict
from castus.collections import pathget
from castus.decorator import linescanner

# This was the last function before tripadvisor was cancelled
@linescanner
def travel_board_to_forum_list(html):
    return []

@linescanner
def user_travel_map_to_geolocs(html):
    """Scrape html for a dict of columns city_id, contributions, url """

    pat = re.compile(r'^data = (.*);$')

    raw_json_data = None

    for l in html:
        m = pat.match(l)
        if m:
            raw_json_data = m.group(1)

    if raw_json_data is None:
        return None

    jd = json.loads(raw_json_data)

    # Get a list of the cities that the member has contributed to
    path = ["store", "modules.membercenter.collection.CityTiles",
            "memberId:CfpsrmcpPug=,sortOrderId:1", "items"]

    city_ids = map(itemgetter("$i"), pathget(jd, path, []))

    # Each city_id has an entry in the CityTile
    """
        "store": {
            [...]
            "modules.membercenter.collection.CityTiles": {

            "modules.membercenter.entity.CityTile": {
                "28982": {
                    "attractions": [],
                    "contributions": 2,
                    "hasCityPage": true,
                    "loc": {
                        "$i": "28982",
                        "$t": "modules.unimplemented.entity.JSONLocation"
                    },
                    "member": {
                        "$i": "CfpsrmcpPug=",
                        "$t": "modules.unimplemented.entity.Member"
                    },
                    "pin": {
                        "$i": "CfpsrmcpPug=-28982",
                        "$t": "modules.travelmap.entity.Pin"
                    },
                    "url": "/members-citypage/gatdaddy3/g28982"
                },
                [...]
    """

    result = defaultdict(list)

    for city_id in city_ids:
        path = ["store", "modules.membercenter.entity.CityTile",
                city_id]
        node = pathget(jd, path)

        if node:
            result['city_id'].append(city_id)
            for k in ['contributions', 'url']:
                result[k].append(node[k])

        path = ["store", "modules.unimplemented.entity.JSONLocation",
                city_id]
        node = pathget(jd, path)

        if node:
            for k in ['city', 'lat', 'lng', 'name', 'url']:
                result[k].append(node[k])


    # import pprint
    # pp = pprint.PrettyPrinter(indent=4)

    # pp.pprint(result)

    return result
