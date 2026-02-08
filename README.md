# 🔍 Wayback Site Analyzer

> **Free tool** to analyze your website's archive coverage on the Wayback Machine

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)

## 🎯 What Does This Do?

Instantly check any website's archival status:

- ✅ **Total Snapshots** - How many times it was archived
- 📅 **Coverage Timeline** - Years with archive data
- ⚠️ **Missing Years** - Gaps in your archive
- 📊 **Page Coverage** - How many pages are archived
- 🔗 **Quick Stats** - First & last archived dates

Perfect for:
- 🏢 **Business owners** checking their digital history
- 📈 **SEO agencies** auditing client archives
- 🎓 **Researchers** validating historical data
- 💼 **Legal teams** needing archive evidence

## 🚀 Quick Start (Non-Technical Users)

### Option 1: Use Online (Easiest)
1. Download `analyzer.py`
2. Double-click to run
3. Enter your website URL
4. Get instant report!

### Option 2: Command Line
```bash
python analyzer.py example.com
```

## 💻 Installation

### Requirements
- Python 3.7 or higher
- Internet connection

### Setup (One-Time)
```bash
# Clone this repository
git clone https://github.com/waybackrevive/wayback-site-analyzer.git
cd wayback-site-analyzer

# Install dependencies
pip install -r requirements.txt
```

## 📖 Usage Examples

### Basic Analysis
```bash
python analyzer.py google.com
```

### Multiple Sites
```bash
python analyzer.py google.com amazon.com facebook.com
```

### Save Report
```bash
python analyzer.py example.com --output report.txt
```

## 📊 Sample Output

```
🔍 Analyzing: example.com
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ ARCHIVE STATUS: Available

📊 Quick Stats:
   Total Snapshots: 4,523
   First Archived: 1996-12-31
   Last Archived: 2026-02-07
   Total Years: 30

📅 Coverage by Year:
   1996: ██████░░░░ 45 snapshots
   1997: ████████░░ 78 snapshots
   1998: ██████████ 123 snapshots
   ...

⚠️ Missing Years: 2001, 2005

📈 Archive Health: 87% (Good)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## ⚠️ Limitations (Free Version)

This free tool provides basic analysis. For advanced features, you'll need professional help:

- ❌ Deep page-level analysis (10,000+ pages)
- ❌ Content reconstruction
- ❌ Broken link recovery
- ❌ Asset retrieval (images, CSS, JS)
- ❌ Database restoration
- ❌ Custom domain migration
- ❌ SEO metadata recovery

## 🚀 Need Full Website Recovery?

**This tool shows what's archived. We can restore it.**

Our professional team at **WaybackRevive** specializes in:

✨ Complete website restoration
✨ Content recovery from archives
✨ Database reconstruction
✨ SEO-optimized migration
✨ Custom domain setup
✨ Technical support

### 👉 [Get Professional Recovery → waybackrevive.com/contact-us](https://waybackrevive.com/contact-us)

📧 Quick consultation: support@waybackrevive.com

---

## 🛠️ Technical Details

### How It Works
1. Queries Wayback Machine CDX API
2. Aggregates snapshot data
3. Calculates coverage statistics
4. Identifies archive gaps
5. Generates visual report

### API Endpoints Used
- `http://web.archive.org/cdx/search/cdx`
- Public, no API key required
- Rate-limited (respectful usage)

### Data Privacy
- ✅ No data stored
- ✅ No tracking
- ✅ Open source
- ✅ Runs locally

## 🤝 Contributing

Found a bug? Have a feature request?

1. Fork this repository
2. Create your feature branch
3. Submit a pull request

We welcome contributions from the community!

## 📜 License

MIT License - Free to use and modify

## ⭐ Show Support

If this tool helped you:
- ⭐ Star this repository
- 🐦 Share on social media
- 💼 Reach out if you need professional recovery

---

## 🔗 Resources

- [Wayback Machine](https://web.archive.org/)
- [CDX API Documentation](https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server)
- [Professional Recovery Services](https://waybackrevive.com)

---

<p align="center">
  <strong>Made with ❤️ by WaybackRevive Team</strong><br>
  <a href="https://waybackrevive.com">waybackrevive.com</a>
</p>
