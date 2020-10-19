# Run this scipt to have a quick visual check
# that your implementation is behaving as expected.

import random
import game_of_life as gol

def main():
    size = (7, 7)
    s = set()
    for _ in range(16):
        s.add((random.randint(0, size[0]-1), random.randint(0, size[1]-1)))

    for _ in range(10):
        print(gol.draw(s, size))
        print()

        s = gol.update(s, size, 1)
    print(gol.draw(s, size))

if __name__ == '__main__':
    main()
