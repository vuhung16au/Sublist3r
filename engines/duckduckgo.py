#!/usr/bin/env python3
# coding: utf-8
"""
DuckDuckGo search engine enumeration module.
"""

import re
import time
import urllib.parse as urlparse
from engines.base import enumratorBaseThreaded, console
import ui_styles


class DuckDuckGoEnum(enumratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        base_url = 'https://html.duckduckgo.com/html/?q={query}'
        self.engine_name = "DuckDuckGo"
        self.MAX_DOMAINS = 11
        self.MAX_PAGES = 0
        super(DuckDuckGoEnum, self).__init__(base_url, self.engine_name, domain, subdomains, q=q, silent=silent, verbose=verbose)
        self.q = q
        return

    def extract_domains(self, resp):
        links_list = list()
        # DuckDuckGo HTML result patterns
        link_regx = re.compile(r'<a class="result__a".*?href="(.*?)"')
        link_regx2 = re.compile(r'<a class="result__url".*?href="(.*?)"')
        try:
            links = link_regx.findall(resp)
            links2 = link_regx2.findall(resp)
            links_list = links + links2

            for link in links_list:
                link = re.sub(r'&amp;', '&', link)  # Decode HTML entities
                if not link.startswith('http'):
                    link = "http://" + link
                subdomain = urlparse.urlparse(link).netloc
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

    def check_response_errors(self, resp):
        # DuckDuckGo doesn't typically block, but check for error pages
        if isinstance(resp, str) and ('error' in resp.lower() or 'blocked' in resp.lower()):
            return False
        return True

    def should_sleep(self):
        # DuckDuckGo is less aggressive, shorter sleep
        time.sleep(2)
        return

    def generate_query(self):
        if self.subdomains:
            fmt = 'site:{domain} -www.{domain} -{found}'
            found = ' -'.join(self.subdomains[:self.MAX_DOMAINS - 2])
            query = fmt.format(domain=self.domain, found=found)
        else:
            query = "site:{domain} -www.{domain}".format(domain=self.domain)
        return query

