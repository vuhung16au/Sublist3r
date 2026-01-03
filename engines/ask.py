#!/usr/bin/env python3
# coding: utf-8
"""
Ask search engine enumeration module.
"""

import re
import urllib.parse as urlparse
from engines.base import enumratorBaseThreaded, console
import ui_styles


class AskEnum(enumratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        base_url = 'http://www.ask.com/web?q={query}&page={page_no}&qid=8D6EE6BF52E0C04527E51F64F22C4534&o=0&l=dir&qsrc=998&qo=pagination'
        self.engine_name = "Ask"
        self.MAX_DOMAINS = 11
        self.MAX_PAGES = 0
        enumratorBaseThreaded.__init__(self, base_url, self.engine_name, domain, subdomains, q=q, silent=silent, verbose=verbose)
        self.q = q
        return

    def extract_domains(self, resp):
        links_list = list()
        link_regx = re.compile('<p class="web-result-url">(.*?)</p>')
        try:
            links_list = link_regx.findall(resp)
            for link in links_list:
                if not link.startswith('http'):
                    link = "http://" + link
                subdomain = urlparse.urlparse(link).netloc
                if subdomain not in self.subdomains and subdomain != self.domain:
                    if self.verbose:
                        if console:
                            self.print_(f"[{ui_styles.UIStyles.SOURCE}]{self.engine_name}[/{ui_styles.UIStyles.SOURCE}]: [{ui_styles.UIStyles.SUBDOMAIN}]{subdomain}[/{ui_styles.UIStyles.SUBDOMAIN}]")
                        else:
                            self.print_(f"{self.engine_name}: {subdomain}")
                    self.subdomains.append(subdomain.strip())
        except Exception:
            pass

        return links_list

    def get_page(self, num):
        return num + 1

    def generate_query(self):
        if self.subdomains:
            fmt = 'site:{domain} -www.{domain} -{found}'
            found = ' -'.join(self.subdomains[:self.MAX_DOMAINS])
            query = fmt.format(domain=self.domain, found=found)
        else:
            query = "site:{domain} -www.{domain}".format(domain=self.domain)

        return query

