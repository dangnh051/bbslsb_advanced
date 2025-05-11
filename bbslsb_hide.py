from PIL import Image
import random
import math

class BlumBlumShub:
    def __init__(self, seed, p=0, q=0):
        # Hàm kiểm tra số nguyên tố
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    return False
            return True
        
        # Hàm kiểm tra số nguyên tố Blum
        def is_blum_prime(n):
            return is_prime(n) and n % 4 == 3
        
        if p == 0 or q == 0:
            self.p = 30091
            self.q = 41227
        else:
            self.p = p
            self.q = q
        
        # Kiểm tra p và q có phải là số nguyên tố Blum
        if not (is_blum_prime(self.p) and is_blum_prime(self.q)):
            raise ValueError("p and q must be Blum primes (primes congruent to 3 mod 4)")
        
        self.n = self.p * self.q
        self.state = seed % self.n
    
    def next_bit(self):
        self.state = pow(self.state, 2, self.n)
        return self.state % 2

def hide_message(image_path, message, output_path, seed):
    img = Image.open(image_path)
    
    # Chuyển đổi ảnh sang RGB nếu cần thiết
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    pixels = img.load()
    width, height = img.size
    
    binary_message = ''.join(format(byte, '08b') for byte in message.encode('utf-8'))
    binary_message += '00000000'  # Null terminator
    
    if len(binary_message) > width * height * 3: 
        raise ValueError("Message too long to hide in image")
    
    bbs = BlumBlumShub(seed)
    index = 0
    
    for y in range(height):
        for x in range(width):
            if index >= len(binary_message):
                break
            
            r, g, b = pixels[x, y]  
            
            channel_select = [bbs.next_bit() for _ in range(3)]

            for i, channel in enumerate([r, g, b]):
                if channel_select[i] and index < len(binary_message):
                    new_channel = (channel & 0xFE) | int(binary_message[index])
                    if i == 0:
                        r = new_channel
                    elif i == 1:
                        g = new_channel
                    else:
                        b = new_channel
                    index += 1
            
            pixels[x, y] = (r, g, b)
    
    img.save(output_path)
    print(f"Message hidden successfully in {output_path}")

if __name__ == "__main__":
    image_path = "deadpool.png"
    output_path = "stego.png"
    message = "This is a secret message!"
    seed = 987654321
    
    hide_message(image_path, message, output_path, seed)