import api
from game_layer import GameLayer
import simple

api_key = "fdeefade-dbbe-4b3f-8374-7563da254238"   # TODO: Your api key here
# The different map names can be found on considition.com/rules
map_name = "training1"  # TODO: You map choice here. If left empty, the map "training1" will be selected.

game_layer: GameLayer = GameLayer(api_key)


def main():
    game_layer.new_game(map_name)
    print("Starting game: " + game_layer.game_state.game_id)
    game_layer.start_game()
    while game_layer.game_state.turn < game_layer.game_state.max_turns:
        take_turn()
    print("Done with game: " + game_layer.game_state.game_id)
    print("Final score was: " + str(game_layer.get_score()["finalScore"]))

def take_turn():
    simple.take_turn(game_layer)


if __name__ == "__main__":
    main()
