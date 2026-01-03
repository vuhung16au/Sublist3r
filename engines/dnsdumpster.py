#!/usr/bin/env python3
# coding: utf-8
"""
DNSdumpster enumeration module.
"""

import re
import threading
import dns.resolver
from engines.base import enumratorBaseThreaded, console
import ui_styles


class DNSdumpster(enumratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        base_url = 'https://dnsdumpster.com/'
        self.live_subdomains = []
        self.engine_name = "DNSdumpster"
        self.q = q
        self.lock = None
        super(DNSdumpster, self).__init__(base_url, self.engine_name, domain, subdomains, q=q, silent=silent, verbose=verbose)
        return

    def check_host(self, host):
        is_valid = False
        Resolver = dns.resolver.Resolver()
        Resolver.nameservers = ['8.8.8.8', '8.8.4.4']
        self.lock.acquire()
        try:
            ip = Resolver.resolve(host, 'A')[0].to_text()
            if ip:
                if self.verbose:
                    if console:
                        self.print_(f"[{ui_styles.UIStyles.SOURCE}]{self.engine_name}[/{ui_styles.UIStyles.SOURCE}]: [{ui_styles.UIStyles.SUBDOMAIN}]{host}[/{ui_styles.UIStyles.SUBDOMAIN}]")
                    else:
                        self.print_(f"{self.engine_name}: {host}")
                is_valid = True
                self.live_subdomains.append(host)
        except:
            pass
        self.lock.release()
        return is_valid

    def req(self, req_method, url, params=None):
        params = params or {}
        headers = dict(self.headers)
        headers['Referer'] = 'https://dnsdumpster.com'
        try:
            if req_method == 'GET':
                resp = self.session.get(url, headers=headers, timeout=self.timeout)
            else:
                resp = self.session.post(url, data=params, headers=headers, timeout=self.timeout)
        except Exception as e:
            self.print_(e)
            resp = None
        return self.get_response(resp)

    def get_csrftoken(self, resp):
        csrf_regex = re.compile(r'<input type="hidden" name="csrfmiddlewaretoken" value="(.*?)">', re.S)
        tokens = csrf_regex.findall(resp)
        if not tokens:
            return None
        token = tokens[0]
        return token.strip()

    def enumerate(self):
        self.lock = threading.BoundedSemaphore(value=70)
        resp = self.req('GET', self.base_url)
        token = self.get_csrftoken(resp)
        if token is None:
            if self.verbose:
                if console:
                    self.print_(f"[{ui_styles.UIStyles.ERROR}][!] Error:[/{ui_styles.UIStyles.ERROR}] Could not retrieve CSRF token from DNSdumpster")
                else:
                    self.print_("[!] Error: Could not retrieve CSRF token from DNSdumpster")
            return self.live_subdomains
        params = {'csrfmiddlewaretoken': token, 'targetip': self.domain}
        post_resp = self.req('POST', self.base_url, params)
        self.extract_domains(post_resp)
        for subdomain in self.subdomains:
            t = threading.Thread(target=self.check_host, args=(subdomain,))
            t.start()
            t.join()
        return self.live_subdomains

    def extract_domains(self, resp):
        tbl_regex = re.compile(r'<a name="hostanchor"></a>Host Records.*?<table.*?>(.*?)</table>', re.S)
        link_regex = re.compile('<td class="col-md-4">(.*?)<br>', re.S)
        links = []
        try:
            results_tbl = tbl_regex.findall(resp)[0]
        except IndexError:
            results_tbl = ''
        links_list = link_regex.findall(results_tbl)
        links = list(set(links_list))
        for link in links:
            subdomain = link.strip()
            if not subdomain.endswith(self.domain):
                continue
            if subdomain and subdomain not in self.subdomains and subdomain != self.domain:
                self.subdomains.append(subdomain.strip())
        return links

