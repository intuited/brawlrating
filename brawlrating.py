from re import compile as re_compile
from collections import namedtuple, defaultdict
from test_data import sample_decklist
Card = namedtuple('Card', ('id', 'name', 'set', 'weight'))
Deckline = namedtuple('Deckline', ('count', 'card'))

def DEBUG(s):
    print('\n'.join([f"DEBUG: {l}" for l in s.split('\n')]))

def read_tsv(filename):
    with open(filename) as f:
        firstline = f.readline()
        typify = lambda i,n,s,w: [int(i), n, s, int(w)]
        return [Card(*typify( *line.rstrip().split("\t") )) for line in f]
db = read_tsv('weights.tsv')
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
card_weights = compile_weights(db)

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
    """
    DEBUG(f"parse_line {line=}")
    match = deck_re.match(line)
    if not match:
        raise Exception(f"parse_line: deck_re failed to match line \"{line}\".")
    return Deckline(int(match.groupdict()['count']),
                    Card(id=None,
                         name=match.groupdict()['name'],
                         set=match.groupdict()['set'],
                         weight=None) )

# def db_lookup(name):
#     """ Look up a card in the DB by name.  Returns all matching cards in a list.
#     >>> db_lookup('Aven Mindcensor')
#     [Card(id=73777, name='Aven Mindcensor', set='AKR', weight=9)]
#     >>> db_lookup('Witch-king of Angmar')
#     [Card(id=84806, name='Witch-king of Angmar', set='LTR', weight=27)]
#     >>> db_lookup('Liliana, Dreadhorde General')
#     [Card(id=69548, name='Liliana, Dreadhorde General', set='WAR', weight=27)]
#     >>> len(db_lookup('Swamp'))
#     153
#     """
#     return [card for card in db if card.name == name]

def parse_decklist(decklist):
    mainboard = decklist.split('\n')[4:] # lines 1-4 are "Commander", the commander, an empty line, and "Deck"
    return [parse_line(line) for line in mainboard]

def print_card_weights(decklist):
    print('Count | Weight | Card')
    print('------+--------+-----')
    total_weight = 0
    for line in decklist:
        #DEBUG(f"print_card_weights: {line=}")
        #DEBUG(f"print_card_weights:     {line.card=}")
        #DEBUG(f"{card_weights=}")
        weight = card_weights[line.card.name]
        print(f"{line.count:6}|{weight:7}|{line.card.name}")
        total_weight += line.count * weight
    print('')
    print(f'Total card weight: {total_weight}')

if __name__ == "__main__": 
    decklist = parse_decklist(sample_decklist)
    print_card_weights(decklist)
