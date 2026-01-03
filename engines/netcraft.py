#!/usr/bin/env python3
# coding: utf-8
"""
Netcraft enumeration module.
"""

import re
import time
import random
import hashlib
import urllib.parse as urlparse
from engines.base import enumratorBaseThreaded, console
import ui_styles


class NetcraftEnum(enumratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        self.base_url = 'https://searchdns.netcraft.com/?restriction=site+ends+with&host={domain}'
        self.engine_name = "Netcraft"
        super(NetcraftEnum, self).__init__(self.base_url, self.engine_name, domain, subdomains, q=q, silent=silent, verbose=verbose)
        self.q = q
        return

    def req(self, url, cookies=None):
        cookies = cookies or {}
        try:
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout, cookies=cookies)
        except Exception as e:
            self.print_(e)
            resp = None
        return resp

    def should_sleep(self):
        time.sleep(random.randint(1, 2))
        return

    def get_next(self, resp):
        link_regx = re.compile('<a.*?href="(.*?)">Next Page')
        link = link_regx.findall(resp)
        url = 'http://searchdns.netcraft.com' + link[0]
        return url

    def create_cookies(self, cookie):
        cookies = dict()
        cookies_list = cookie[0:cookie.find(';')].split("=")
        cookies[cookies_list[0]] = cookies_list[1]
        # hashlib.sha1 requires utf-8 encoded str
        cookies['netcraft_js_verification_response'] = hashlib.sha1(urlparse.unquote(cookies_list[1]).encode('utf-8')).hexdigest()
        return cookies

    def get_cookies(self, headers):
        if 'set-cookie' in headers:
            cookies = self.create_cookies(headers['set-cookie'])
        else:
            cookies = {}
        return cookies

    def enumerate(self):
        start_url = self.base_url.format(domain='example.com')
        resp = self.req(start_url)
        cookies = self.get_cookies(resp.headers)
        url = self.base_url.format(domain=self.domain)
        while True:
            resp = self.get_response(self.req(url, cookies))
            self.extract_domains(resp)
            if 'Next Page' not in resp:
                return self.subdomains
                break
            url = self.get_next(resp)
            self.should_sleep()

    def extract_domains(self, resp):
        links_list = list()
        link_regx = re.compile('<a class="results-table__host" href="(.*?)"')
        try:
            links_list = link_regx.findall(resp)
            for link in links_list:
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

