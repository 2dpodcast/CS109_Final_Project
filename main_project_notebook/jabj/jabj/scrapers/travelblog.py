import re
import json
from operator import itemgetter
from collections import defaultdict
from castus.collections import pathget
from castus.decorator import linescanner
from castus.tmpldict import Tmpldict
import jabj.scrapers as scrapers
import pandas as pd

##############################################################################
#
# Templates

url_templates = Tmpldict({
    'blog_map_url': 'http://www.travelblog.org/Bloggers/{}/map.html',
})


##############################################################################
#
# Line scanners (scrapers)

@linescanner
def bloggers_prefix_to_bloggers(html):
    """Converts a bloggers prefix page to blogger ids.

    The bloggers prefix page is what you get when you select for
    example Bloggers->J->Jo.

    An individual blogger has an entry as follows:

    <div class='blogger_mini_pic'>
      <a href='/Bloggers/Jo-and-Barry/'>
      <img style='margin:1px;padding:1px;border:0;margin-right:5px;margin-bottom:5px;'
           src='/pix/portrait-s-0.jpg' alt='Jo and Barry'>
      <br>Jo and Barry<br>(<i>Barry Taylor</i>)
    </a>
    </div>

    """

    # TODO implement if needed
    assert(False)

@linescanner
def blogger_map_to_coords(html):
    p1 = re.compile(r'^var placemarkers = \'(.*)\';$')
    p2 = re.compile(r'^var placedata = \'(.*)\';$')

    cols = {}

    # Normally we use defaultdict for this type of thing, but we will
    # be returning a normal dict, and we want to make sure these items
    # are present.
    for colname in ['latitude', 'longitude', 'blog_number']:
        cols[colname] = []

    markers = None
    data = None

    # Loop until placemarkers and placedata is collected
    for l in html:
        if markers is None:
            markers = p1.match(l)
        elif data is None:
            data = p2.match(l)
        else:
            break

    if not (markers and data):
        return None

    markers, data = map(lambda x: x.group(1), [markers, data])

    markers = eval('[{}]'.format(markers))

    data = re.compile('\),\(').sub('\'),(', data)
    data = re.compile('\)$').sub('\')', data)
    data = re.compile('(\(\d+,)').sub(r"\1'", data)
    data = eval('[{}]'.format(data))

    assert(len(markers) == len(data))

    for i, x in enumerate(data):
        latitude, longitude = markers[i]
        cols['latitude'].append(latitude)
        cols['longitude'].append(longitude)
        cols['blog_number'].append(x[0])

    return cols

##############################################################################
#
# Crawlers.
#
# Crawlers and their utilities operate at a higher level
# architecturally than scrapers.  String processing should be limited
# to cleanup.  Above the crawler level should be higher level data
# manipulation.

def get_blogger_blog_coords(bloggername):
    debug = False

    d = scrapers.scrape_url_tmpl(url_templates, 'blog_map_url',
                                 [bloggername], blogger_map_to_coords,
                                 debug=debug)

    if d is None:
        return d

    d['bloggername'] = [bloggername] * len(d['latitude'])

    ret = pd.DataFrame(d)

    if not ret:
        raise Exception("No dataframe!")

    return ret

