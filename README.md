## About Sublist3r 

Sublist3r is a python tool designed to enumerate subdomains of websites using OSINT. It helps penetration testers and bug hunters collect and gather subdomains for the domain they are targeting. Sublist3r enumerates subdomains using many search engines such as Google, Yahoo, Bing, Baidu and Ask. Sublist3r also enumerates subdomains using Netcraft, Virustotal, ThreatCrowd, DNSdumpster and ReverseDNS.

[subbrute](https://github.com/TheRook/subbrute) was integrated with Sublist3r to increase the possibility of finding more subdomains using bruteforce with an improved wordlist. The credit goes to TheRook who is the author of subbrute.

## Screenshots

![Sublist3r](http://www.secgeek.net/images/Sublist3r.png "Sublist3r in action")


## Installation

```
git clone https://github.com/vuhung16au/Sublist3r.git
```

## Recommended Python Version:

Sublist3r requires **Python 3.12 or higher**.

## Dependencies:

Sublist3r depends on the `requests`, `dnspython`, `rich`, and `pyyaml` python modules.

These dependencies can be installed using the project's `pyproject.toml`:

- Installation on Windows:
```
python -m pip install -e .
```
- Installation on Linux
```
pip install -e .
```

Or using the Makefile (recommended):
```
make setup-env
```

Alternatively, each module can be installed independently as shown below.

#### Requests Module (http://docs.python-requests.org/en/latest/)

- Install for Windows:
```
python -m pip install requests
```

- Install for Ubuntu/Debian:
```
sudo apt-get install python3-requests
```

- Install for Centos/Redhat:
```
sudo yum install python3-requests
```

- Install using pip on Linux:
```
pip install requests
```

#### dnspython Module (http://www.dnspython.org/)

- Install for Windows:
```
python -m pip install dnspython
```

- Install for Ubuntu/Debian:
```
sudo apt-get install python3-dnspython
```

- Install using pip:
```
pip install dnspython
```

**Note:** `argparse` is included in Python 3.12+ standard library and does not need to be installed separately.

**For coloring in Windows, install the following libraries:**
```
python -m pip install win_unicode_console colorama
```

## Usage

Short Form    | Long Form     | Description
------------- | ------------- |-------------
-d            | --domain      | Domain name to enumerate subdomains of
-b            | --bruteforce  | Enable the subbrute bruteforce module
-p            | --ports       | Scan the found subdomains against specific tcp ports
-v            | --verbose     | Enable the verbose mode and display results in realtime
-t            | --threads     | Number of threads to use for subbrute bruteforce
-e            | --engines     | Specify a comma-separated list of search engines
-o            | --output      | Save the results to text file
-c            | --config      | Path to engine configuration file (YAML format)
-n            | --no-color    | Output without color
-h            | --help        | show the help message and exit

### Examples

* To list all the basic options and switches use -h switch:

```python sublist3r.py -h```

* To enumerate subdomains of specific domain:

``python sublist3r.py -d example.com``

* To enumerate subdomains of specific domain and show only subdomains which have open ports 80 and 443 :

``python sublist3r.py -d example.com -p 80,443``

* To enumerate subdomains of specific domain and show the results in realtime:

``python sublist3r.py -v -d example.com``

* To enumerate subdomains and enable the bruteforce module:

``python sublist3r.py -b -d example.com``

* To enumerate subdomains and use specific engines such Google, Yahoo and Virustotal engines

``python sublist3r.py -e google,yahoo,virustotal -d example.com``

* To use a custom configuration file to enable/disable engines:

``python sublist3r.py -c /path/to/config.yaml -d example.com``

## Engine Configuration

Sublist3r supports configuration files to enable or disable specific enumeration engines. This is useful when certain engines are blocking requests or you want to customize which engines are used by default.

### Configuration File Format

The configuration file uses YAML format and should be located at `config/engines.yaml` (relative to the script) or specified with the `--config` option.

Example `config/engines.yaml`:

```yaml
engines:
  baidu:
    enabled: true
  yahoo:
    enabled: true
  google:
    enabled: false  # Disabled due to blocking
  bing:
    enabled: true
  ask:
    enabled: true
  netcraft:
    enabled: true
  dnsdumpster:
    enabled: true
  virustotal:
    enabled: false  # Disabled due to blocking
  threatcrowd:
    enabled: true
  ssl:
    enabled: true
  passivedns:
    enabled: true
  duckduckgo:
    enabled: true
  alienvault:
    enabled: true
  otx:
    enabled: true
```

### Configuration Priority

1. **CLI argument `-e/--engines`** (highest priority) - If specified, only the listed engines will be used
2. **Config file** (`config/engines.yaml` or custom via `--config`) - Engines marked as `enabled: false` will be excluded
3. **Default** - If no config file exists, all engines are enabled by default

### Available Engine Names

- `baidu`, `yahoo`, `google`, `bing`, `ask` - Search engines
- `netcraft`, `dnsdumpster`, `virustotal`, `threatcrowd` - OSINT sources
- `ssl` - SSL Certificate search (crt.sh)
- `passivedns` - PassiveDNS API
- `duckduckgo` - DuckDuckGo search
- `alienvault`, `otx` - AlienVault OTX (both names refer to the same engine)


## Using Sublist3r as a module in your python scripts

**Example**

```python
import sublist3r 
subdomains = sublist3r.main(domain, no_threads, savefile, ports, silent, verbose, enable_bruteforce, engines)
```
The main function will return a set of unique subdomains found by Sublist3r

**Function Usage:**
* **domain**: The domain you want to enumerate subdomains of.
* **threads**: Number of threads for bruteforce operations.
* **savefile**: save the output into text file.
* **ports**: specify a comma-separated list of the tcp ports to scan.
* **silent**: set sublist3r to work in silent mode during the execution (helpful when you don't need a lot of noise).
* **verbose**: display the found subdomains in real time.
* **enable_bruteforce**: enable the bruteforce module.
* **engines**: (Optional) to choose specific engines (comma-separated string).
* **config_path**: (Optional) path to engine configuration file (YAML format).

Example to enumerate subdomains of Yahoo.com:
```python
import sublist3r 
subdomains = sublist3r.main('yahoo.com', 40, 'yahoo_subdomains.txt', ports= None, silent=False, verbose= False, enable_bruteforce= False, engines=None)
```

## License

Sublist3r is licensed under the GNU GPL license. take a look at the [LICENSE](https://github.com/vuhung16au/Sublist3r/blob/master/LICENSE) for more information.


## Credits

* [TheRook](https://github.com/TheRook) - The bruteforce module was based on his script **subbrute**. 
* [Bitquark](https://github.com/bitquark) - The Subbrute's wordlist was based on his research **dnspop**. 

## Thanks

* Special Thanks to [Ibrahim Mosaad](https://twitter.com/ibrahim_mosaad) for his great contributions that helped in improving the tool.

## Version
**Current version is 1.0**
