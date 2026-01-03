# Agent Policies

## Python Version Compatibility

- The project should run without errors (and warnings) with Python 3.12+ (3.12, 3.13)
- This project requires Python 3.12 or higher. Python 2.x and Python 3.x < 3.12 are no longer supported.

## Adding New Engines

When adding new enumeration engines, please follow the current engine structure to maintain consistency and ensure proper integration with the configuration system.

### Engine Structure Pattern

All engines must inherit from `enumratorBaseThreaded` (or `enumratorBase` for non-threaded engines) located in `engines/base.py`.

### Step-by-Step Guide

1. **Create a new engine file** in the `engines/` directory:
   - File name should be lowercase with underscores (e.g., `new_engine.py`)
   - Import the base class: `from engines.base import enumratorBaseThreaded`
   - Import necessary modules: `import ui_styles`, `from engines.base import console`

2. **Define the engine class** following this template:

```python
#!/usr/bin/env python3
# coding: utf-8
"""
Description of the engine.
"""

import re
import urllib.parse as urlparse
from engines.base import enumratorBaseThreaded, console
import ui_styles


class NewEngineEnum(enumratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        subdomains = subdomains or []
        base_url = 'https://example.com/search?q={query}&page={page_no}'
        self.engine_name = "NewEngine"
        self.MAX_DOMAINS = 10  # Optional: limit subdomains in query
        self.MAX_PAGES = 0     # Optional: limit pages to avoid blocking
        super(NewEngineEnum, self).__init__(
            base_url, self.engine_name, domain, subdomains, 
            q=q, silent=silent, verbose=verbose
        )
        self.q = q
        return

    def extract_domains(self, resp):
        """Extract subdomains from the response.
        
        This method is REQUIRED and must be implemented.
        """
        links_list = []
        # Your extraction logic here
        # Use regex or parsing to find subdomains in resp
        # Add found subdomains to self.subdomains list
        return links_list

    def generate_query(self):
        """Generate the search query.
        
        This method is REQUIRED and must be implemented.
        """
        if self.subdomains:
            # Query excluding already found subdomains
            fmt = 'site:{domain} -www.{domain} -{found}'
            found = ' -'.join(self.subdomains[:self.MAX_DOMAINS])
            query = fmt.format(domain=self.domain, found=found)
        else:
            query = "site:{domain} -www.{domain}".format(domain=self.domain)
        return query

    # Optional methods (override if needed):
    
    def check_response_errors(self, resp):
        """Check for errors in the response.
        
        Return True if no errors, False otherwise.
        """
        # Check for blocking messages, CAPTCHAs, etc.
        return True

    def should_sleep(self):
        """Sleep to avoid rate limiting."""
        import time
        time.sleep(2)  # Adjust as needed
        return

    def get_page(self, num):
        """Get the next page number for pagination."""
        return num + 10  # Adjust based on engine's pagination
```

3. **Register the engine** in `engines/__init__.py`:
   - Import your engine class at the top
   - Add it to `ENGINE_REGISTRY` dictionary with a lowercase key
   - Add it to `ALL_ENGINES` list

```python
from engines.new_engine import NewEngineEnum

ENGINE_REGISTRY = {
    # ... existing engines ...
    'newengine': NewEngineEnum,
}

ALL_ENGINES = [
    # ... existing engines ...
    NewEngineEnum,
]
```

4. **Add the engine to configuration** in `config/engines.yaml`:

```yaml
engines:
  # ... existing engines ...
  newengine:
    enabled: true
```

### Required Methods

- `extract_domains(resp)`: Extract subdomains from the HTTP response
- `generate_query()`: Generate the search query string

### Optional Methods (Override as Needed)

- `check_response_errors(resp)`: Check if the response indicates blocking/errors
- `should_sleep()`: Add delays to avoid rate limiting
- `get_page(num)`: Customize pagination logic
- `enumerate()`: Override the entire enumeration logic if needed (advanced)

### Best Practices

1. **Follow naming conventions**: Use descriptive class names ending with `Enum` (e.g., `GoogleEnum`, `YahooEnum`)
2. **Handle errors gracefully**: Use try/except blocks in `extract_domains` to avoid crashes
3. **Respect rate limits**: Implement `should_sleep()` with appropriate delays
4. **Use consistent output**: Use the `console` and `ui_styles` for consistent output formatting
5. **Test thoroughly**: Test the engine with various domains before submitting
6. **Document clearly**: Add comments explaining any non-obvious logic

### Example: Complete Engine Implementation

See existing engines in the `engines/` directory for reference:
- `engines/google.py` - Search engine with pagination and error checking
- `engines/virustotal.py` - API-based engine with JSON parsing
- `engines/netcraft.py` - Engine with custom enumeration logic

### Testing Your Engine

1. Test with a known domain: `python sublist3r.py -e newengine -d example.com -v`
2. Verify it appears in the engine list
3. Check that it respects the configuration file settings
4. Ensure error handling works correctly

