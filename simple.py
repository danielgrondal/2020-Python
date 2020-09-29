

def take_turn(game_layer):
    # TODO Implement your artificial intelligence here.
    # TODO Take one action per turn until the game ends.
    # TODO The following is a short example of how to use the StarterKit

    game_state = game_layer.game_state

    temps = [r.temperature for r in game_state.residences]
    print("Temp: " + str(temps))

    if maintain(game_layer, game_state):
        return

    if adjust_temp(game_layer, game_state):
        return

    if build(game_layer):
        return

    if build_utility():
        return

    game_layer.wait()

    for message in game_layer.game_state.messages:
        print(message)
    for error in game_layer.game_state.errors:
        print("Error: " + error)

     
def maintain(game_layer, game_state):

    if len(game_state.residences) == 0:
        return False

    did_maint = False
    for res in game_state.residences:
        if res.build_progress == 100:
            if res.health < 60 and game_state.funds > 150:
                game_layer.maintenance((res.X, res.Y))
                did_maint = True

    return did_maint

     
def adjust_temp(game_layer, game_state):

    if len(game_state.residences) == 0:
        return False

    did_maint = False
    for res in game_state.residences:
        if res.build_progress == 100:
            if res.temperature < 20 and game_state.funds > 150:
                did_maint = True
                blueprint = game_layer.get_residence_blueprint(res.building_name)
                # newTemp = indoorTemp + (effectiveEnergyIn - baseEnergyNeed) * degreesPerExcessMwh + degreesPerPop * currentPop - (indoorTemp - outdoorTemp) * emissivity
                #21 = res.temperature + (energy-blueprint.base_energy_need)*blueprint.degreesPerExcessMwh + blueprint.degreesPerPop - (res.temperature - game_state.current_temp)*blueprint.emissivity;
                energy = ((21 - game_state.current_temp - 0.04*res.current_pop) / 2) + blueprint.base_energy_need
                #energy = blueprint.base_energy_need + 0.5 + (res.temperature - game_state.current_temp) * blueprint.emissivity / 1 - res.current_pop * 0.04
                
                game_layer.adjust_energy_level((res.X, res.Y), energy)

            elif res.temperature > 24 and game_state.funds > 150:
                did_maint = True
                blueprint = game_layer.get_residence_blueprint(res.building_name)
                energy = blueprint.base_energy_need - 0.5 \
                        + (res.temperature - game_state.current_temp) * blueprint.emissivity / 1 \
                        - res.current_pop * 0.04
                game_layer.adjust_energy_level((res.X, res.Y), energy)

    return did_maint


def find_free_slot(state):
    x = -1
    y = -1
    for i in range(len(state.map)):
        for j in range(len(state.map)):
            if state.map[i][j] == 0:
                x = i
                y = j
                state.map[i][j] = 1
                break
    return x,y

def select_building(game_layer):
    for b in game_layer.game_state.available_residence_buildings:
        blueprint = game_layer.get_residence_blueprint(b.building_name)
        if blueprint.release_tick <= game_layer.game_state.turn:
            return b.building_name
    return ""

def build(game_layer):

    state = game_layer.game_state

    if len(state.residences) == 0:
        coords = find_free_slot(state)
        if coords != (-1,-1):
            name = select_building(game_layer)
            if name != "":
                game_layer.place_foundation(coords, name)
                return True

    for res in state.residences:
        if res.build_progress < 100:
            game_layer.build((res.X, res.Y))
            return True

    if (state.housing_queue > 10):
        coords = find_free_slot(state)
        if coords != (-1,-1):
            name = select_building(game_layer)
            if name != "":
                game_layer.place_foundation(coords, name)
                return True

    return False    

def build_utility():
    False


    # state = game_layer.game_state
    # x = 0
    # y = 0
    # if len(state.residences) < 2:
    #     for i in range(len(state.map)):
    #         for j in range(len(state.map)):
    #             if state.map[i][j] == 0:
    #                 x = i
    #                 y = j
    #                 break
    #     game_layer.place_foundation((x, y), game_layer.game_state.available_residence_buildings[0].building_name)
    #     # Save building position to map (occupied)
    #     state.map[x][y] = 1
    # elif len(state.utilities) < 2:
    #     for i in range(len(state.map)):
    #         for j in range(len(state.map)):
    #             if state.map[i][j] == 0:
    #                 x = i
    #                 y = j
    #                 break
    #     state.map[x][y] = 1
    #     game_layer.place_foundation((x, y), game_layer.game_state.available_utility_buildings[0].building_name)
    # else:
    #     for the_only_residence in state.residences:
    #         #the_only_residence = state.residences[0]
    #         if the_only_residence.build_progress < 100:
    #             game_layer.build((the_only_residence.X, the_only_residence.Y))
    #         elif the_only_residence.health < 45:
    #             game_layer.maintenance((the_only_residence.X, the_only_residence.Y))
    #         elif the_only_residence.temperature < 18:
    #             blueprint = game_layer.get_residence_blueprint(the_only_residence.building_name)
    #             energy = blueprint.base_energy_need + 0.5 \
    #                     + (the_only_residence.temperature - state.current_temp) * blueprint.emissivity / 1 \
    #                     - the_only_residence.current_pop * 0.04
    #             game_layer.adjust_energy_level((the_only_residence.X, the_only_residence.Y), energy)
    #         elif the_only_residence.temperature > 24:
    #             blueprint = game_layer.get_residence_blueprint(the_only_residence.building_name)
    #             energy = blueprint.base_energy_need - 0.5 \
    #                     + (the_only_residence.temperature - state.current_temp) * blueprint.emissivity / 1 \
    #                     - the_only_residence.current_pop * 0.04
    #             game_layer.adjust_energy_level((the_only_residence.X, the_only_residence.Y), energy)
    #         elif state.available_upgrades[0].name not in the_only_residence.effects:
    #             game_layer.buy_upgrade((the_only_residence.X, the_only_residence.Y), state.available_upgrades[0].name)
    #         else:
    #             game_layer.wait()
    # for message in game_layer.game_state.messages:
    #     print(message)
    # for error in game_layer.game_state.errors:
    #     print("Error: " + error)