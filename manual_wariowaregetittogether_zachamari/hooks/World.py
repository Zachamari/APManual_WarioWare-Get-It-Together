# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState, Item

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem, item_name_groups
from ..Locations import ManualLocation, location_name_groups

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table, category_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value, format_state_prog_items_key, ProgItemsCat

# calling logging.info("message") anywhere below in this file will output the message to both console and log file
import logging

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the `filler_item_name` from game.json
def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool:
    return False

# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to remove locations from the world
    locationNamesToRemove: list[str] = [] # List of location names


    # Defining variables
    anycrew = "any"
    solocrew = "solo"
    crew3 = "crew of 3"
    crew5 = "crew of 5"
    allcrew = "all"
    crewsanity = "crewsanity"
    popIncluded = is_option_enabled(multiworld, player, "Include_PlayoPedia")
    popChecks = [] + get_option_value(multiworld, player, "PoP_Checks")
    crewmembers = ['Wario','18-Volt','Young Cricket','Mona','Dribble & Spitz','Dr. Crygor','9-Volt','Mike','Kat & Ana','Jimmy T','Ashley','Orbulon','5-Volt','Red','Master Mantis','Lulu','Penny','Pyoro']


    # Remove all non-included Play-o-Pedia checks from the locations list

    # The function counts all the way up bc if I don't have it do that, it adds the entire list of locations to locationNamesToRemove as a single string rather than a list, and the generator doesn't know what to do with that
    # I imagine there's a more efficient way to do this and that a skilled python programmer is shaking their head disapprovingly at my horribly unoptimized code
    if popIncluded:
        if anycrew not in popChecks:
            count = 0
            while count <= 221:
                locationNamesToRemove.append(location_name_groups["Play-o-Pedia Any"][count])
                count += 1
        if allcrew not in popChecks:
            count = 0
            while count <= 221:
                locationNamesToRemove.append(location_name_groups["Play-o-Pedia All Crew"][count])
                count += 1
        if solocrew not in popChecks:
            count = 0
            while count <= 221:
                locationNamesToRemove.append(location_name_groups["Play-o-Pedia Any Solo Crew"][count])
                count += 1
        if crew3 not in popChecks:
            count = 0
            while count <= 221:
                locationNamesToRemove.append(location_name_groups["Play-o-Pedia Crew of 3"][count])
                count += 1
        if crew5 not in popChecks:
            count = 0
            while count <= 221:
                locationNamesToRemove.append(location_name_groups["Play-o-Pedia Crew of 5"][count])
                count += 1
        if crewsanity not in popChecks:
            for crew in crewmembers:
                if crew not in popChecks:
                    count = 0
                    while count <= 221:
                        locationNamesToRemove.append(location_name_groups['Play-o-Pedia Crewsanity - ' + crew][count])
                        count += 1

    warioCupDifficulty = get_option_value(multiworld, player, "Include_Wario_Cup")

    if warioCupDifficulty == 0:
        count = 0
        while count <= 51:
            locationNamesToRemove.append(location_name_groups["Wario Cup"][count])
            locationNamesToRemove.append(location_name_groups["Wario Cup Gold"][count])
            count += 1

    if warioCupDifficulty == 1:
        count = 0
        while count <= 51:
            locationNamesToRemove.append(location_name_groups["Wario Cup Gold"][count])
            count += 1


    varietyPackDifficulty = get_option_value(multiworld, player, "Include_Variety_Pack")

    if varietyPackDifficulty == 0:
        count = 0
        while count <= 3:
            locationNamesToRemove.append(location_name_groups["Variety Pack"][count])
            count += 1
        differentcount = 0  # I know this probably doesn't need to be a different variable but whatever, I'm superstitious
        while differentcount <= 2:
            locationNamesToRemove.append(location_name_groups["Variety Pack Expert"][differentcount])
            locationNamesToRemove.append(location_name_groups["Variety Pack Master"][differentcount])
            differentcount += 1

    if varietyPackDifficulty == 1:
        count = 0
        while count <= 2:
            locationNamesToRemove.append(location_name_groups["Variety Pack Expert"][count])
            locationNamesToRemove.append(location_name_groups["Variety Pack Master"][count])
            count += 1

    if varietyPackDifficulty == 2:
        count = 0
        while count <= 2:
            locationNamesToRemove.append(location_name_groups["Variety Pack Master"][count])
            count += 1


    chosenGoal = get_option_value(multiworld, player, "goal")

    if chosenGoal == 0:
        locationNamesToRemove.append("Anything Goes - Boss 1 Clear")
        locationNamesToRemove.append("Anything Goes - Boss 2 Clear")
        locationNamesToRemove.append("Anything Goes - Boss 3 Clear")


    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)



# This hook allows you to access the item names & counts before the items are created. Use this to increase/decrease the amount of a specific item in the pool
# Valid item_config key/values:
# {"Item Name": 5} <- This will create qty 5 items using all the default settings
# {"Item Name": {"useful": 7}} <- This will create qty 7 items and force them to be classified as useful
# {"Item Name": {"progression": 2, "useful": 1}} <- This will create 3 items, with 2 classified as progression and 1 as useful
# {"Item Name": {0b0110: 5}} <- If you know the special flag for the item classes, you can also define non-standard options. This setup
#       will create 5 items that are the "useful trap" class
# {"Item Name": {ItemClassification.useful: 5}} <- You can also use the classification directly
def before_create_items_all(item_config: dict[str, int|dict], world: World, multiworld: MultiWorld, player: int) -> dict[str, int|dict]:
    return item_config

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool



# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # Use this hook to remove items from the item pool
    itemNamesToRemove: list[str] = [] # List of item names

    # Add your code here to calculate which items to remove.
    #
    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.


    # Most of the following code was created by studying the code written by Axxroy for the Manual Rhythm Game Randomizer and by Squidy et al. for the SMO manual.
    # I did not know much python before this, so most of the credit for this code should go to them (although I did modify it heavily for my purposes)





    # Fetch the list of items with category 'Prezzies'. Big thanks to Silasary for showing me this function!
    prezzies = item_name_groups["Prezzies"]


    from random import randint

    itemNamesToAdd = []




    warioCupDifficulty = get_option_value(multiworld, player, "Include_Wario_Cup")
    warioCupUnlocks = get_option_value(multiworld, player, "Wario_Cup_Unlocks")

    if warioCupDifficulty == 0:
        count = 0
        while count <= 51:
            itemNamesToRemove.append(item_name_groups["Wario Cup Challenges"][count])
            count += 1
    else:
        if warioCupUnlocks == 0:
            count = 0
            while count <= 51:
                itemNamesToRemove.append(item_name_groups["Wario Cup Challenges"][count])
                count += 1



    varietyPackDifficulty = get_option_value(multiworld, player, "Include_Variety_Pack")
    varietyPackUnlocks = get_option_value(multiworld, player, "Variety_Pack_Unlocks")


    if varietyPackDifficulty == 0:
        count = 0
        while count <= 3:
            itemNamesToRemove.append(item_name_groups["Variety Pack Games"][count])
            count += 1
    else:
        if varietyPackUnlocks == 0:
            count = 0
            while count <= 3:
                itemNamesToRemove.append(item_name_groups["Variety Pack Games"][count])
                count += 1



    popUnlocks = get_option_value(multiworld, player, "PoP_Unlocks")
    popIncluded = is_option_enabled(multiworld, player, "Include_PlayoPedia")
    popChecks = [] + get_option_value(multiworld, player, "PoP_Checks")


    if popIncluded: 
        if popChecks:
            if popUnlocks == 0:
                count = 0
                while count <= 221:
                    itemNamesToRemove.append(item_name_groups["Individual Play-o-Pedia Games"][count])
                    count += 1
                differentcount = 0
                while differentcount <= 9:
                    itemNamesToRemove.append(item_name_groups["Play-o-Pedia Sections"][differentcount])
                    differentcount += 1
            if popUnlocks == 1:
                count = 0
                while count <= 221:
                    itemNamesToRemove.append(item_name_groups["Individual Play-o-Pedia Games"][count])
                    count += 1
            if popUnlocks == 2:
                count = 0
                while count <= 9:
                    itemNamesToRemove.append(item_name_groups["Play-o-Pedia Sections"][count])
                    count += 1

    # Special exception if popIncluded on but no values are present in PoP_Checks
    if popIncluded:
        if not popChecks:
            count = 0
            while count <= 221:
                itemNamesToRemove.append(item_name_groups["Individual Play-o-Pedia Games"][count])
                count += 1
            differentcount = 0
            while differentcount <= 9:
                itemNamesToRemove.append(item_name_groups["Play-o-Pedia Sections"][differentcount])
                differentcount += 1

    # Universal Tracker bypass
    if hasattr(multiworld, "generation_is_fake"):
        for itemName in itemNamesToRemove:
            item = next(i for i in item_pool if i.name == itemName)
            item_pool.remove(item)
        return item_pool
    # This just skips having to calc all the filler again



    # Fill all unfilled item slots with random Prezzies
    count = 1
    nothings = len(multiworld.get_unfilled_locations(player)) - (len(item_pool) - len(itemNamesToRemove))
    while (count <= nothings):
        cluckadepull = randint(0,99)
        itemNamesToAdd.append(prezzies[cluckadepull])
        count += 1

    # If there are no unfilled item slots, remove a random selection of them. 
    # (This is probably a stupid way to do it, but it makes the generator stop complaining, so whatevs)

    if nothings < 0:
        if nothings == (0 - 100): # In the event that there are exactly 0 non-progression item slots (exactly 100 filler), remove everything
            countup = 0
            while countup <= 99:
                prezzylist.append(prezzies[countup])
                countup += 1
        else:
            prezzylist = []
            countup = 0
            countdown = 0
            while countup <= 99:
                prezzylist.append(prezzies[countup])
                countup += 1
            while (countdown > nothings):
                cluckade = (randint(1, len(prezzylist)) - 1)
                prezzytoremove = prezzylist[cluckade]
                itemNamesToRemove.append(prezzytoremove)
                prezzylist.remove(prezzytoremove)
                countdown -= 1





    for itemName in itemNamesToRemove:
        item = next(i for i in item_pool if i.name == itemName)
        item_pool.remove(item)


    for itemName in itemNamesToAdd:
        item = next(i for i in item_pool if i.name == itemName)
        item_pool.append(item)



    return item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # item_pool.remove(item_to_place)

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location

    def Example_Rule(state: CollectionState) -> bool:
        # Calculated rules take a CollectionState object and return a boolean
        # True if the player can access the location
        # CollectionState is defined in BaseClasses
        return True

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is run every time an item is added to the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be cancelled/undone in after_remove_item
def after_collect_item(world: World, state: CollectionState, Changed: bool, item: Item):
    # the following let you add to the Potato Item Value count
    # if item.name == "Cooked Potato":
    #     state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "Potato")] += 1
    pass

# This method is run every time an item is removed from the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be first done in after_collect_item
def after_remove_item(world: World, state: CollectionState, Changed: bool, item: Item):
    # the following let you undo the addition to the Potato Item Value count
    # if item.name == "Cooked Potato":
    #     state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "Potato")] -= 1
    pass


# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass

# This is called when you want to add information to the hint text
def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:

    ### Example way to use this hook:
    # if player not in hint_data:
    #     hint_data.update({player: {}})
    # for location in multiworld.get_locations(player):
    #     if not location.address:
    #         continue
    #
    #     use this section to calculate the hint string
    #
    #     hint_data[player][location.address] = hint_string

    pass

def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    pass
