import pygame
import io
import requests


def input_params():
    with open('input.txt') as f:
        coords, scale = list(map(lambda x: x.strip(), f.readlines()))
    return coords, scale


def make_params(coords, scale):
    params = {
        "ll": coords,
        "z": scale,
        "l": "map",
        "size": "650,450",
        "pt": "0.000000,55.000000~-0.390625,55.000000~0.390625,55.000000~0.000000,55.186035~0.000000,54.813965"
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

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    coords, scale = input_params()
    params = make_params(coords, scale)
    content = get_image(params)

    image = pygame.image.load(content)
    image = pygame.transform.scale(image, (WIDTH, HEIGHT))

    running = True
    while running:
        changed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_PAGEUP]:
                if int(scale) < 23:
                    scale = str(int(scale) + 1)
                    changed = True
            if keys[pygame.K_PAGEDOWN]:
                if int(scale) > 0:
                    scale = str(int(scale) - 1)
                    changed = True
            if keys[pygame.K_LEFT]:
                coords = ",".join([str(float(coords.split(',')[0]) - 800 / 2 ** int(scale)), coords.split(',')[1]])
                changed = True
                if abs(float(coords.split(',')[0])) > 180:
                    coords = ",".join([str(float(coords.split(',')[0]) + 800 / 2 ** int(scale)), coords.split(',')[1]])
                    changed = False
            if keys[pygame.K_RIGHT]:
                coords = ",".join([str(float(coords.split(',')[0]) + 800 / 2 ** int(scale)), coords.split(',')[1]])
                changed = True
                if abs(float(coords.split(',')[0])) > 180:
                    coords = ",".join([str(float(coords.split(',')[0]) - 800 / 2 ** int(scale)), coords.split(',')[1]])
                    changed = False
            if keys[pygame.K_UP]:
                coords = ",".join([coords.split(',')[0], str(float(coords.split(',')[1]) + 381 / 2 ** int(scale))])
                changed = True
                if abs(float(coords.split(',')[1])) > 90:
                    coords = ",".join([coords.split(',')[0], str(float(coords.split(',')[1]) - 381 / 2 ** int(scale))])
                    changed = False
            if keys[pygame.K_DOWN]:
                coords = ",".join([coords.split(',')[0], str(float(coords.split(',')[1]) - 381 / 2 ** int(scale))])
                changed = True
                if abs(float(coords.split(',')[1])) > 90:
                    coords = ",".join([coords.split(',')[0], str(float(coords.split(',')[1]) + 381 / 2 ** int(scale))])
                    changed = False
        if changed:
            params = make_params(coords, scale)
            content = get_image(params)

            image = pygame.image.load(content)
            image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        screen.blit(image, image.get_rect())
        pygame.display.flip()
