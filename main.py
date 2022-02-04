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
        "size": "650,450"
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
    step = 0.008

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    coords, scale = input_params()
    coords1 = coords.split(',')
    coords1 = list(map(float, coords1))
    params = make_params(coords, scale)
    content = get_image(params)

    image = pygame.image.load(content)
    image = pygame.transform.scale(image, (WIDTH, HEIGHT))

    running = True
    while running:
        changed_scale = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                if int(scale) < 23:
                    scale = str(int(scale) + 1)
                    changed_scale = True
            if keys[pygame.K_DOWN]:
                if int(scale) > 0:
                    scale = str(int(scale) - 1)
                    changed_scale = True
            if keys[pygame.K_a]:
                coords1[0] -= step / (2 * int(scale) ** 0.5)
                changed_scale = True
            if keys[pygame.K_d]:
                coords1[0] += step / (2 * int(scale) ** 0.5)
                changed_scale = True
            if keys[pygame.K_w] and coords1[1] < 85:
                coords1[1] += step / (2 * int(scale) ** 0.5)
                changed_scale = True
            if keys[pygame.K_s] and coords1[1] > -85:
                coords1[1] -= step / (2 * int(scale) ** 0.5)
                changed_scale = True

            print(scale)
            print(coords1)
        if changed_scale:
            coords2 = ','.join(list(map(str, coords1)))
            params = make_params(coords2, scale)
            content = get_image(params)

            image = pygame.image.load(content)
            image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        screen.blit(image, image.get_rect())
        pygame.display.flip()

