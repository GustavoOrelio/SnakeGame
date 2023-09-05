from Game import Game


def main_game():
    sprite_paths = {
        'head': 'img/snake_head.png',
        'body': 'img/snake_body.png',
        'cauda': 'img/snake_cauda.png',
        'curve_left': 'img/snake_curve.png',
        'curve_right': 'img/snake_curve_right.png'
    }
    game = Game(500, 20, sprite_paths)
    retry = game.play()
    print(f"Main game retry is {retry}")
    return retry


if __name__ == "__main__":
    retry = True
    while retry:
        print("Starting a new game")
        retry = main_game()
