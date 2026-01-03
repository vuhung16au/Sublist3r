#!/usr/bin/env python3
# coding: utf-8
"""
AlienVault OTX enumeration module.
"""

import json
from engines.base import enumratorBaseThreaded, console
import ui_styles


class AlienVaultOTXEnum(enumratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        base_url = 'https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns'
        self.engine_name = "AlienVault OTX"
        self.q = q
        super(AlienVaultOTXEnum, self).__init__(base_url, self.engine_name, domain, subdomains, q=q, silent=silent, verbose=verbose)
        return

    def req(self, url):
        try:
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)
        except Exception as e:
            resp = None

        return self.get_response(resp)

    def enumerate(self):
        url = self.base_url.format(domain=self.domain)
        resp = self.req(url)
        if not resp:
            return self.subdomains

        self.extract_domains(resp)
        return self.subdomains

    def extract_domains(self, resp):
        try:
            data = json.loads(resp)
            # OTX passive_dns response structure
            if 'passive_dns' in data:
                for record in data['passive_dns']:
                    if 'hostname' in record:
                        subdomain = record['hostname'].strip()
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

