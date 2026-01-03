# Sublist3r Quick Start Guide

Sublist3r is a Python tool designed to enumerate subdomains of websites using OSINT (Open Source Intelligence). It helps penetration testers and bug hunters collect and gather subdomains for their target domains.

## What Sublist3r Does

Sublist3r enumerates subdomains using:
- **Search engines**: Google, Yahoo, Bing, Baidu, Ask
- **OSINT sources**: Netcraft, Virustotal, ThreatCrowd, DNSdumpster, ReverseDNS
- **Bruteforce module**: Integrated subbrute for additional subdomain discovery

## Quick Setup

### Prerequisites
- Python 3.12
- Make (for using the Makefile)

### Installation Steps

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/aboul3la/Sublist3r.git
   cd Sublist3r
   ```

2. **Set up the virtual environment and install dependencies**:
   ```bash
   make setup-env
   ```
   This will:
   - Create a virtual environment (`.venv`) with Python 3.12
   - Install all required dependencies from `pyproject.toml`

3. **Activate the virtual environment** (if not already active):
   ```bash
   source .venv/bin/activate
   ```

## Basic Usage

### Simple Subdomain Enumeration

The most basic command to enumerate subdomains:

```bash
python sublist3r.py -d example.com
```

### Verbose Mode (Recommended)

See results in real-time as they are discovered:

```bash
python sublist3r.py -v -d example.com
```

### Save Results to File

Save discovered subdomains to a text file:

```bash
python sublist3r.py -d example.com -o results.txt
```

### Enable Bruteforce Module

Use the integrated bruteforce module to find additional subdomains:

```bash
python sublist3r.py -b -d example.com
```

### Port Scanning

Scan discovered subdomains for specific open ports (e.g., 80, 443):

```bash
python sublist3r.py -d example.com -p 80,443
```

### Use Specific Search Engines

Limit enumeration to specific engines (faster, but may miss results):

```bash
python sublist3r.py -e google,yahoo,virustotal -d example.com
```

Available engines: `google`, `yahoo`, `bing`, `baidu`, `ask`, `netcraft`, `virustotal`, `threatcrowd`, `dnsdumpster`, `ssl`, `passivedns`

### Adjust Thread Count

Control the number of threads for bruteforce operations (default: 30):

```bash
python sublist3r.py -b -d example.com -t 50
```

## Common Use Cases

### 1. Quick Subdomain Discovery
```bash
python sublist3r.py -v -d target.com -o target_subdomains.txt
```

### 2. Comprehensive Discovery with Bruteforce
```bash
python sublist3r.py -v -b -d target.com -o target_subdomains.txt
```

### 3. Find Web Servers Only
```bash
python sublist3r.py -d target.com -p 80,443 -o web_servers.txt
```

### 4. Fast Enumeration (Specific Engines)
```bash
python sublist3r.py -e google,virustotal,dnsdumpster -d target.com
```

## Command-Line Options

| Short | Long | Description |
|-------|------|-------------|
| `-d` | `--domain` | Domain name to enumerate subdomains of (required) |
| `-b` | `--bruteforce` | Enable the subbrute bruteforce module |
| `-p` | `--ports` | Scan found subdomains against specific TCP ports (comma-separated) |
| `-v` | `--verbose` | Enable verbose mode and display results in real-time |
| `-t` | `--threads` | Number of threads for subbrute bruteforce (default: 30) |
| `-e` | `--engines` | Specify comma-separated list of search engines |
| `-o` | `--output` | Save results to text file |
| `-n` | `--no-color` | Output without color |
| `-h` | `--help` | Show help message |

## Testing

Run the test suite to verify everything works:

```bash
make test
```

This will run two test commands:
- `python sublist3r.py -v -d google.com`
- `python sublist3r.py -v -d example.com`

## Tips and Best Practices

1. **Always use verbose mode** (`-v`) to see progress in real-time
2. **Save results** (`-o`) to avoid losing discovered subdomains
3. **Use bruteforce** (`-b`) for comprehensive discovery, but note it takes longer
4. **Port scanning** (`-p`) helps identify active services quickly
5. **Specific engines** (`-e`) can speed up enumeration if you know which sources work best for your target
6. **Increase threads** (`-t`) for faster bruteforce, but be mindful of rate limits

## Cleanup

To remove the virtual environment:

```bash
make del-env
```

## Getting Help

View all available options:

```bash
python sublist3r.py -h
```

Or use the Makefile help:

```bash
make help
```

## Example Workflow

```bash
# 1. Set up environment
make setup-env
source .venv/bin/activate

# 2. Run enumeration with verbose output and save results
python sublist3r.py -v -d example.com -o example_subdomains.txt

# 3. Run with bruteforce for comprehensive discovery
python sublist3r.py -v -b -d example.com -o example_subdomains_full.txt

# 4. Check for web servers
python sublist3r.py -d example.com -p 80,443 -o example_web_servers.txt
```

## Troubleshooting

- **No results found**: Try enabling bruteforce mode (`-b`) or using different search engines
- **Slow performance**: Reduce thread count (`-t`) or use specific engines (`-e`)
- **Import errors**: Make sure the virtual environment is activated and dependencies are installed
- **Permission errors**: Ensure you have write permissions for output files

## Next Steps

- Read the full [README.md](../README.md) for advanced usage
- Learn about using Sublist3r as a Python module in your scripts
- Explore the source code to understand how each search engine works

