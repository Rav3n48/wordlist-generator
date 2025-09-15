import argparse
from datetime import datetime
import math
from itertools import permutations, combinations, chain

banner = """\n\n\n\n\nooooooooo.         .o.       oooooo     oooo oooooooooooo ooooo      ooo
`888   `Y88.      .888.       `888.     .8'  `888'     `8 `888b.     `8'
 888   .d88'     .8"888.       `888.   .8'    888          8 `88b.    8
 888ooo88P'     .8' `888.       `888. .8'     888oooo8     8   `88b.  8
 888`88b.      .88ooo8888.       `888.8'      888    "     8     `88b.8
 888  `88b.   .8'     `888.       `888'       888       o  8       `888
o888o  o888o o88o     o8888o       `8'       o888ooooood8 o8o        `8\n\n\n\n\n"""

def generate_wordlist(first_name=None, last_name=None, birthday=None, national_id=None, phone_number=None, 
                     family_members=None, other_info=None, min_length=4, max_length=8, max_words=None, display=None):
    """Generate a wordlist based on extensive personal information."""
    # Safety cap to avoid insane explosion. Increase with caution.
    maximum_combinations = max_words

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

    #helpers
    def clean_number(s):
        return s.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')

    def limit_and_add(s):
        nonlocal counter
        if s is None:
            return
        if max_words and len(wordlist) >= max_words:
            return
        if min_length <= len(s) <= max_length:
            if s not in wordlist:
                wordlist.add(s)
                if display and not maximum_combinations:
                    print(f'{counter}.Generated: {s}')
                    counter += 1

    def interleave_two(a, b):
        """
        Yield all interleavings of strings a and b preserving internal order.
        If the number of combinations exceeds maximum_combinations, return [].
        """
        n, m = len(a), len(b)
        total = n + m
        try:
            combos = math.comb(total, n)
        except Exception:
            combos = float('inf')
        if maximum_combinations:
            if combos > maximum_combinations:
                # skip full interleaving to avoid explosion
                return []

        results = []

        # iterative stack-based generation to avoid recursion depth issues
        stack = [(0, 0, [])]  # (i in a, j in b, built list of chars)
        while stack:
            i, j, built = stack.pop()
            if i == n and j == m:
                results.append(''.join(built))
                continue
            # choose from a
            if i < n:
                stack.append((i+1, j, built + [a[i]]))
            # choose from b
            if j < m:
                stack.append((i, j+1, built + [b[j]]))
        return results

    def all_concatenations(tokens, seps=['']):
        """Return concat variants of tokens with separators in between (single sep)."""
        outputs = []
        # tokens is list of strings
        for perm in permutations(tokens):
            # try separators between tokens
            for sep in seps:
                outputs.append(sep.join(perm))
        return outputs

    # leet substitutions map (kept as in original but can be extended)
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

    separators = ['', '.', '-', '_']
    number_suffixes = ['!', '@', '#', '$', '%', '&', '*', '123', '1', '007', '69', '1234', '000']

    # Collect tokens
    alpha_tokens = []   # pure or mostly alphabetic tokens (names, family, etc.)
    numeric_tokens = []  # pure-digit tokens (phone parts, national id, date parts)
    mixed_tokens = []   # tokens that contain both letters and digits

    # First name (guaranteed required by parser)
    if first_name:
        alpha_tokens.extend([first_name.lower(), first_name.capitalize()])
        # also split name into small chunks (e.g. 'er' 'fan') for extra mixing possibilities
        if len(first_name) >= 4:
            # add some substrings to increase permutations (prefixes/suffixes)
            fname = first_name.lower()
            alpha_tokens.append(fname[:3])
            alpha_tokens.append(fname[-3:])

    # Last name
    if last_name:
        alpha_tokens.extend([last_name.lower(), last_name.capitalize()])

    # Family members
    family_list = []
    if family_members:
        for member in family_members.split(','):
            member = member.strip()
            if not member:
                continue
            alpha_tokens.extend([member.lower(), member.capitalize()])
            family_list.extend([member.lower(), member.capitalize()])

    # Other info: can contain words and numbers. Split into tokens.
    other_tokens = []
    if other_info:
        for token in other_info.split(','):
            token = token.strip()
            if not token:
                continue
            other_tokens.append(token)
            if token.isdigit():
                numeric_tokens.append(clean_number(token))
            elif any(ch.isdigit() for ch in token):
                mixed_tokens.append(token)
            else:
                alpha_tokens.extend([token.lower(), token.capitalize()])

    # Birthday parsing (same as original)
    year = year_short = month = day = month_padded = day_padded = None
    if birthday:
        try:
            birth_date = datetime.strptime(birthday, "%Y-%m-%d")
            year = str(birth_date.year)
            year_short = year[2:]
            month = str(birth_date.month)
            day = str(birth_date.day)
            month_padded = month.zfill(2)
            day_padded = day.zfill(2)
            date_parts = [
                year, year_short, month, day, month_padded, day_padded,
                month + day, day + month, month_padded + day_padded, day_padded + month_padded,
                year_short + month, year_short + day, month + year_short, day + year_short
            ]
            for dp in date_parts:
                if dp.isdigit():
                    numeric_tokens.append(dp)
                else:
                    # fallback
                    alpha_tokens.append(dp)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return []

    # National ID
    if national_id:
        nid_clean = clean_number(national_id)
        numeric_tokens.extend([nid_clean, nid_clean[-4:], nid_clean[:4], nid_clean[-6:], nid_clean[:6]])

    # Phone number
    if phone_number:
        clean_phone = clean_number(phone_number)
        numeric_tokens.extend([clean_phone, clean_phone[-4:], clean_phone[-6:], clean_phone[:3]])

    # Mixed tokens (retain)
    for t in mixed_tokens:
        mixed_tokens.append(t.lower())
        mixed_tokens.append(t.capitalize())

    # Add alpha tokens derived from earlier collected lists
    # Deduplicate
    alpha_tokens = list(dict.fromkeys([t for t in alpha_tokens if t]))
    numeric_tokens = list(dict.fromkeys([t for t in numeric_tokens if t]))
    mixed_tokens = list(dict.fromkeys([t for t in mixed_tokens if t]))

    # Basic additions: each token alone if within length bounds
    for t in chain(alpha_tokens, numeric_tokens, mixed_tokens):
        limit_and_add(t)
    
    # Concatenate with separators for alpha tokens (first+last, first+family, etc.)
    name_pairs = []
    # If both first and last exist, add those combinations
    if first_name and last_name:
        name_pairs.append((first_name.lower(), last_name.lower()))
        name_pairs.append((first_name.capitalize(), last_name.capitalize()))
        name_pairs.append((last_name.lower(), first_name.lower()))

    # include combinations with family members (if any)
    for fam in family_list:
        name_pairs.append((first_name.lower(), fam))
        name_pairs.append((fam, first_name.lower()))

    for a, b in name_pairs:
        for sep in separators:
            limit_and_add(f"{a}{sep}{b}")

    # Interleavings between alpha token and numeric token
    # For each alpha token and each numeric token (and also for short concatenations of numeric tokens),
    # generate all interleavings preserving the order inside each token.
    # To be thorough, also try short concatenations/permutations of numeric tokens (up to 2 combined).
    numeric_pairs = list(numeric_tokens)
    # create combos of concatenated numeric tokens (single and pairs in both orders)
    concat_numeric_variants = set(numeric_pairs)
    for a, b in permutations(numeric_pairs, 2):
        # only create concatenations that are still reasonably short (<= max_length)
        cat = a + b
        if len(cat) <= max_length:
            concat_numeric_variants.add(cat)
    concat_numeric_variants = list(concat_numeric_variants)

    # For each alpha and each numeric concat variant, attempt interleaving
    for alpha in alpha_tokens:
        for num in concat_numeric_variants:
            # quick length pruning
            if len(alpha) + len(num) < min_length or len(alpha) + len(num) > max_length:
                # But interleavings might produce lengths equal to sum only; they won't change length.
                # So safe to skip if sum outside bounds.
                continue

            inters = interleave_two(alpha, num)
            if not inters:
                # if we couldn't interleave due to cap, fallback to concatenations with separators and placements
                for sep in separators:
                    limit_and_add(f"{alpha}{sep}{num}")
                    limit_and_add(f"{num}{sep}{alpha}")
                    # split numeric across two places (prefix/suffix)
                    if len(num) >= 2:
                        half = len(num)//2
                        a1, a2 = num[:half], num[half:]
                        limit_and_add(f"{alpha}{sep}{a1}{sep}{a2}")
                        limit_and_add(f"{a1}{sep}{alpha}{sep}{a2}")
                continue

            for s in inters:
                limit_and_add(s)
                # also add sep variants (in case separators were expected)
                for sep in separators:
                    # put separator in between the alpha and numeric segments if easy to detect (heuristic)
                    limit_and_add(s + sep)
                    limit_and_add(sep + s)

    # --- Interleavings between two alpha tokens (firstname <-> lastname, firstname <-> family) ---
    # This will mix letters of two names (e.g. e r f a n + s m i t h -> many combos)
    alpha_pairs = []
    if first_name and last_name:
        alpha_pairs.append((first_name.lower(), last_name.lower()))
        alpha_pairs.append((first_name.capitalize(), last_name.capitalize()))
    for fam in family_list:
        alpha_pairs.append((first_name.lower(), fam))

    for a, b in alpha_pairs:
        if len(a) + len(b) < min_length or len(a) + len(b) > max_length:
            # skip if sum outside final length constraints
            continue
        inters = interleave_two(a, b)
        if not inters:
            # fallback to simple concatenations
            for sep in separators:
                limit_and_add(f"{a}{sep}{b}")
                limit_and_add(f"{b}{sep}{a}")
            continue
        for s in inters:
            limit_and_add(s)
            for sep in separators:
                limit_and_add(f"{a}{sep}{b}")
                limit_and_add(f"{b}{sep}{a}")

    # Combine mixed tokens with others (simple concatenation & permutations)
    combined_tokens = alpha_tokens + numeric_tokens + mixed_tokens
    # take pairs and simple concatenations/permutations (keeps combinatorics reasonable)
    for a, b in permutations(combined_tokens, 2):
        concat = a + b
        if min_length <= len(concat) <= max_length:
            limit_and_add(concat)
        for sep in separators:
            s = f"{a}{sep}{b}"
            limit_and_add(s)

    # --- Add numeric suffixes to all base words (like original) ---
    base_words = list(wordlist)
    for word in base_words:
        for suffix in number_suffixes:
            new_word = word + suffix
            limit_and_add(new_word)

    # --- Leet speak expansions: for each generated word create variants ---
    leet_words = set()
    for word in list(wordlist):
        if len(word) < min_length or len(word) > max_length:
            continue
        variations = {word}
        # For each letter that has substitutions, create variations by replacing all occurrences
        for ch, subs in leet_subs.items():
            to_add = set()
            for var in list(variations):
                if ch in var.lower():
                    for sub in subs:
                        # do replacements in a case-insensitive manner preserving original case where possible
                        # simple approach: replace lowercase char and uppercase char separately
                        to_add.add(var.replace(ch, sub))
                        to_add.add(var.replace(ch.upper(), sub))
            variations.update(to_add)
        # filter and add
        for v in variations:
            if v != word and min_length <= len(v) <= max_length:
                leet_words.add(v)
    if display and not maximum_combinations:
        for lw in leet_words:
            if lw not in wordlist:
                print(f'{counter}.Generated: {lw}')
                counter += 1
    wordlist.update(leet_words)

    # Case variations
    case_variations = set()
    for w in list(wordlist):
        if w.isdigit():
            continue
        if w and w[0].islower():
            cap = w.capitalize()
            if min_length <= len(cap) <= max_length:
                case_variations.add(cap)
        upper = w.upper()
        if min_length <= len(upper) <= max_length:
            case_variations.add(upper)
        # toggle case
        toggle_case = ''.join(c.upper() if c.islower() else c.lower() for c in w)
        if min_length <= len(toggle_case) <= max_length:
            case_variations.add(toggle_case)

    if display and not maximum_combinations:
        for cv in case_variations:
            if cv not in wordlist:
                print(f'{counter}.Generated: {cv}')
                counter += 1
    wordlist.update(case_variations)

    if maximum_combinations:
        for i in sorted(wordlist)[:max_words]:
            print(f'{counter}.Generated: {i}')
            counter += 1

    return sorted(wordlist)[:max_words] if max_words else sorted(wordlist)



def main():
    print('\n\nRaven Wordlist Generator')
    print(banner)
    parser = argparse.ArgumentParser(description='Generate a custom wordlist based on personal information', prog='raven-wg.py', epilog='Use only for ethical purposes')
    parser.add_argument('-f', '--firstname', help='First name of target. Example: john', metavar='firstname', )
    parser.add_argument('-l', '--lastname', help='Last name of target. Example: smith', metavar='lastname')
    parser.add_argument('-b', '--birthday', help='Birthday in YYYY-MM-DD format. Example: 1968-9-25', metavar='YYYY-MM-DD')
    parser.add_argument('-n', '--nationalid', help='National ID number of target. Example: 1456487941', metavar='national id')
    parser.add_argument('-p', '--phone', help='Phone number of target. Example: 447911124456', metavar='phone number')
    parser.add_argument('--family', help='Family members (comma separated). Example: alice,james', metavar='member1,member2')
    parser.add_argument('-i', '--info', help='Other info (comma separated). Example: barcelona,messi', metavar='info1,info2')
    parser.add_argument('-o', '--output', default='wordlist.txt', help='Output file name.', metavar='filename')
    parser.add_argument('--min', type=int, default=4, help='Minimum password length.', metavar='integer')
    parser.add_argument('--max', type=int, default=8, help='Maximum password length.', metavar='integer')
    parser.add_argument('-m', '--max_words', type=int, default=None, help='Maximum number of words to be generated.', metavar='maximum words')
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
        args.max_words,
        args.display
    )
    
    # Write to file
    with open(args.output, 'w') as f:
        for word in wordlist:
            f.write(f"{word}\n")
    
    print(f"\nGenerated {len(wordlist)} words. Saved to {args.output}")

if __name__ == "__main__":
    main()