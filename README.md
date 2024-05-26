## `brawlrating` ##

Python utility that calculates total rating for the cards in the 99 of Brawl decks.

Decklists are taken from the system clipboard: export your deck in arena, and then run `brawlrating`.

Before using, install `pyperclip` via `pip`:

    $ pip install pyperclip

Ratings are based on [those collected by redditor schlarpc][1].

Commander ratings use the data from [this spreadsheet][2].

1: https://www.reddit.com/r/MagicArena/comments/1d0pih7/spreadsheet_of_card_weights_for_brawl/
2: https://docs.google.com/spreadsheets/d/1UKhHjCJ0bU0r2HLQV85usa3WnmdjNHW_9UTDXdPAutA/edit#gid=1412951292
