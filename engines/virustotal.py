#!/usr/bin/env python3
# coding: utf-8
"""
Virustotal enumeration module.
"""

import json
from engines.base import enumratorBaseThreaded, console
import ui_styles


class Virustotal(enumratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        base_url = 'https://www.virustotal.com/ui/domains/{domain}/subdomains'
        self.engine_name = "Virustotal"
        self.q = q
        super(Virustotal, self).__init__(base_url, self.engine_name, domain, subdomains, q=q, silent=silent, verbose=verbose)
        self.url = self.base_url.format(domain=self.domain)
        return

    # the main send_req need to be rewritten
    def send_req(self, url):
        try:
            resp = self.session.get(url, headers=self.headers, timeout=self.timeout)
        except Exception as e:
            self.print_(e)
            resp = None

        return self.get_response(resp)

    # once the send_req is rewritten we don't need to call this function, the stock one should be ok
    def enumerate(self):
        while self.url != '':
            resp = self.send_req(self.url)
            resp = json.loads(resp)
            if 'error' in resp:
                if console:
                    self.print_(f"[{ui_styles.UIStyles.ERROR}][!] Error:[/{ui_styles.UIStyles.ERROR}] Virustotal probably now is blocking our requests")
                else:
                    self.print_("[!] Error: Virustotal probably now is blocking our requests")
                break
            if 'links' in resp and 'next' in resp['links']:
                self.url = resp['links']['next']
            else:
                self.url = ''
            self.extract_domains(resp)
        return self.subdomains

    def extract_domains(self, resp):
        #resp is already parsed as json
        try:
            for i in resp['data']:
                if i['type'] == 'domain':
                    subdomain = i['id']
                    if not subdomain.endswith(self.domain):
                        continue
                    if subdomain not in self.subdomains and subdomain != self.domain:
                        if self.verbose:
                            if console:
                                self.print_(f"[{ui_styles.UIStyles.SOURCE}]{self.engine_name}[/{ui_styles.UIStyles.SOURCE}]: [{ui_styles.UIStyles.SUBDOMAIN}]{subdomain}[/{ui_styles.UIStyles.SUBDOMAIN}]")
                            else:
                                self.print_(f"{self.engine_name}: {subdomain}")
                        self.subdomains.append(subdomain.strip())
        except Exception:
            pass

