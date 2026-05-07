# Probable Password Generator

A sophisticated, likelihood-aware password generator designed for penetration testing and security assessments. This tool generates password candidates based on geographic locations, sports teams, college mascots, and common password patterns, ranked by real-world usage probability.

## 🎯 Features

### Core Functionality
- **Geographic Intelligence**: Generates passwords based on city names, local sports teams, and college mascots
- **Likelihood-Based Scoring**: Passwords ranked by real-world usage probability
- **Dynamic Date Handling**: Automatically uses current/previous years and respects password expiration policies
- **Custom Word Integration**: Support for organization-specific wordlists
- **Advanced Pattern Generation**: Multiple leetspeak levels, case variations, and symbol combinations

### Output Options
- **All Combinations**: Generate every possible password combination (default)
- **Limited Output**: Specify exact count for targeted lists
- **File Output**: Save results to files for organized testing
- **Debug Mode**: View scoring details for analysis

### Security Features
- **Expiration Awareness**: Filters out expired month-based passwords
- **Corporate Policy Compliance**: Bonus scoring for common password policies
- **Symbol Frequency Ordering**: Uses real-world symbol usage statistics
- **Length Optimization**: Prioritizes commonly required password lengths
- **Intelligent Length Padding**: Automatically adds duplicate symbols (e.g., "Summer2025!!") to meet minimum length requirements

## 🚀 Quick Start

```bash
# Generate passwords from keywords only
python password_generator.py --words "chase,finance" --min-length 12 --count 50

# Generate all combinations for a city
python password_generator.py --city "New York"

# Generate top 100 passwords and save to file
python password_generator.py --city "Seattle" --count 100 --output seattle_passwords.txt

# Include custom words with expiration policy
python password_generator.py --city "Dallas" --words "company,finance,server" --expiration 60
```

## 📋 Installation

### Requirements
- Python 3.6+
- No external dependencies required

### Setup
```bash
git clone https://github.com/cnmiller/Probable-Password-Generator.git
cd Probable-Password-Generator
chmod +x password_generator.py
```

## 🔧 Usage

### Basic Syntax
```bash
python password_generator.py [options]
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--city` | Target city name (optional) | None |
| `--count` | Number of passwords to generate | All combinations |
| `--output` | Output file path | stdout |
| `--words` | Custom words (comma-separated or file path) | None |
| `--min-length` | Minimum password length | 0 |
| `--symbols` | Number of symbols to use (1-8) | 5 |
| `--expiration` | Password expiration in days | None |
| `--debug` | Show password scores and types | False |

**Note**: Either `--city` or `--words` must be provided.

### Usage Examples

#### Basic Generation
```bash
# Generate all combinations for Boston
python password_generator.py --city "Boston"

# Generate top 50 passwords for Chicago
python password_generator.py --city "Chicago" --count 50

# Generate from keywords only
python password_generator.py --words "chase,finance,company" --count 50
```

#### File Output
```bash
# Save all combinations to file
python password_generator.py --city "Miami" --output miami_passwords.txt

# Generate with custom words and save
python password_generator.py --city "Denver" --words "company,brand,server" --output denver_custom.txt

# Keywords only with file output
python password_generator.py --words "admin,server,database" --output custom_passwords.txt
```

#### Advanced Options
```bash
# Corporate environment with 90-day password expiration
python password_generator.py --city "Austin" --expiration 90 --min-length 8 --output corporate_passwords.txt

# Generate passwords with minimum 12-character length (creates "Summer2025!!" style patterns)
python password_generator.py --city "Seattle" --min-length 12 --count 50 --debug

# Keywords-only with minimum length and debug information
python password_generator.py --words "chase,finance" --min-length 12 --count 25 --debug

# Penetration testing with debug information
python password_generator.py --city "Portland" --count 25 --debug --symbols 3

# Custom wordlist from file
python password_generator.py --city "Phoenix" --words /path/to/wordlist.txt --output phoenix_passwords.txt
```

#### Custom Word Files
Create a text file with one word per line:
```
company
finance
server
database
# This is a comment - will be ignored
admin
manager
```

## 🧠 Intelligence Features

### Likelihood-Based Scoring
Passwords are ranked using a sophisticated scoring system based on:

- **Word Type Priority**: Custom words > Common passwords > Seasonal patterns > Sports teams
- **Case Patterns**: Title case (most common) > lowercase > uppercase
- **Length Optimization**: 8-10 characters preferred (corporate policies)
- **Symbol Frequency**: Ordered by real-world usage (!@#$%^&*)
- **Date Intelligence**: Current year gets highest priority
- **Corporate Policies**: Bonus for complexity requirements

### Dynamic Data Sources
- **80+ Cities**: Professional sports teams from all major leagues
- **College Coverage**: FBS schools, regional universities, mascots
- **Real-time Years**: Automatically uses current/previous years
- **Expiration Awareness**: Filters months based on password age policies

### Intelligent Length Padding
When a minimum length is specified, the tool mimics real user behavior by automatically creating variants that meet length requirements:

- **Duplicate Symbols**: "Summer2025!" becomes "Summer2025!!" for 12-char minimum
- **Realistic Patterns**: Focuses on simple, natural padding that users actually employ
- **Smart Scoring**: Length-padded passwords receive priority bonuses based on real-world usage patterns

### Advanced Prioritization
The tool uses sophisticated scoring to prioritize passwords by real-world likelihood:

- **Clean Patterns First**: "Chase2025!!!" ranks 228 points higher than "Chase!2025@@"
- **Seasonal Priority**: "Spring2025!!", "Summer2025!!" appear right after custom words
- **Compound Words**: "NewYork2025!" gets priority over "newyork2025!" for multi-word inputs
- **Natural Behavior**: Patterns based on actual user behavior observed in penetration testing
- **Symbol Consistency**: Rewards consistent symbols (!!!) over mixed patterns (!@#)
- **Length Intelligence**: Passwords exactly meeting minimum lengths get priority bonuses

### Pattern Categories
1. **Custom Words** (200+ points): Organization-specific terms
2. **Common Passwords** (190 points): Clean, unmodified common passwords
3. **Seasonal + Year** (180/170 points): Season patterns with dates
4. **Monthly + Year** (160/150 points): Month patterns with dates
5. **Sports Teams** (140 points): Local team names and variants
6. **College Mascots** (130 points): University-related terms
7. **Technical Defaults** (100 points): Generic IT passwords

## 📊 Example Output

### Standard Mode
```bash
$ python password_generator.py --city "Seattle" --count 10
Generating top 10 passwords
Spring2025!
Summer2025!
Winter2025!
Seahawks2025!
Mariners2025!
Spring2025@
Summer2025@
Huskies2025!
Kraken2025!
Winter2025@
```

### Debug Mode
```bash
$ python password_generator.py --city "Seattle" --count 5 --debug
Generating top 5 passwords
Spring2025! (Score: 276.0, Type: seasons)
Summer2025! (Score: 275.0, Type: seasons)
Winter2025! (Score: 274.0, Type: seasons)
Seahawks2025! (Score: 265.0, Type: teams)
Spring2025@ (Score: 264.0, Type: seasons)
```

## 🛡️ Security Considerations

### Ethical Use Only
This tool is designed for:
- ✅ Authorized penetration testing
- ✅ Security assessments with proper authorization
- ✅ Educational and research purposes
- ✅ Testing your own systems

### Prohibited Uses
- ❌ Unauthorized access attempts
- ❌ Malicious attacks on systems you don't own
- ❌ Any illegal activities

### Best Practices
- Always obtain proper authorization before testing
- Use responsibly and within legal boundaries
- Consider rate limiting and detection evasion
- Document and report findings appropriately

## 🔍 Technical Details

### Scoring Algorithm
The likelihood scoring system considers:
- Word type and source priority
- Real-world password statistics
- Corporate policy compliance
- Character pattern frequency
- Length optimization
- Symbol usage patterns

### Performance
- Generates 40,000+ combinations per city
- Efficient memory usage with set operations
- Fast sorting with optimized scoring
- Portable single-file design

### Data Sources
- Professional sports teams (NFL, NBA, MLB, NHL, MLS, WNBA)
- College football (FBS) and major universities
- Real-world password breach analysis
- Corporate password policy studies

## 📁 Project Structure

```
Probable-Password-Generator/
├── password_generator.py    # Main application
├── README.md               # This file
├── LICENSE                 # MIT License
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore patterns
├── examples/              # Example files
│   ├── custom_words.txt   # Sample wordlist
│   └── sample_output.txt  # Example output
└── docs/                  # Additional documentation
    └── CHANGELOG.md       # Version history
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is intended for authorized security testing only. Users are responsible for ensuring they have proper authorization before using this tool against any systems. The authors are not responsible for any misuse or damage caused by this tool.

## 📞 Support

- Report bugs: [GitHub Issues](https://github.com/cnmiller/Probable-Password-Generator/issues)
- Feature requests: [GitHub Discussions](https://github.com/cnmiller/Probable-Password-Generator/discussions)

---

**⭐ Star this repository if you find it useful for your security testing!** 