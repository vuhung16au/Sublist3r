#!/usr/bin/env python3
# coding: utf-8
# Sublist3r v1.0
# By Ahmed Aboul-Ela - twitter.com/aboul3la

# modules in standard library
import re
import sys
import os
import argparse
import multiprocessing
import threading
import socket
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.panel import Panel
import ui_styles
import urllib.parse as urlparse

# external modules
from subbrute import subbrute
import yaml

# Import engines
from engines import ENGINE_REGISTRY, ALL_ENGINES, get_enabled_engines, set_console

# In case you cannot install some of the required development packages
# there's also an option to disable the SSL warning:
try:
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()
except:
    pass

# Check if we are running this on windows platform
is_windows = sys.platform.startswith('win')

# Global Rich console instance - initialized in interactive() function
console = None

def no_color():
    """Disable colors in console output."""
    global console
    console = Console(no_color=True, force_terminal=True)
    ui_styles.set_console(console)
    set_console(console)


def banner():
    """Display Sublist3r banner using Rich."""
    banner_ascii = r"""
                 ____        _     _ _     _   _____
                / ___| _   _| |__ | (_)___| |_|___ / _ __
                \___ \| | | | '_ \| | / __| __| |_ \| '__|
                 ___) | |_| | |_) | | \__ \ |_ ___) | |
                |____/ \__,_|_.__/|_|_|___/\__|____/|_|
    """
    subtitle = "# Coded By Ahmed Aboul-Ela - @aboul3la, revived by @vuhung16au/Sublist3r.git"
    
    if console:
        console.print(banner_ascii, style=ui_styles.UIStyles.BANNER)
        console.print(subtitle, style=ui_styles.UIStyles.BANNER_SUBTITLE)
    else:
        print(banner_ascii)
        print(subtitle)


def parser_error(errmsg):
    banner()
    if console:
        console.print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
        console.print(f"[{ui_styles.UIStyles.ERROR}]Error:[/{ui_styles.UIStyles.ERROR}] {errmsg}")
    else:
        print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
        print("Error: " + errmsg)
    sys.exit()


def load_config(config_path=None):
    """
    Load engine configuration from YAML file.
    
    Args:
        config_path: Path to config file. If None, uses default location.
    
    Returns:
        Dictionary with config data, or None if file doesn't exist
    """
    if config_path is None:
        # Default config location: config/engines.yaml relative to script
        script_dir = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(script_dir, 'config', 'engines.yaml')
    
    if not os.path.exists(config_path):
        return None
    
    try:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        return config_data
    except Exception as e:
        if console:
            console.print(f"[{ui_styles.UIStyles.WARNING}][!] Warning: Could not load config file {config_path}: {e}[/{ui_styles.UIStyles.WARNING}]")
        else:
            print(f"[!] Warning: Could not load config file {config_path}: {e}")
        return None


def parse_args():
    # parse the arguments
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -d google.com")
    parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-d', '--domain', help="Domain name to enumerate it's subdomains", required=True)
    parser.add_argument('-b', '--bruteforce', help='Enable the subbrute bruteforce module', nargs='?', default=False)
    parser.add_argument('-p', '--ports', help='Scan the found subdomains against specified tcp ports')
    parser.add_argument('-v', '--verbose', help='Enable Verbosity and display results in realtime', nargs='?', default=False)
    parser.add_argument('-t', '--threads', help='Number of threads to use for subbrute bruteforce', type=int, default=30)
    parser.add_argument('-e', '--engines', help='Specify a comma-separated list of search engines')
    parser.add_argument('-o', '--output', help='Save the results to text file')
    parser.add_argument('-n', '--no-color', help='Output without color', default=False, action='store_true')
    parser.add_argument('-c', '--config', help='Path to engine configuration file (YAML format)')
    return parser.parse_args()


def write_file(filename, subdomains):
    # saving subdomains results to output file
    if console:
        console.print(f"[{ui_styles.UIStyles.WARNING}][-][/{ui_styles.UIStyles.WARNING}] Saving results to file: [{ui_styles.UIStyles.ERROR}]{filename}[/{ui_styles.UIStyles.ERROR}]")
    else:
        print(f"[-] Saving results to file: {filename}")
    with open(str(filename), 'wt') as f:
        for subdomain in subdomains:
            f.write(subdomain + os.linesep)


def subdomain_sorting_key(hostname):
    """Sorting key for subdomains

    This sorting key orders subdomains from the top-level domain at the right
    reading left, then moving '^' and 'www' to the top of their group. For
    example, the following list is sorted correctly:

    [
        'example.com',
        'www.example.com',
        'a.example.com',
        'www.a.example.com',
        'b.a.example.com',
        'b.example.com',
        'example.net',
        'www.example.net',
        'a.example.net',
    ]

    """
    parts = hostname.split('.')[::-1]
    if parts[-1] == 'www':
        return parts[:-1], 1
    return parts, 0


class portscan():
    def __init__(self, subdomains, ports):
        self.subdomains = subdomains
        self.ports = ports
        self.lock = None

    def port_scan(self, host, ports):
        openports = []
        self.lock.acquire()
        for port in ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                result = s.connect_ex((host, int(port)))
                if result == 0:
                    openports.append(port)
                s.close()
            except Exception:
                pass
        self.lock.release()
        if len(openports) > 0:
            if console:
                console.print(f"[{ui_styles.UIStyles.SUCCESS}]{host}[/{ui_styles.UIStyles.SUCCESS}] - [{ui_styles.UIStyles.ERROR}]Found open ports:[/{ui_styles.UIStyles.ERROR}] [{ui_styles.UIStyles.PORT}]{', '.join(openports)}[/{ui_styles.UIStyles.PORT}]")
            else:
                print(f"{host} - Found open ports: {', '.join(openports)}")

    def run(self):
        self.lock = threading.BoundedSemaphore(value=20)
        for subdomain in self.subdomains:
            t = threading.Thread(target=self.port_scan, args=(subdomain, self.ports))
            t.start()


def format_elapsed_time(seconds):
    """Format elapsed time in a human-readable format.
    
    Args:
        seconds: Elapsed time in seconds (float)
    
    Returns:
        Formatted time string
    """
    if seconds < 1:
        return f"{seconds:.2f} seconds"
    elif seconds < 60:
        return f"{int(round(seconds))} seconds"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(round(seconds % 60))
        return f"{minutes} minute{'s' if minutes != 1 else ''} {secs} second{'s' if secs != 1 else ''}"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(round(seconds % 60))
        return f"{hours} hour{'s' if hours != 1 else ''} {minutes} minute{'s' if minutes != 1 else ''} {secs} second{'s' if secs != 1 else ''}"


def display_summary(total_subdomains, search_count, bruteforce_count, engines_used, elapsed_time, engine_names, enable_bruteforce, verbose, silent):
    """Display enumeration summary statistics.
    
    Args:
        total_subdomains: Total unique subdomains found
        search_count: Number of subdomains from search engines
        bruteforce_count: Number of subdomains from bruteforce
        engines_used: Number of engines used
        elapsed_time: Elapsed time in seconds
        engine_names: List of engine names
        enable_bruteforce: Whether bruteforce was enabled
        verbose: Whether verbose mode is enabled
        silent: Whether silent mode is enabled
    """
    # Only display if verbose and not silent
    if not verbose or silent:
        return
    
    # Format elapsed time
    time_str = format_elapsed_time(elapsed_time)
    
    # Build summary content
    summary_lines = [
        f"Total Subdomains Found: {total_subdomains}",
        f"Engines Used: {engines_used}",
        f"Scan Time: {time_str}",
        "",
        "Breakdown by Source:",
        f"  • Search Engines: {search_count} subdomain{'s' if search_count != 1 else ''}"
    ]
    
    # Add bruteforce line if enabled
    if enable_bruteforce:
        summary_lines.append(f"  • Bruteforce: {bruteforce_count} subdomain{'s' if bruteforce_count != 1 else ''}")
    
    summary_lines.append("")
    
    # Add engine names
    if engine_names:
        engine_names_sorted = sorted(engine_names)
        engine_str = ", ".join(engine_names_sorted)
        summary_lines.append(f"Engines: {engine_str}")
    else:
        summary_lines.append("Engines: None")
    
    # Join all lines
    summary_content = "\n".join(summary_lines)
    
    # Display using Rich Panel
    if console:
        panel = Panel(
            summary_content,
            title="[bold magenta]Enumeration Summary[/bold magenta]",
            border_style="magenta"
        )
        console.print(panel)
    else:
        # Fallback for non-Rich console
        print("\n" + "=" * 60)
        print("Enumeration Summary")
        print("=" * 60)
        print(summary_content)
        print("=" * 60 + "\n")


def main(domain, threads, savefile, ports, silent, verbose, enable_bruteforce, engines, config_path=None):
    bruteforce_list = set()
    search_list = set()

    if is_windows:
        subdomains_queue = list()
    else:
        subdomains_queue = multiprocessing.Manager().list()

    # Check Bruteforce Status
    if enable_bruteforce or enable_bruteforce is None:
        enable_bruteforce = True

    # Validate domain
    domain_check = re.compile(r"^(http|https)?[a-zA-Z0-9]+([\-\.]{1}[a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$")
    if not domain_check.match(domain):
        if not silent:
            if console:
                console.print(f"[{ui_styles.UIStyles.ERROR}]Error: Please enter a valid domain[/{ui_styles.UIStyles.ERROR}]")
            else:
                print("Error: Please enter a valid domain")
        return []

    if not domain.startswith('http://') and not domain.startswith('https://'):
        domain = 'http://' + domain

    parsed_domain = urlparse.urlparse(domain)

    # Start timing for enumeration
    start_time = time.time()

    if not silent:
        if console:
            console.print(f"[{ui_styles.UIStyles.INFO}][-] Enumerating subdomains now for {parsed_domain.netloc}[/{ui_styles.UIStyles.INFO}]")

    if verbose and not silent:
        if console:
            console.print(f"[{ui_styles.UIStyles.WARNING}][-] verbosity is enabled, will show the subdomains results in realtime[/{ui_styles.UIStyles.WARNING}]")
        else:
            print("[-] verbosity is enabled, will show the subdomains results in realtime")

    # Load configuration
    config_data = None
    if config_path or engines is None:
        config_data = load_config(config_path)

    # Determine which engines to use
    chosenEnums = []

    if engines is not None:
        # CLI argument takes precedence - use specified engines
        engines = engines.split(',')
        for engine in engines:
            engine_lower = engine.lower().strip()
            if engine_lower in ENGINE_REGISTRY:
                chosenEnums.append(ENGINE_REGISTRY[engine_lower])
    else:
        # Use config file or default to all engines
        chosenEnums = get_enabled_engines(config_data)

    if not chosenEnums:
        if not silent:
            if console:
                console.print(f"[{ui_styles.UIStyles.WARNING}][!] Warning: No engines enabled. Using all engines by default.[/{ui_styles.UIStyles.WARNING}]")
            else:
                print("[!] Warning: No engines enabled. Using all engines by default.")
        chosenEnums = ALL_ENGINES

    # Start the engines enumeration with progress tracking
    enums = [enum(domain, [], q=subdomains_queue, silent=silent, verbose=verbose) for enum in chosenEnums]
    
    # Extract engine names for summary
    engine_names = [enum.engine_name for enum in enums]
    
    if not silent and console:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Enumerating subdomains...", total=len(enums))
            
            # Start all enumeration processes
            for enum in enums:
                enum.start()
            
            # Wait for all to complete and update progress
            completed = 0
            for enum in enums:
                enum.join()
                completed += 1
                progress.update(task, completed=completed)
    else:
        # Fallback without progress bar
        for enum in enums:
            enum.start()
        for enum in enums:
            enum.join()

    subdomains = set(subdomains_queue)
    for subdomain in subdomains:
        search_list.add(subdomain)

    if enable_bruteforce:
        if not silent:
            if console:
                console.print(f"[{ui_styles.UIStyles.SUCCESS}][-] Starting bruteforce module now using subbrute..[/{ui_styles.UIStyles.SUCCESS}]")
            else:
                print("[-] Starting bruteforce module now using subbrute..")
        record_type = False
        path_to_file = os.path.dirname(os.path.realpath(__file__))
        subs = os.path.join(path_to_file, 'subbrute', 'names.txt')
        resolvers = os.path.join(path_to_file, 'subbrute', 'resolvers.txt')
        process_count = threads
        output = False
        json_output = False
        bruteforce_list = subbrute.print_target(parsed_domain.netloc, record_type, subs, resolvers, process_count, output, json_output, search_list, verbose)

    # End timing for enumeration
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Count subdomains by source BEFORE union (for accurate breakdown)
    search_count = len(search_list)
    bruteforce_count = len(bruteforce_list) if enable_bruteforce else 0

    subdomains = search_list.union(bruteforce_list)

    if subdomains:
        subdomains = sorted(subdomains, key=subdomain_sorting_key)

        if savefile:
            write_file(savefile, subdomains)

        if not silent:
            if console:
                console.print(f"[{ui_styles.UIStyles.WARNING}][-] Total Unique Subdomains Found: {len(subdomains)}[/{ui_styles.UIStyles.WARNING}]")
            else:
                print(f"[-] Total Unique Subdomains Found: {len(subdomains)}")

        if ports:
            if not silent:
                if console:
                    console.print(f"[{ui_styles.UIStyles.SUCCESS}][-] Start port scan now for the following ports: [{ui_styles.UIStyles.PORT}]{ports}[/{ui_styles.UIStyles.PORT}][/{ui_styles.UIStyles.SUCCESS}]")
                else:
                    print(f"[-] Start port scan now for the following ports: {ports}")
            ports = ports.split(',')
            pscan = portscan(subdomains, ports)
            pscan.run()
            
            # Display summary after port scan (only in verbose mode)
            display_summary(
                total_subdomains=len(subdomains),
                search_count=search_count,
                bruteforce_count=bruteforce_count,
                engines_used=len(enums),
                elapsed_time=elapsed_time,
                engine_names=engine_names,
                enable_bruteforce=enable_bruteforce,
                verbose=verbose,
                silent=silent
            )

        elif not silent:
            # Display subdomains in a Rich table
            if console:
                table = Table(title="Subdomains Found", show_header=True, header_style="bold magenta")
                table.add_column("Subdomain", style=ui_styles.UIStyles.SUBDOMAIN, overflow="fold")
                for subdomain in subdomains:
                    table.add_row(subdomain)
                console.print(table)
            else:
                for subdomain in subdomains:
                    print(subdomain)
        
        # Display summary (only in verbose mode)
        display_summary(
            total_subdomains=len(subdomains),
            search_count=search_count,
            bruteforce_count=bruteforce_count,
            engines_used=len(enums),
            elapsed_time=elapsed_time,
            engine_names=engine_names,
            enable_bruteforce=enable_bruteforce,
            verbose=verbose,
            silent=silent
        )
    else:
        # No subdomains found, but still show summary if verbose
        display_summary(
            total_subdomains=0,
            search_count=search_count,
            bruteforce_count=bruteforce_count,
            engines_used=len(enums),
            elapsed_time=elapsed_time,
            engine_names=engine_names,
            enable_bruteforce=enable_bruteforce,
            verbose=verbose,
            silent=silent
        )
    return subdomains


def interactive():
    global console
    args = parse_args()
    domain = args.domain
    threads = args.threads
    savefile = args.output
    ports = args.ports
    enable_bruteforce = args.bruteforce
    verbose = args.verbose
    engines = args.engines
    config_path = args.config
    if verbose or verbose is None:
        verbose = True
    
    # Initialize Rich console
    if args.no_color:
        no_color()
    else:
        console = Console(force_terminal=True)
        ui_styles.set_console(console)
        set_console(console)
    
    banner()
    res = main(domain, threads, savefile, ports, silent=False, verbose=verbose, enable_bruteforce=enable_bruteforce, engines=engines, config_path=config_path)

if __name__ == "__main__":
    interactive()
