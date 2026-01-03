#!/usr/bin/env python3
# coding: utf-8
"""
Yahoo search engine enumeration module.
"""

import re
import urllib.parse as urlparse
from engines.base import enumratorBaseThreaded, console
import ui_styles


class YahooEnum(enumratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        base_url = "https://search.yahoo.com/search?p={query}&b={page_no}"
        self.engine_name = "Yahoo"
        self.MAX_DOMAINS = 10
        self.MAX_PAGES = 0
        super(YahooEnum, self).__init__(base_url, self.engine_name, domain, subdomains, q=q, silent=silent, verbose=verbose)
        self.q = q
        return

    def extract_domains(self, resp):
        link_regx2 = re.compile('<span class=" fz-.*? fw-m fc-12th wr-bw.*?">(.*?)</span>')
        link_regx = re.compile('<span class="txt"><span class=" cite fw-xl fz-15px">(.*?)</span>')
        links_list = []
        try:
            links = link_regx.findall(resp)
            links2 = link_regx2.findall(resp)
            links_list = links + links2
            for link in links_list:
                link = re.sub(r"<(/?)?b>", "", link)
                if not link.startswith('http'):
                    link = "http://" + link
                subdomain = urlparse.urlparse(link).netloc
                if not subdomain.endswith(self.domain):
                    continue
                if subdomain and subdomain not in self.subdomains and subdomain != self.domain:
                    if self.verbose:
                        if console:
                            self.print_(f"[{ui_styles.UIStyles.SOURCE}]{self.engine_name}[/{ui_styles.UIStyles.SOURCE}]: [{ui_styles.UIStyles.SUBDOMAIN}]{subdomain}[/{ui_styles.UIStyles.SUBDOMAIN}]")
                        else:
                            self.print_(f"{self.engine_name}: {subdomain}")
                    self.subdomains.append(subdomain.strip())
        except Exception:
            pass

        return links_list

    def should_sleep(self):
        return

    def get_page(self, num):
        return num + 10

    def generate_query(self):
        if self.subdomains:
            fmt = 'site:{domain} -domain:www.{domain} -domain:{found}'
            found = ' -domain:'.join(self.subdomains[:77])
            query = fmt.format(domain=self.domain, found=found)
        else:
            query = "site:{domain}".format(domain=self.domain)
        return query

