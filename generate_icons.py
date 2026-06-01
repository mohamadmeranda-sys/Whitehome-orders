#!/usr/bin/env python3
"""Generate PWA icons for White Home app"""

import struct, zlib, base64

def create_png(size, bg_color, text_color):
    """Create a simple PNG icon with house symbol"""
    # Simple colored square PNG
    width = height = size
    
    # Create pixel data
    pixels = []
    cx, cy = width // 2, height // 2
    
    for y in range(height):
        row = []
        for x in range(width):
            # Background gradient (blue to light blue)
            r = int(3 + (x / width) * 14)
            g = int(105 + (y / height) * 20)
            b = int(161 + (x / width) * 30)
            
            # Draw white house shape
            # Roof triangle
            roof_h = height // 3
            roof_base = width * 0.7
            roof_left = int(cx - roof_base / 2)
            roof_right = int(cx + roof_base / 2)
            roof_top = int(cy - height * 0.35)
            
            in_roof = False
            if y >= roof_top and y <= cy - height * 0.05:
                slope = roof_base / 2 / (cy - height * 0.05 - roof_top + 1)
                dist_from_center = abs(x - cx)
                max_dist = (y - roof_top) * slope
                if dist_from_center <= max_dist:
                    in_roof = True
            
            # Body rectangle
            body_top = int(cy - height * 0.05)
            body_bottom = int(cy + height * 0.28)
            body_left = int(cx - width * 0.27)
            body_right = int(cx + width * 0.27)
            in_body = (body_left <= x <= body_right and body_top <= y <= body_bottom)
            
            # Door
            door_w = int(width * 0.14)
            door_h = int(height * 0.16)
            door_left = cx - door_w // 2
            door_right = cx + door_w // 2
            door_top = body_bottom - door_h
            in_door = (door_left <= x <= door_right and door_top <= y <= body_bottom)
            
            if in_door:
                row.extend([3, 105, 161, 255])  # blue door
            elif in_roof or in_body:
                row.extend([255, 255, 255, 255])  # white
            else:
                row.extend([r, g, b, 255])  # gradient bg
        pixels.append(row)
    
    # Build PNG
    def write_chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    
    signature = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = write_chunk(b'IHDR', ihdr_data)
    
    raw = b''
    for row in pixels:
        raw += b'\x00' + bytes(row)
    
    compressed = zlib.compress(raw, 9)
    idat = write_chunk(b'IDAT', compressed)
    iend = write_chunk(b'IEND', b'')
    
    return signature + ihdr + idat + iend

# Generate icons
for size, filename in [(192, 'icon-192.png'), (512, 'icon-512.png'), (180, 'apple-touch-icon.png')]:
    png_data = create_png(size, (3, 105, 161), (255, 255, 255))
    with open(f'/home/claude/whitehome-pwa/public/{filename}', 'wb') as f:
        f.write(png_data)
    print(f"Created {filename} ({size}x{size})")

print("All icons generated!")
