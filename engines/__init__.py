#!/usr/bin/env python3
# coding: utf-8
"""
Engine registry and exports for all enumeration engines.
"""

from engines.google import GoogleEnum
from engines.yahoo import YahooEnum
from engines.bing import BingEnum
from engines.baidu import BaiduEnum
from engines.ask import AskEnum
from engines.netcraft import NetcraftEnum
from engines.dnsdumpster import DNSdumpster
from engines.virustotal import Virustotal
from engines.threatcrowd import ThreatCrowd
from engines.crt_search import CrtSearch
from engines.passivedns import PassiveDNS
from engines.duckduckgo import DuckDuckGoEnum
from engines.alienvault_otx import AlienVaultOTXEnum
from engines.base import set_console

# Engine registry mapping engine names to classes
ENGINE_REGISTRY = {
    'baidu': BaiduEnum,
    'yahoo': YahooEnum,
    'google': GoogleEnum,
    'bing': BingEnum,
    'ask': AskEnum,
    'netcraft': NetcraftEnum,
    'dnsdumpster': DNSdumpster,
    'virustotal': Virustotal,
    'threatcrowd': ThreatCrowd,
    'ssl': CrtSearch,
    'passivedns': PassiveDNS,
    'duckduckgo': DuckDuckGoEnum,
    'alienvault': AlienVaultOTXEnum,
    'otx': AlienVaultOTXEnum
}

# All engine classes (for default enumeration when no engines specified)
ALL_ENGINES = [
    BaiduEnum,
    YahooEnum,
    GoogleEnum,
    BingEnum,
    AskEnum,
    NetcraftEnum,
    DNSdumpster,
    Virustotal,
    ThreatCrowd,
    CrtSearch,
    PassiveDNS,
    DuckDuckGoEnum,
    AlienVaultOTXEnum
]


def get_enabled_engines(config_data=None):
    """
    Get list of enabled engine classes based on configuration.
    
    Args:
        config_data: Dictionary with engine configuration (from YAML)
                     Format: {'engines': {'engine_name': {'enabled': True/False}}}
    
    Returns:
        List of engine classes that are enabled (unique classes only)
    """
    if config_data is None or 'engines' not in config_data:
        # No config or invalid config - return all engines
        return ALL_ENGINES
    
    enabled_engines = []
    seen_classes = set()  # Track unique engine classes
    engines_config = config_data.get('engines', {})
    
    for engine_name, engine_class in ENGINE_REGISTRY.items():
        engine_config = engines_config.get(engine_name, {})
        # Default to enabled if not specified
        if engine_config.get('enabled', True):
            # Only add if we haven't seen this class before (handles aliases like 'alienvault' and 'otx')
            if engine_class not in seen_classes:
                enabled_engines.append(engine_class)
                seen_classes.add(engine_class)
    
    return enabled_engines if enabled_engines else ALL_ENGINES


__all__ = [
    'GoogleEnum',
    'YahooEnum',
    'BingEnum',
    'BaiduEnum',
    'AskEnum',
    'NetcraftEnum',
    'DNSdumpster',
    'Virustotal',
    'ThreatCrowd',
    'CrtSearch',
    'PassiveDNS',
    'DuckDuckGoEnum',
    'AlienVaultOTXEnum',
    'ENGINE_REGISTRY',
    'ALL_ENGINES',
    'get_enabled_engines',
    'set_console'
]

