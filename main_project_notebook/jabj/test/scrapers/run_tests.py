import re
import importlib
import os
import os.path
import sys
import jabj.scrapers.tripadvisor as ta
import jabj.scrapers.travelblog as tb


num_tests = -1

currpath = '.'
for f in os.listdir(currpath):
    if os.path.isfile(os.path.join(currpath,f)):
        if re.match('^\d\d\d\d$', f):
            if int(f) + 1 > num_tests:
                num_tests = int(f) + 1

scraper = [0] * num_tests
exp = [0] * num_tests

# List of tests to skip
skips = set([1, 2])

# The actual tests
scraper[0] = ta.user_travel_map_to_geolocs
exp[0] = {'city':
               [u'Gatlinburg', u'Oxford', u'Guntersville', u'Pigeon Forge',
                u'Alexander City', u'Anniston', u'Birmingham', u'Madison',
                u'Albertville', u'Franklin', u'Helen', u'Tuscaloosa'],
               'name':
               [u'Gatlinburg', u'Oxford', u'Guntersville', u'Pigeon Forge',
                u'Alexander City', u'Anniston', u'Birmingham', u'Madison',
                u'Albertville', u'Franklin', u'Helen', u'Tuscaloosa'],
               'city_id':
               [u'60842', u'30756', u'30584', u'55270', u'28983', u'28995',
                u'30375', u'30677', u'28982', u'39427', u'35004', u'30889'],
               'url':
               [u'/members-citypage/gatdaddy3/g60842',
                u'/Tourism-g60842-Gatlinburg_Tennessee-Vacations.html',
                u'/members-citypage/gatdaddy3/g30756',
                u'/Tourism-g30756-Oxford_Alabama-Vacations.html',
                u'/members-citypage/gatdaddy3/g30584',
                u'/Tourism-g30584-Guntersville_Alabama-Vacations.html',
                u'/members-citypage/gatdaddy3/g55270',
                u'/Tourism-g55270-Pigeon_Forge_Tennessee-Vacations.html',
                u'/members-citypage/gatdaddy3/g28983',
                u'/Tourism-g28983-Alexander_City_Alabama-Vacations.html',
                u'/members-citypage/gatdaddy3/g28995',
                u'/Tourism-g28995-Anniston_Alabama-Vacations.html',
                u'/members-citypage/gatdaddy3/g30375',
                u'/Tourism-g30375-Birmingham_Alabama-Vacations.html',
                u'/members-citypage/gatdaddy3/g30677',
                u'/Tourism-g30677-Madison_Alabama-Vacations.html',
                u'/members-citypage/gatdaddy3/g28982',
                u'/Tourism-g28982-Albertville_Alabama-Vacations.html',
                u'/members-citypage/gatdaddy3/g39427',
                u'/Tourism-g39427-Franklin_Kentucky-Vacations.html',
                u'/members-citypage/gatdaddy3/g35004',
                u'/Tourism-g35004-Helen_Georgia-Vacations.html',
                u'/members-citypage/gatdaddy3/g30889',
                u'/Tourism-g30889-Tuscaloosa_Alabama-Vacations.html'],
               'lat':
               [35.714596, 33.614628, 34.36307, 35.789257, 32.94466, 33.738,
                33.522934, 34.693253, 34.266094, 36.717213, 34.70015,
                33.21032],
               'lng':
               [-83.511215, -85.8339, -86.35284, -83.553986, -85.95328,
                -85.81808,
                -86.812584, -86.74844, -86.20611, -86.58314, -83.76309,
                -87.56662],
               'contributions': [353, 15, 11, 9, 5, 5, 3, 3, 2, 2, 2, 2]}

scraper[2] = tb.bloggers_prefix_to_bloggers

scraper[3] = tb.blogger_map_to_coords

exp[3] = {'latitude': [37.7186, 32.2192, 33.8136, 28.7503, 30.1586, 32.7503,
                       37.7186, 37.7186, 35.5006, 37.7186, 35.7503, 28.7503,
                       28.7503, 28.7503, 32.7503, 37.7186, 37.7186, 37.7186,
                       37.7186, 30.1922, 28.7503, 28.7503, 37.7186, 37.7186,
                       28.7503, 32.7503, 39.096, 37.7186, 37.7186, 32.7503,
                       28.7503, 37.7186, 38.8739, 32.7503, 32.7503, 32.7503,
                       28.7503, 32.7503, 32.7503, 34.1747, 28.7503, 29.2106,
                       28.7503, 37.7186, 39.4561, 39.9267, 39.7294, 28.7503,
                       32.335, 39.4561, 38.1944, 43.6575, 43.6669, 44.4668,
                       38.4731, 32.3175, 28.7503, 35.2019, 39.7294, 39.7294,
                       28.7503, 28.7503, 28.7503, 39.4561, 39.4561, 40.2503,
                       43.9442, 30.1531, 28.7503, 27.0994, 28.7503, 38.8339,
                       40.8138, 42.5603, 42.5603, 32.1531, 36.0556, 33.5386,
                       32.2217],
          'longitude': [-77.3438, -80.6706, -85.7614, -82.5003, -85.6603,
                        -86.7503, -77.3438, -77.3438, -80.0006, -77.3438,
                        -86.2503, -82.5003, -82.5003, -82.5003, -83.5003,
                        -77.3438, -77.3438, -77.3438, -77.3438, -82.6147,
                        -82.5003, -82.5003, -77.3438, -77.3438, -82.5003,
                        -86.7503, -102.305, -77.3438, -77.3438, -86.7503,
                        -82.5003, -77.3438, -77.0581, -86.7503, -86.7503,
                        -86.7503, -82.5003, -86.7503, -86.7503, -86.8436,
                        -82.5003, -81.0231, -82.5003, -77.3438, -77.9642,
                        -86.6289, -104.831, -82.5003, -80.6925, -77.9642,
                        -95.7425, -71.5008, -71.5003, -68.278, -77.9969,
                        -89.0256, -82.5003, -92.4558, -104.831, -104.831,
                        -82.5003, -82.5003, -82.5003, -77.9642, -77.9642,
                        -83.0003, -90.8128, -85.6114, -82.5003, -82.4544,
                        -82.5003, -104.821, -81.1011, -90.7756, -90.7756,
                        -94.7992, -112.139, -112.185, -110.926],
          'blog_number': [264512, 271043, 271496, 272945, 274148, 274899,
                          275621, 277621, 326071, 392200, 394346, 395242,
                          395931, 397188, 397718, 405545, 405559, 412940,
                          432394, 436270, 469779, 471007, 484382, 491012,
                          494942, 495182, 500005, 528658, 574100, 582245,
                          582810, 590049, 591086, 606400, 611179, 617857,
                          622770, 629351, 649619, 654517, 655969, 657234,
                          657724, 660648, 663239, 663291, 664888, 694006,
                          696931, 724071, 724284, 724458, 724796, 724800,
                          727697, 737959, 739929, 749839, 751277, 752845,
                          756061, 756844, 776137, 783518, 784868, 787484,
                          788114, 791557, 803042, 803436, 804641, 808218,
                          809194, 810236, 810522, 811114, 813290, 813433,
                          814203]
}

for i in xrange(num_tests):
    if i in skips:
        continue
    test_numstr = '{0:04d}'.format(i)
    with open(test_numstr) as fh:
        data = fh.read()
    sys.stdout.write("testing {}...".format(test_numstr))
    result = scraper[i](data)
    expected = exp[i]
    if result != expected:
        print "NOT OK"
        print "expected {}, got {}".format(expected, result)
    else:
        print "OK"

