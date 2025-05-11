from PIL import Image
import random
import math

class BlumBlumShub:
    def __init__(self, seed, p=0, q=0):
        # Ham kiem tra so nguyen to

        # Ham kiem tra so nguyen to Blum
     

        if p == 0 or q == 0:
            self.p = 30091
            self.q = 41227
        else:
            self.p = p
            self.q = q

        # Kiem tra p va q co phai la so nguyen to hay khong

        self.M = self.p * self.q
        self.state = seed % self.M

    def next_bit(self):
        self.state = (self.state * self.state) % self.M
        return self.state % 2

    def next_int(self, max_val):
        bits = []
        for _ in range(int(math.log2(max_val)) + 1):
            bits.append(self.next_bit())
        return int(''.join(map(str, bits)), 2) % max_val


def hide_message(image_path, message, output_path, seed):
    img = Image.open(image_path)

    # Chuyen doi anh sang RGB neu can thiet
    if img.mode != 'RGB':
        img = img.convert('RGB')

    pixels = img.load()
    width, height = img.size

    binary_message = ''.join(format(byte, '08b') for byte in message.encode('utf-8'))
    binary_message += '00000000'

    if len(binary_message) > width * height:  # Chi su dung 1 kenh
        raise ValueError("Message too long to hide in image")

    bbs = BlumBlumShub(seed)
    pixel_indices = list(range(width * height))
    random_pixels = []

    for _ in range(len(binary_message)):
        idx = bbs.next_int(len(pixel_indices))
        random_pixels.append(pixel_indices.pop(idx))

    index = 0
    for pixel_idx in random_pixels:
        x = pixel_idx % width
        y = pixel_idx // width
        r, g, b = pixels[x, y]
        r = (r & 0xFE) | int(binary_message[index])
        pixels[x, y] = (r, g, b)
        index += 1

    img.save(output_path)
    print(f"Message hidden successfully in {output_path}")


if __name__ == "__main__":
    image_path = "deadpool.png"
    output_path = "stego.png"
    message = "This is a secret message!"
    seed = 987654321
    hide_message(image_path, message, output_path, seed)
