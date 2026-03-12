# WarioWare: Get It Together! Manual Archipelago Randomizer
This is a manual Archipelago integration for WarioWare: Get It Together!

# How to Play
This is a manual apworld, so the game itself remains unmodified and you must restrict yourself based on the items that you've received. You should only ever choose crew members and stages you have unlocked from the multiworld. 

This apworld was made with the latest stable release of Manual. For more information about Manual, check the repository here:

https://github.com/ManualForArchipelago/Manual

This manual assumes you are playing on a completed save file with all characters and story mode stages unlocked. If you have the Play-o-Pedia or Wario Cup enabled, you should also make sure you have all of the microgames/challenges unlocked beforehand. (Especially check that you have all Wario Cup challenges unlocked, as those are, to my knowledge, unlocked on a week-by-week basis starting from when you played the game for the first time, so it may take a while to unlock them all.)

Universal Tracker is recommended to help you know what you're able to do. You can get Universal Tracker here:

https://github.com/FarisTheAncient/Archipelago/releases/latest

# Goals
Both goals may be set to additionally require the 3 Golden Treasures in order to assemble the Golden Watering Can.
- Anything Goes - Clear the first boss of Wario Bug (Requires 5 crew members and Anything Goes)
- Showdown - Defeat Pyoro in Showdown after obtaining every Crew Member (except Pyoro) and Showdown

# Items
- Crew Members (18)
- Story Mode Stages (17)
- Prezzies (100 unique, filler)
  Optional:
  - Golden Treasures (3, required for goal if enabled)
  - Play-o-Pedia microgames (222) or sections of the Play-o-Pedia (10)
  - Wario Cup Challenges (52)
  - Variety Pack Minigames (4)

# Locations
- Clearing boss stages in Story Mode (3 per stage)
- Clearing certain scores in Story Mode levels without boss stages (i.e. All Mixed Up) (3 per stage)
  Optional:
  - Clearing the Target Score on every microgame in the Play-o-Pedia (222 per group enabled):
      - In any mode
      - With any solo crew member
      - With any crew of 3
      - With any crew of 5
      - With all crew members at once
      - Crewsanity: With each individual solo crew member (x18)
  - Clearing each Wario Cup Challenge with Bronze and Gold (52 each)
  - Playing (4) or reaching the Expert and Master Mission scores (3 each) in each Variety Pack minigame

# Notes and Known Issues
- Due to restrictions for certain symbols in json formatting, some microgames and challenges had to have their names slightly changed. Any names containing commas (,) or colons (:) had to have those characters removed. For consistency's sake, those characters are currently just straight-up missing and aren't replaced with anything.
- If Play-o-Pedia checks are set to require the individual microgames, generation slows down substantially due to the overly restrictive logic, especially if only one type of Play-o-Pedia check is included. To speed up generation in public games with this setting on, it's recommended to include at least two types of PoP checks (i.e. ['any','solo']). (For smaller multiworlds if you don't mind longer gen times, don't worry about it)
- "Look Both Ways" is the name of both a microgame and a Wario Cup Challenge. The challenge is called "Look Both Ways (Challenge)" while the microgame is just called "Look Both Ways".

# To Do
- Add a setting like Pokemon games' Trainersanity ranges for included Play-o-Pedia microgames, to allow more customizability in number of checks
- Possibly refine logic to prevent having to do difficult checks with horrible characters (i.e. Thrill Ride/Super Hard with 9-Volt/Kat in the party)
- Refine Variety Pack logic a bit, make proper logic for Daily Grind
    - Add per-character checks for Friendless Battle and Gotta Bounce
