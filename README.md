## `brawlrating` ##

Python utility that calculates total rating for the cards in the 99 of Brawl decks.

Decklists are taken from the system clipboard: export your deck in arena, and then run `brawlrating`.

Before using, install `pyperclip` via `pip`:

    $ pip install pyperclip

Then just export a deck and run the utility.

    $ brawlrating
    Commander: Professor Onyx
    Commander weight: 360.0

    Cards in the 99:
    Count | Weight | Card
    ------+--------+-----
         1|    0.0|Gate of the Black Dragon
         1|    0.0|Cabal Stronghold
         1|    0.0|Demolition Field
         1|    0.0|Barren Moor
         1|    0.0|Detection Tower
        22|    0.0|Snow-Covered Swamp
         1|    0.0|Field of Ruin
         1|    9.0|Takenuma, Abandoned Mire
         1|    9.0|Arcane Signet
         1|    9.0|Skyclave Relic
         1|    9.0|Replicating Ring
         1|    9.0|Bojuka Bog
         1|    9.0|A-The One Ring
         1|    9.0|Feed the Swarm
         1|    9.0|Bone Shards
         1|    9.0|Insatiable Avarice
         1|    9.0|Whisper of the Dross
         1|    9.0|Go for the Throat
         1|    9.0|Blood Pact
         1|    9.0|Crawling Barrens
         1|    9.0|Mishra's Foundry
         1|    9.0|Reliquary Tower
         1|    9.0|Primal Amulet
         1|    9.0|Bitter Triumph
         1|   18.0|Liliana's Triumph
         1|   18.0|Pilfer
         1|   18.0|Dreams of Steel and Oil
         1|   18.0|Vraska, Betrayal's Sting
         1|   18.0|Coldsteel Heart
         1|   18.0|Guardian Idol
         1|   18.0|Key to the Archive
         1|   18.0|Hedron Archive
         1|   18.0|Pharika's Libation
         1|   18.0|The Cruelty of Gix
         1|   18.0|Pelakka Predation
         1|   18.0|Karn's Bastion
         1|   18.0|Labyrinth of Skophos
         1|   18.0|Yahenni's Expertise
         1|   27.0|Hive of the Eye Tyrant
         1|   27.0|Mind Spike
         1|   27.0|Agonizing Remorse
         1|   27.0|Check for Traps
         1|   27.0|Beseech the Mirror
         1|   27.0|Mox Amber
         1|   27.0|The Celestus
         1|   27.0|Hero's Downfall
         1|   27.0|Eat to Extinction
         1|   27.0|Shambling Ghast
         1|   27.0|Infernal Grasp
         1|   27.0|Power Word Kill
         1|   27.0|Hagra Mauling
         1|   27.0|Painful Bond
         1|   27.0|Crux of Fate
         1|   27.0|Liliana, Dreadhorde General
         1|   27.0|Ugin, the Ineffable
         1|   36.0|Phyrexian Arena
         1|   36.0|Mind Stone
         1|   36.0|Staff of Compleation
         1|   36.0|Erebos's Intervention
         1|   36.0|Vraska's Contempt
         1|   36.0|The Eldest Reborn
         1|   36.0|Baleful Mastery
         1|   36.0|Black Market Connections
         1|   36.0|Ritual of Soot
         1|   36.0|Lolth, Spider Queen
         1|   45.0|Thoughtseize
         1|   45.0|Castle Locthwain
         1|   45.0|March of Wretched Sorrow
         1|   45.0|Liliana of the Veil
         1|   45.0|Murderous Rider
         1|   45.0|Invoke Despair
         1|   45.0|Doom Blade
         1|   45.0|Heartless Act
         1|   45.0|Blood on the Snow
         1|   45.0|Sorin the Mirthless
         1|   45.0|Faceless Haven
         1|   45.0|Dark Ritual
         1|   45.0|Necropotence

    Total mainboard weight: 1809.0
    Total deck weight including commander: 2169.0

Ratings are based on [those collected by redditor schlarpc][1].

Commander ratings are from [a second spreadsheet][2], mentioned in a comment by schlarpc on the reddit post.

1: https://www.reddit.com/r/MagicArena/comments/1d0pih7/spreadsheet_of_card_weights_for_brawl/
2: https://docs.google.com/spreadsheets/d/1NUxfvRGw_dofRmduo9lrvH5oUhqj4I6G1QsqhZvRL20/edit#gid=0
