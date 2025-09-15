# Raven Wordlist Generator

A powerful and customizable wordlist generator tool designed for cybersecurity professionals and penetration testers to create targeted wordlists based on personal information.

## Features

- Personalized Wordlists: Generate wordlists using personal information like names, birthdays, phone numbers, and more
- Advanced Combinatorics: Uses permutations, combinations, and interleaving techniques
- Leet Speak Support: Automatically generates common leet substitutions (e.g., @ for a, 3 for e)
- Customizable Length: Set minimum and maximum password lengths
- Output Control: Limit the total number of generated words with the max_words parameter
- Multiple Formats: Supports various separator characters (., -, _) between words
- Case Variations: Generates uppercase, lowercase, and capitalized versions

## Installation

1. Clone the repository:
git clone https://github.com/yourusername/raven-wg.git
cd raven-wg

2. Ensure you have Python 3.x installed

## Usage

### Basic Syntax
python3 raven-wg.py -f FIRSTNAME -l LASTNAME [OPTIONS] -m MAX_WORDS -o OUTPUT_FILE

### Example
python3 raven-wg.py -f john -l doe -b 1990-05-15 -p 5551234567 --family jane,smith -i company,tech --min 6 --max 12 -m 5000 -o custom_wordlist.txt -d

### Options
Option          Description                             Example
-f, --firstname Target's first name                     -f john
-l, --lastname  Target's last name                      -l doe
-b, --birthday  Birthday in YYYY-MM-DD format           -b 1990-05-15
-n, --nationalid National ID number                     -n 123456789
-p, --phone     Phone number                            -p 5551234567
--family        Family members (comma separated)        --family jane,smith
-i, --info      Other information (comma separated)     -i company,tech
-o, --output    Output file name                        -o wordlist.txt
--min           Minimum password length                 --min 6
--max           Maximum password length                 --max 12
-m, --max_words Maximum number of words to generate     -m 5000
-d, --display   Print generated words to terminal       -d

## Ethical Use Disclaimer

This tool is intended for:
- Security professionals conducting authorized penetration tests
- System administrators testing their own systems' password strength
- Educational purposes in controlled environments

Please ensure you have proper authorization before using this tool against any system. Unauthorized use may violate laws and regulations. The developers are not responsible for misuse of this software.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
