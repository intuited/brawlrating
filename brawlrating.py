from re import compile as re_compile
from collections import namedtuple, defaultdict
import test_data
from os import path
import pyperclip
Card = namedtuple('Card', ('id', 'name', 'set', 'weight'))
Deckline = namedtuple('Deckline', ('count', 'card'))

def DEBUG(s):
    print('\n'.join([f"DEBUG: {l}" for l in s.split('\n')]))

def typify(id_, name, set_, weight):
    """Remove commas from numeric values and cast them to numeric types."""
    id_ = int(id_)
    weight = float(weight.replace(',', ''))
    return (id_, name, set_, weight)
def read_weights(filename):
    with open(filename) as f:
        firstline = f.readline()
        return [Card(*typify( *line.rstrip().split("\t") )) for line in f]
install_dir = path.dirname(__file__)
cmdr_db = read_weights(path.join(install_dir, 'commanderweights.tsv'))
card_db = read_weights(path.join(install_dir, 'weights.tsv'))

def compile_weights(db):
    """Builds a dictionary of card names to card weights from the DB.

    Raises an exception if any card entries with identical names
    have different weights.
    """
    cards_by_name = defaultdict(list)
    for card in db:
        cards_by_name[card.name].append(card)
    ret = {}
    for name, cards in cards_by_name.items():
        weights = [card.weight for card in cards]
        for w in weights:
            if w != weights[0] and name != '?':
                raise Exception(f"Card \"{name}\" has entries with different weights: {weights}")
        ret[name] = weights[0]
    return ret
card_weights = compile_weights(card_db)
cmdr_weights = compile_weights(cmdr_db)
def get_weight(name, cmdr=False):
    """Need to do extra processing for some split cards.

    Arena exports some split cards with two slashes, e.g. "Discovery // Dispersal",
    and others with three, e.g. 'Consign /// Oblivion'.

    The database uses two slashes for all of these cards.

    >>> get_weight('Discovery // Dispersal')
    27.0
    >>> get_weight('Consign /// Oblivion')
    27.0
    """
    db = cmdr_weights if cmdr else card_weights
    name = name.replace('///', '//')
    return db[name]

deck_re = re_compile(r'(?P<count>\d+) (?P<name>.*) \((?P<set>[A-Z0-9]{3})\) (?P<id>\d+)')
def parse_line(line):
    """Parse a decklist line into an list of cards.

    Cards are Card objects with `id` and `weight` set to None.

    >>> parse_line('1 Aven Mindcensor (AKR) 5')
    Deckline(count=1, card=Card(id=None, name='Aven Mindcensor', set='AKR', weight=None))
    >>> parse_line('1 Witch-king of Angmar (LTR) 114')
    Deckline(count=1, card=Card(id=None, name='Witch-king of Angmar', set='LTR', weight=None))
    >>> parse_line('1 Liliana, Dreadhorde General (WAR) 97')
    Deckline(count=1, card=Card(id=None, name='Liliana, Dreadhorde General', set='WAR', weight=None))
    >>> parse_line('8 Swamp (M21) 311')
    Deckline(count=8, card=Card(id=None, name='Swamp', set='M21', weight=None))
    >>> parse_line('1 Consign /// Oblivion (AKR) 230')
    Deckline(count=1, card=Card(id=None, name='Consign /// Oblivion', set='AKR', weight=None))
    """
    # DEBUG(f"parse_line {line=}")
    match = deck_re.match(line)
    if not match:
        raise Exception(f"parse_line: deck_re failed to match line \"{line}\".")
    return Deckline(int(match.groupdict()['count']),
                    Card(id=None,
                         name=match.groupdict()['name'],
                         set=match.groupdict()['set'],
                         weight=None) )

def parse_mainboard(decklist):
    mainboard = decklist.split('\n')[4:] # lines 1-4 are "Commander", the commander, an empty line, and "Deck"
    return [parse_line(line) for line in mainboard]

def parse_commander(decklist):
    return parse_line(decklist.split('\n')[1]).card # Commander is on the second line of the decklist

def print_card_weights(decklist):
    """Prints out a total weight for the deck as well as each contained card.

    >>> print_card_weights(test_data.teysa_oo) # doctest: +ELLIPSIS
    Commander: Teysa, Opulent Oligarch
    Commander weight: 9.0
    <BLANKLINE>
    Cards in the 99:
    Count | Weight | Card
    ------+--------+-----
         8|    0.0|Swamp
         8|    0.0|Plains
         1|    0.0|Plaza of Heroes
         1|    0.0|Isolated Chapel
    ...
         1|   45.0|Shadowspear
         1|   45.0|Emeria's Call
         1|   45.0|Agadeem's Awakening
         1|   45.0|Sheoldred, the Apocalypse
    <BLANKLINE>
    Total mainboard weight: 1797.0
    Total deck weight including commander: 1806.0

    >>> print_card_weights(test_data.onyx) # doctest: +ELLIPSIS
    Commander: Professor Onyx
    ...
    Total deck weight including commander: 2169.0

    >>> print_card_weights(test_data.saint_elenda) # doctest: +ELLIPSIS
    Commander: Saint Elenda
    ...
    Total deck weight including commander: 1449.0

    >>> print_card_weights(test_data.rankle) # doctest: +ELLIPSIS
    Commander: Rankle, Pitiless Trickster
    ...
         1|    9.0|Troll of Khazad-dûm
    ...
    Total deck weight including commander: 1656.0
    """
    commander = parse_commander(decklist)
    mainboard = parse_mainboard(decklist)
    commander_weight = get_weight(commander.name, True)

    print(f"Commander: {commander.name}")
    print(f"Commander weight: {commander_weight}")
    print()
    print("Cards in the 99:")
    print('Count | Weight | Card')
    print('------+--------+-----')
    mainboard_weight = 0
    WeightedCard = namedtuple('WeightedCard', ('count', 'weight', 'name'))
    weighted = (WeightedCard(line.count, get_weight(line.card.name), line.card.name)
                for line in mainboard)
    sorted_ = sorted(weighted, key=lambda i: i[1])
    for card in sorted_:
        print(f"{card.count:6}|{card.weight:7}|{card.name}")
        mainboard_weight += card.count * card.weight
    print()
    print(f'Total mainboard weight: {mainboard_weight}')
    print(f'Total deck weight including commander: {mainboard_weight + commander_weight}')

if __name__ == "__main__": 
    # Clipboard may contain Windows-encoded text under WSL?
    # I don't pretend to understand what was happening here
    # but this exception-handling code fixed the issue with pyperclip
    # that occurred when trying to import a decklist containing
    # Troll of Khazad=dûm (the Rankle deck that was also pasted into
    # test_data.py).
    try:
        decklist = pyperclip.paste()
    except UnicodeDecodeError:
        pyperclip.ENCODING = 'cp437'
        decklist = pyperclip.paste()
    print_card_weights(decklist.strip())
