import requests


##############################################################################
#
# Generic utilities common to all scrapers.

def scrape_url(url, scraper, debug=False):
    """Scrape a given url given a scraper."""
    html = requests.get(url).text.encode('ascii','ignore')

    if debug:
        print url
        print html
    return scraper(html)

def scrape_url_tmpl(tmpldict, tmplname, tmpl_args, scraper, debug=False):
    """Scrape a page.

    This scraper takes an url template dict, name and args,
    and the scraper, and returns the scraping result.
    """

    url = tmpldict.instantiate(tmplname, tmpl_args)

    return scrape_url(url, scraper, debug)

