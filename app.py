from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)

# Braille character mapping (Grade 1 Braille)
BRAILLE_MAP = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
    'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
    'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
    'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
    'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽',
    'z': '⠵',
    '0': '⠼⠚', '1': '⠼⠁', '2': '⠼⠃', '3': '⠼⠉', '4': '⠼⠙',
    '5': '⠼⠑', '6': '⠼⠋', '7': '⠼⠛', '8': '⠼⠓', '9': '⠼⠊',
    '.': '⠲', ',': '⠂', ';': '⠆', ':': '⠒', '!': '⠮',
    '?': '⠿', '-': '⠤', "'": '⠄', '"': '⠐', '(': '⠣',
    ')': '⠜', '/': '⠌', '\\': '⠡', '&': '⠯', ' ': ' ',
    '\n': '\n'
}

def text_to_braille(text):
    """Convert English text to Braille."""
    braille_result = []
    capital_next = False
    
    for char in text.lower():
        if char.isupper():
            capital_next = True
            char = char.lower()
        
        # Add capital indicator if needed
        if capital_next and char.isalpha():
            braille_result.append('⠠')  # Capital indicator
            capital_next = False
        
        # Get braille character or use original if not mapped
        if char in BRAILLE_MAP:
            braille_result.append(BRAILLE_MAP[char])
        else:
            braille_result.append(char)  # Keep unmapped characters as-is
    
    return ''.join(braille_result)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Please enter some text'}), 400
        
        # Translate English text to Braille
        braille_text = text_to_braille(text)
        
        return jsonify({
            'original': text,
            'braille': braille_text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_braille_image(braille_text):
    """Generate an image from Braille text."""
    # Image settings
    padding = 50
    line_spacing = 80
    char_spacing = 8
    
    # Use a monospace font that supports Braille
    font_size = 96
    try:
        # Try to use a system font
        font = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", font_size)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", font_size)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
    
    # Split text into lines
    lines = braille_text.split('\n')
    
    # Create temporary image to measure text
    temp_img = Image.new('RGB', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # Calculate image dimensions
    max_width = 0
    for line in lines:
        bbox = temp_draw.textbbox((0, 0), line, font=font)
        width = bbox[2] - bbox[0]
        max_width = max(max_width, width)
    
    img_width = max_width + (padding * 2)
    img_height = (len(lines) * line_spacing) + (padding * 2)
    
    # Create image
    img = Image.new('RGB', (img_width, img_height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw text
    y_position = padding
    for line in lines:
        draw.text((padding, y_position), line, fill='black', font=font)
        y_position += line_spacing
    
    return img

@app.route('/api/download-braille', methods=['POST'])
def download_braille():
    try:
        data = request.get_json()
        braille_text = data.get('braille', '').strip()
        filename = data.get('filename', 'braille.png')
        
        if not braille_text:
            return jsonify({'error': 'No Braille text to download'}), 400
        
        # Generate image
        img = generate_braille_image(braille_text)
        
        # Save to bytes
        img_io = io.BytesIO()
        img.save(img_io, 'PNG', quality=95)
        img_io.seek(0)
        
        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
