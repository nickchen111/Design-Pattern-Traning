from .models import World, Hero, Fire, Water, Coord
import random


def main():
    # create world
    w = World(length=30)

    # create 10 unique positions
    positions = random.sample(range(0, 30), 10)
    sprites = []
    kinds = [Hero, Fire, Water]
    for i, pos in enumerate(positions):
        kind = random.choice(kinds)
        coord = Coord(pos=pos)
        if kind is Hero:
            sprites.append(Hero(coord=coord, hp=30))
        elif kind is Fire:
            sprites.append(Fire(coord=coord))
        else:
            sprites.append(Water(coord=coord))

    w._create(sprites)
    w._start_loop()


if __name__ == "__main__":
    main()
