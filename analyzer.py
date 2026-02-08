#!/usr/bin/env python3
"""
Wayback Site Analyzer
Analyze website archive coverage on the Wayback Machine

Usage:
    python analyzer.py example.com
    python analyzer.py example.com --output report.txt
"""

import sys
import argparse
import requests
from collections import defaultdict
from datetime import datetime
from urllib.parse import quote
import time
import threading


class ProgressIndicator:
    """Show animated progress while waiting"""
    def __init__(self, message="Processing"):
        self.message = message
        self.running = False
        self.thread = None
        
    def _animate(self):
        """Animation loop"""
        spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        idx = 0
        start_time = time.time()
        while self.running:
            elapsed = int(time.time() - start_time)
            sys.stdout.write(f'\r{spinner[idx]} {self.message}... {elapsed}s ')
            sys.stdout.flush()
            idx = (idx + 1) % len(spinner)
            time.sleep(0.1)
    
    def start(self):
        """Start progress indicator"""
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self, final_message="Done"):
        """Stop progress indicator"""
        self.running = False
        if self.thread:
            self.thread.join()
        sys.stdout.write(f'\r✅ {final_message}' + ' ' * 20 + '\n')
        sys.stdout.flush()


class WaybackAnalyzer:
    """Analyze website coverage in the Wayback Machine"""
    
    CDX_API = "https://web.archive.org/cdx/search/cdx"
    
    def __init__(self, domain):
        self.domain = domain.replace('http://', '').replace('https://', '').strip('/')
        self.snapshots = []
        
    def fetch_snapshots(self):
        """Fetch snapshot data from CDX API"""
        print(f"🔍 Analyzing: {self.domain}")
        print("━" * 50)
        
        params = {
            'url': self.domain,
            'matchType': 'domain',
            'output': 'json',
            'fl': 'timestamp,statuscode,mimetype',
            'collapse': 'timestamp:8',  # Collapse by day
            'limit': 100000  # Free version limit
        }
        
        # Start progress indicator
        progress = ProgressIndicator("Fetching archive data from Wayback Machine")
        progress.start()
        
        try:
            response = requests.get(self.CDX_API, params=params, timeout=90)
            response.raise_for_status()
            data = response.json()
            
            # Stop progress indicator
            progress.stop("Data fetched successfully!")
            
            # Skip header row
            if data and len(data) > 1:
                self.snapshots = data[1:]
                print(f"📊 Found {len(self.snapshots):,} snapshots to analyze\n")
                return True
            else:
                print("❌ No archive data found for this domain.")
                print("\n💡 Tip: Make sure the domain was archived. Check https://web.archive.org")
                return False
                
        except requests.exceptions.Timeout:
            progress.stop("Request timed out")
            print("❌ This domain may have too many snapshots.")
            print("\n💡 Tips:")
            print("   • Try a smaller/newer domain first (e.g., example.com)")
            print("   • Very large sites like google.com may timeout")
            print("   • For enterprise analysis, contact: https://waybackrevive.com/contact-us")
            return False
        except requests.exceptions.RequestException as e:
            progress.stop("Request failed")
            print(f"❌ Error: {e}")
            print("\n💡 Troubleshooting:")
            print("   • Check your internet connection")
            print("   • Try again in a few moments")
            print("   • Try a different domain to test")
            return False
    
    def analyze(self):
        """Analyze the snapshot data"""
        if not self.snapshots:
            return None
        
        # Group by year
        yearly_counts = defaultdict(int)
        timestamps = []
        
        for snapshot in self.snapshots:
            timestamp = snapshot[0]
            year = timestamp[:4]
            yearly_counts[year] += 1
            timestamps.append(timestamp)
        
        # Sort timestamps
        timestamps.sort()
        first_snapshot = timestamps[0]
        last_snapshot = timestamps[-1]
        
        # Calculate missing years
        all_years = set(yearly_counts.keys())
        if all_years:
            start_year = int(min(all_years))
            end_year = int(max(all_years))
            expected_years = set(str(y) for y in range(start_year, end_year + 1))
            missing_years = expected_years - all_years
        else:
            missing_years = set()
        
        return {
            'total_snapshots': len(self.snapshots),
            'yearly_counts': dict(sorted(yearly_counts.items())),
            'first_snapshot': self.format_timestamp(first_snapshot),
            'last_snapshot': self.format_timestamp(last_snapshot),
            'missing_years': sorted(missing_years),
            'total_years': len(yearly_counts)
        }
    
    def format_timestamp(self, timestamp):
        """Convert timestamp to readable date"""
        try:
            return datetime.strptime(timestamp[:8], '%Y%m%d').strftime('%Y-%m-%d')
        except:
            return timestamp[:8]
    
    def calculate_health_score(self, stats):
        """Calculate archive health score (simple version)"""
        if not stats:
            return 0
        
        total_years = stats['total_years']
        missing_years = len(stats['missing_years'])
        
        if total_years == 0:
            return 0
        
        coverage_rate = ((total_years - missing_years) / total_years) * 100
        
        # Bonus for recent activity
        if stats['last_snapshot'].startswith('202'):
            coverage_rate = min(coverage_rate + 10, 100)
        
        return int(coverage_rate)
    
    def print_report(self, stats):
        """Print beautiful report"""
        if not stats:
            return
        
        print("\n✅ ARCHIVE STATUS: Available\n")
        
        print("📊 Quick Stats:")
        print(f"   Total Snapshots: {stats['total_snapshots']:,}")
        print(f"   First Archived: {stats['first_snapshot']}")
        print(f"   Last Archived: {stats['last_snapshot']}")
        print(f"   Total Years: {stats['total_years']}")
        
        print("\n📅 Coverage by Year:")
        yearly = stats['yearly_counts']
        max_count = max(yearly.values()) if yearly else 1
        
        # Show last 10 years for readability
        years_to_show = sorted(yearly.keys())[-10:]
        
        for year in years_to_show:
            count = yearly[year]
            bar_length = int((count / max_count) * 10)
            bar = "█" * bar_length + "░" * (10 - bar_length)
            print(f"   {year}: {bar} {count:,} snapshots")
        
        if len(yearly) > 10:
            print(f"   ... and {len(yearly) - 10} more years")
        
        if stats['missing_years']:
            print(f"\n⚠️ Missing Years: {', '.join(stats['missing_years'][:10])}")
            if len(stats['missing_years']) > 10:
                print(f"   ... and {len(stats['missing_years']) - 10} more")
        
        health = self.calculate_health_score(stats)
        health_label = "Excellent" if health >= 90 else "Good" if health >= 70 else "Fair" if health >= 50 else "Limited"
        print(f"\n📈 Archive Health: {health}% ({health_label})")
        
        # Add upgrade CTA
        print("\n" + "━" * 50)
        print("\n💡 This is a basic analysis.")
        print("\n📦 FREE VERSION LIMITATIONS:")
        print("   • Limited to 100,000 snapshots")
        print("   • No deep page-level analysis")
        print("   • No content recovery")
        print("   • No asset retrieval")
        
        print("\n🚀 NEED FULL WEBSITE RECOVERY?")
        print("   Our professional team can restore your complete website")
        print("   from the Wayback Machine with all content, images, and")
        print("   functionality intact.")
        print("\n   👉 Get started: https://waybackrevive.com/contact-us")
        print("   📧 Email: support@waybackrevive.com")
        
        print("\n" + "━" * 50)
    
    def save_report(self, stats, filename):
        """Save report to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Wayback Machine Analysis Report\n")
            f.write(f"Domain: {self.domain}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Total Snapshots: {stats['total_snapshots']:,}\n")
            f.write(f"First Archived: {stats['first_snapshot']}\n")
            f.write(f"Last Archived: {stats['last_snapshot']}\n")
            f.write(f"Total Years: {stats['total_years']}\n\n")
            
            f.write("Coverage by Year:\n")
            for year, count in sorted(stats['yearly_counts'].items()):
                f.write(f"  {year}: {count:,} snapshots\n")
            
            if stats['missing_years']:
                f.write(f"\nMissing Years: {', '.join(stats['missing_years'])}\n")
            
            health = self.calculate_health_score(stats)
            f.write(f"\nArchive Health Score: {health}%\n")
            
            f.write("\n" + "=" * 50 + "\n")
            f.write("\nFor professional website recovery services:\n")
            f.write("Visit: https://waybackrevive.com/contact-us\n")
            f.write("Email: support@waybackrevive.com\n")
        
        print(f"\n💾 Report saved to: {filename}\n\n")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Analyze website archive coverage on the Wayback Machine',
        epilog='For professional recovery: https://waybackrevive.com/contact-us'
    )
    parser.add_argument('domains', nargs='+', help='Domain(s) to analyze')
    parser.add_argument('--output', '-o', help='Save report to file')
    
    args = parser.parse_args()
    
    print("\n" + "═" * 50)
    print("  🔍 WAYBACK SITE ANALYZER")
    print("  Free Archive Coverage Tool")
    print("═" * 50 + "\n")
    
    for domain in args.domains:
        analyzer = WaybackAnalyzer(domain)
        
        if analyzer.fetch_snapshots():
            stats = analyzer.analyze()
            analyzer.print_report(stats)
            
            if args.output:
                analyzer.save_report(stats, args.output)
        
        if len(args.domains) > 1:
            print("\n" + "=" * 50 + "\n")
    
    print("\n⭐ If this tool helped you, star us on GitHub!")
    print("🔗 Professional recovery: https://waybackrevive.com\n")


if __name__ == '__main__':
    # Allow interactive mode if no args
    if len(sys.argv) == 1:
        print("\n" + "═" * 50)
        print("  🔍 WAYBACK SITE ANALYZER")
        print("  Free Archive Coverage Tool")
        print("═" * 50 + "\n")
        
        domain = input("Enter domain to analyze (e.g., example.com): ").strip()
        
        if domain:
            analyzer = WaybackAnalyzer(domain)
            if analyzer.fetch_snapshots():
                stats = analyzer.analyze()
                analyzer.print_report(stats)
        
        input("\nPress Enter to exit...")
    else:
        main()
