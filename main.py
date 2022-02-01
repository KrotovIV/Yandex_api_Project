import pygame
import io
import requests

WIDTH = 360
HEIGHT = 480
FPS = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def input_params():
    with open('input.txt') as f:
        spisok = list(map(lambda x: x.strip(), f.readlines()))
    return tuple(spisok)


def make_params(coords, scale):
    params = {
        "ll": coords,
        "z": 10,
        "l": "map",
        "size": scale
    }
    return params


def get_image(params):
    api = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(api, params=params)
    img = io.BytesIO(response.content)
    return img


if __name__ == "__main__":
    pygame.init()

    WIDTH = 650
    HEIGHT = 450
    FPS = 30

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    coords, scale = input_params()
    params = make_params(coords, scale)
    content = get_image(params)

    image = pygame.image.load(content)
    image = pygame.transform.scale(image, (WIDTH, HEIGHT))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(image, image.get_rect())
        pygame.display.flip()
