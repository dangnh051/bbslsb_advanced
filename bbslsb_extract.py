from PIL import Image
import math

class BlumBlumShub:
    def __init__(self, seed, p=0, q=0):
        if p == 0 or q == 0:
            self.p = 30091
            self.q = 41227
        else:
            self.p = p
            self.q = q
        self.n = self.p * self.q
        self.state = seed % self.n
    
    def next_bit(self):
        self.state = pow(self.state, 2, self.n)
        return self.state % 2

def extract_message(image_path, seed, max_length=1000):
    img = Image.open(image_path)
    
    # Chuyển đổi ảnh sang RGB nếu cần thiết
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    pixels = img.load()
    width, height = img.size
    
    bbs = BlumBlumShub(seed)
    binary_message = []
    message = ""
    byte_buffer = []
    
    for y in range(height):
        for x in range(width):
            if len(message) >= max_length:
                break
            
            r, g, b = pixels[x, y]  
            
            channel_select = [bbs.next_bit() for _ in range(3)]
            
            for i, channel in enumerate([r, g, b]):
                if channel_select[i] and len(binary_message) < max_length * 8:
                    bit = channel & 1
                    byte_buffer.append(str(bit))
                    
                    if len(byte_buffer) == 8:
                        byte_str = ''.join(byte_buffer)
                        byte = int(byte_str, 2)
                        
                        if byte == 0:
                            return message
                        
                        message += chr(byte)
                        byte_buffer = []
    
    return message

if __name__ == "__main__":
    stego_image = "stego.png"
    seed = 987654321
    
    extracted = extract_message(stego_image, seed)
    print(f"Extracted message: {extracted}")