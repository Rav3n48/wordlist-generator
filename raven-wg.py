import itertools
import argparse
from datetime import datetime



banner = """\n\n\n\n\nooooooooo.         .o.       oooooo     oooo oooooooooooo ooooo      ooo
`888   `Y88.      .888.       `888.     .8'  `888'     `8 `888b.     `8'
 888   .d88'     .8"888.       `888.   .8'    888          8 `88b.    8
 888ooo88P'     .8' `888.       `888. .8'     888oooo8     8   `88b.  8
 888`88b.      .88ooo8888.       `888.8'      888    "     8     `88b.8
 888  `88b.   .8'     `888.       `888'       888       o  8       `888
o888o  o888o o88o     o8888o       `8'       o888ooooood8 o8o        `8\n\n\n\n\n"""


def generate_wordlist(first_name=None, last_name=None, birthday=None, national_id=None, phone_number=None, 
                     family_members=None, other_info=None, min_length=4, max_length=8, display=None):
    """
    Generate a wordlist based on extensive personal information
    """
    if display:
        print("display option is true \n")
        if first_name:
            print(f'firstname: {first_name}')
        if last_name:
            print(f'lastname: {last_name}')
        if birthday:
            print(f'birthday: {birthday}')
        if national_id:
            print(f'national id: {national_id}')
        if phone_number:
            print(f'phone number: {phone_number}')
        if family_members:
            print(f'family members: {family_members}')
        if other_info:
            print(f'other info: {other_info}')
        if min_length:
            print(f'minimum length: {min_length}')
        if max_length:
            print(f'maximum length: {max_length}')
        print("printing generated words...\n")
        counter = 1

    wordlist = set()

    informations = []
    
    # Parse and add firstname into informations
    if first_name:
        informations.extend([first_name.lower(), first_name.capitalize()])

    # Parse and add lastname into information
    if last_name:
            informations.extend([last_name.lower(), last_name.capitalize()])

    # Parse and add birthday into informations
    if birthday:
        try:
            birth_date = datetime.strptime(birthday, "%Y-%m-%d")
            year = str(birth_date.year)
            year_short = year[2:]
            month = str(birth_date.month)
            day = str(birth_date.day)
            month_padded = month.zfill(2)
            day_padded = day.zfill(2)
            
            informations.extend([
        year,
        year_short,
        month,
        day,
        month_padded,
        day_padded,
        month + day,
        day + month,
        month_padded + day_padded,
        day_padded + month_padded,
        year_short + month,
        year_short + day,
        month + year_short,
        day + year_short
        ])
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return []
    
    # Parse and add national ID into informations
    if national_id:
        informations.extend([national_id, national_id[-4:], national_id[:4], national_id[-6:], national_id[:6]])
    
    # Parse and add phone number into informations
    if phone_number:
        # Remove common separators
        clean_phone = phone_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')
        informations.extend([
            clean_phone,
            clean_phone[-4:],
            clean_phone[-6:],
            clean_phone[:3]  # area code
        ])
    
    # Parse and add family members into informations
    family_list = []
    if family_members:
        for member in family_members.split(','):
            member = member.strip()
            if member:
                informations.extend([member.lower(), member.capitalize()])
                family_list.extend([member.lower(), member.capitalize()])
    
    # Add other info into informations
    if other_info:
        for word in other_info.split(','):
            word = word.strip()
            if word:
                informations.extend([word.lower(), word.capitalize()])
    
    # Common separators and suffixes
    separators = ['', '.', '-', '_']
    number_suffixes = ['!', '@', '#', '$', '%', '&', '*', '123', '1', '007', '69', '1234', '000']
    
    # Generate combinations
    for info in informations:
        if min_length <= len(info) <= max_length:
            wordlist.add(info)
            if display:
                print(f'{counter}.Generated: {info}')
                counter += 1
    
    # Combine first name and last name with separators
    if last_name:
        for sep in separators:
            combo = f"{first_name.lower()}{sep}{last_name.lower()}"
            if min_length <= len(combo) <= max_length:
                wordlist.add(combo)
                if display:
                    print(f'{counter}.Generated: {combo}')
                    counter += 1
        
        combo = f"{last_name.lower()}{sep}{first_name.lower()}"
        if min_length <= len(combo) <= max_length:
            wordlist.add(combo)
            if display:
                print(f'{counter}.Generated: {combo}')
                counter += 1
            
        combo_cap = f"{first_name.capitalize()}{sep}{last_name.capitalize()}"
        if min_length <= len(combo_cap) <= max_length:
            wordlist.add(combo_cap)
            if display:
                print(f'{counter}.Generated: {combo_cap}')
                counter += 1
    
    # Combine names with date components
    if last_name:
        name_parts = [first_name.lower(), last_name.lower(), 
                    first_name.capitalize(), last_name.capitalize()]
    name_parts = [first_name.lower(), first_name.capitalize()]
    
    # Add family members to name parts
    
    name_parts.extend(family_list)
    
    if birthday:
        for name_part in name_parts:
            for date_part in [year, year_short, month, day, month+day, day+month]:
                for sep in separators:
                    # Name + date
                    combo = f"{name_part}{sep}{date_part}"
                    if min_length <= len(combo) <= max_length:
                        wordlist.add(combo)
                        if display:
                            print(f'{counter}.Generated: {combo}')
                            counter += 1
                
                # Date + name
                combo = f"{date_part}{sep}{name_part}"
                if min_length <= len(combo) <= max_length:
                    wordlist.add(combo)
                    if display:
                        print(f'{counter}.Generated: {combo}')
                        counter += 1
    
    # Combine with national ID if provided
    if national_id:
        for name_part in name_parts:
            for sep in separators:
                # Name + national ID
                combo = f"{name_part}{sep}{national_id}"
                if min_length <= len(combo) <= max_length:
                    wordlist.add(combo)
                    if display:
                        print(f'{counter}.Generated: {combo}')
                        counter += 1
                
                # Name + partial national ID
                combo = f"{name_part}{sep}{national_id[-4:]}"
                if min_length <= len(combo) <= max_length:
                    wordlist.add(combo)
                    if display:
                        print(f'{counter}.Generated: {combo}')
                        counter += 1
                
                # National ID + name
                combo = f"{national_id}{sep}{name_part}"
                if min_length <= len(combo) <= max_length:
                    wordlist.add(combo)
                    if display:
                        print(f'{counter}.Generated: {combo}')
                        counter += 1
    
    # Combine with phone number if provided
    if phone_number:
        clean_phone = phone_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')
        for name_part in name_parts:
            for sep in separators:
                # Name + phone
                combo = f"{name_part}{sep}{clean_phone}"
                if min_length <= len(combo) <= max_length:
                    wordlist.add(combo)
                    if display:
                        print(f'{counter}.Generated: {combo}')
                        counter += 1
                
                # Name + partial phone
                combo = f"{name_part}{sep}{clean_phone[-4:]}"
                if min_length <= len(combo) <= max_length:
                    wordlist.add(combo)
                    if display:
                        print(f'{counter}.Generated: {combo}')
                        counter += 1
                
                # Phone + name
                combo = f"{clean_phone}{sep}{name_part}"
                if min_length <= len(combo) <= max_length:
                    wordlist.add(combo)
                    if display:
                        print(f'{counter}.Generated: {combo}')
                        counter += 1
    
    # Add number suffixes
    base_words = list(wordlist)
    for word in base_words:
        for suffix in number_suffixes:
            new_word = word + suffix
            if min_length <= len(new_word) <= max_length:
                wordlist.add(new_word)
                if display:
                        print(f'{counter}.Generated: {new_word}')
                        counter += 1
    
    # Leet speak substitutions (basic)
    leet_words = set()
    leet_subs = {
        'a': ['@', '4'],
        'e': ['3'],
        'i': ['!', '1'],
        'o': ['0'],
        's': ['$', '5'],
        't': ['7'],
        'b': ['8'],
        'g': ['9']
    }
    
    for word in wordlist:
        # Generate leet variations
        leet_variations = [word]
        
        # For each character that has leet substitutions, create variations
        for char, substitutes in leet_subs.items():
            new_variations = []
            for variation in leet_variations:
                if char in variation:
                    for sub in substitutes:
                        new_variations.append(variation.replace(char, sub))
            leet_variations.extend(new_variations)
        
        # Add all variations that meet length requirements
        for variation in leet_variations:
            if variation != word and min_length <= len(variation) <= max_length:
                leet_words.add(variation)
    
    if display:
        for lw in leet_words:
            if lw not in wordlist:
                print(f'{counter}.Generated: {lw}')
                counter += 1
    wordlist.update(leet_words)
    
    # Case variations (first letter uppercase, all uppercase, etc.)
    case_variations = set()
    for word in wordlist:
        # Skip if it's already all digits
        if not word.isdigit():
            # First letter uppercase if not already
            if word and word[0].islower():
                case_variations.add(word.capitalize())
            
            # All uppercase
            case_variations.add(word.upper())
            
            # Toggle case
            toggle_case = ''.join(c.upper() if c.islower() else c.lower() for c in word)
            case_variations.add(toggle_case)
    
    if display:
        for cv in case_variations:
            if cv not in wordlist:
                print(f'{counter}.Generated: {cv}')
                counter += 1
    wordlist.update(case_variations)

    
    return sorted(wordlist)

def main():
    print('\n\nRaven Wordlist Generator')
    print(banner)
    parser = argparse.ArgumentParser(description='Generate a custom wordlist based on personal information', prog='raven-wg.py', epilog='Use only for ethical purposes')
    parser.add_argument('-f', '--firstname', required=True, help='First name of target. Example: john', metavar='firstname', )
    parser.add_argument('-l', '--lastname', help='Last name of target. Example: smith', metavar='lastname')
    parser.add_argument('-b', '--birthday', help='Birthday in YYYY-MM-DD format. Example: 1968-9-25', metavar='YYYY-MM-DD')
    parser.add_argument('-n', '--nationalid', help='National ID number of target. Example: 1456487941', metavar='integer')
    parser.add_argument('-p', '--phone', help='Phone number of target. Example: 447911124456', metavar='integer')
    parser.add_argument('--family', help='Family members (comma separated). Example: alice,james', metavar='name1,name2')
    parser.add_argument('-i', '--info', help='Other info (comma separated). Example: barcelna,messi', metavar='info1,info2')
    parser.add_argument('-o', '--output', default='wordlist.txt', help='Output file name.', metavar='output')
    parser.add_argument('--min', type=int, default=4, help='Minimum password length.', metavar='integer')
    parser.add_argument('--max', type=int, default=8, help='Maximum password length.', metavar='integer')
    parser.add_argument('-d', '--display', const=True, nargs='?', default=False, help='Print generated words in terminal.')
    
    args = parser.parse_args()
    
    print("Generating wordlist...")
    wordlist = generate_wordlist(
        args.firstname, 
        args.lastname, 
        args.birthday, 
        args.nationalid,
        args.phone,
        args.family,
        args.info,
        args.min, 
        args.max,
        args.display
    )
    
    # Write to file
    with open(args.output, 'w') as f:
        for word in wordlist:
            f.write(f"{word}\n")
    
    print(f"\nGenerated {len(wordlist)} words. Saved to {args.output}")

if __name__ == "__main__":
    main()