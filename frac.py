import numpy as np
from PIL import Image
import matplotlib as mt
from datetime import datetime
import colorsys
import tweepy
import os

turbo = mt.colormaps.get_cmap("turbo")

def mandelbrot_escape_time(c, max_iter=100):
    z = 0
    for i in range(max_iter):
        z = z*z + c
        if abs(z) > 2:
            return i
    return max_iter

# gera um valor de c aleatório dentro de uma região daora do Mandelbrot
def random_c(min_escape=90, max_iter=100):
    while True:
        re = np.random.uniform(-1.5, 1.5)
        im = np.random.uniform(-1.5, 1.5)
        c = complex(re, im)
        escape = mandelbrot_escape_time(c, max_iter)
        if escape >= min_escape:
            return c

# gera a imagem

def gerar_fractal(c, width=2048, height=2048, max_iter=300):
    x_min, x_max = -1.5, 1.5
    y_min, y_max = -1.5, 1.5

    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    img = np.zeros((height, width, 3))

    for i in range(height):
        for j in range(width):
            z = Z[i, j]
            n = 0
            while abs(z) <= 4 and n < max_iter:
                z = z*z + c
                n += 1

            if n < max_iter:
                t = n / max_iter
                r, g, b, _ = turbo(t)
            else:
                r = g = b = 0

            img[i, j] = (r, g, b)

    return img

# salva imagem
def salvar_imagem(img_np, c):
    pasta = "fractais_julia"
    os.makedirs(pasta, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome = f"{pasta}/julia_{timestamp}_c_{c.real:+.4f}_{c.imag:+.4f}.png"
    
    # converte o array [0-1] para [0-255] e salva com Pillow
    img_uint8 = (img_np * 255).astype(np.uint8)
    image = Image.fromarray(img_uint8, mode='RGB')
    image.save(nome, quality=100, compress_level=0)
    return nome

# postar no Twitter 
# def postar_no_twitter(caminho_arquivo, c):
#     # Coloque suas credenciais da API aqui:
#     consumer_key = "SUA_CONSUMER_KEY"
#     consumer_secret = "SEU_CONSUMER_SECRET"
#     access_token = "SEU_ACCESS_TOKEN"
#     access_token_secret = "SEU_ACCESS_TOKEN_SECRET"

#     auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
#     api = tweepy.API(auth)

#     texto = f"Julia set, c = {c.real:.4f} + {c.imag:.4f}i #fractal #julia #mathart"
#     api.update_status_with_media(status=texto, filename=caminho_arquivo)

# executar
if __name__ == "__main__":
    c = random_c()
    print(f"Gerando fractal para c = {c}")
    img = gerar_fractal(c)
    caminho = salvar_imagem(img, c)
    print(f"Imagem salva em: {caminho}")
    # postar_no_twitter(caminho, c)
