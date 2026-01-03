#!/usr/bin/env python3
# coding: utf-8
"""
ThreatCrowd enumeration module.
"""

import json
from engines.base import enumratorBaseThreaded, console
import ui_styles


class ThreatCrowd(enumratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        base_url = 'https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}'
        self.engine_name = "ThreatCrowd"
        self.q = q
        super(ThreatCrowd, self).__init__(base_url, self.engine_name, domain, subdomains, q=q, silent=silent, verbose=verbose)
        return

    def req(self, url):
        try:
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)
        except Exception:
            resp = None

        return self.get_response(resp)

    def enumerate(self):
        url = self.base_url.format(domain=self.domain)
        resp = self.req(url)
        self.extract_domains(resp)
        return self.subdomains

    def extract_domains(self, resp):
        try:
            links = json.loads(resp)['subdomains']
            for link in links:
                subdomain = link.strip()
                if not subdomain.endswith(self.domain):
                    continue
                if subdomain not in self.subdomains and subdomain != self.domain:
                    if self.verbose:
                        if console:
                            self.print_(f"[{ui_styles.UIStyles.SOURCE}]{self.engine_name}[/{ui_styles.UIStyles.SOURCE}]: [{ui_styles.UIStyles.SUBDOMAIN}]{subdomain}[/{ui_styles.UIStyles.SUBDOMAIN}]")
                        else:
                            self.print_(f"{self.engine_name}: {subdomain}")
                    self.subdomains.append(subdomain.strip())
        except Exception as e:
            pass

