from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import os
import base64

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
    font = None
    
    # Try to find a suitable font
    font_paths = [
        "/System/Library/Fonts/Monaco.dfont",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/Windows/Fonts/consola.ttf",
        "C:\\Windows\\Fonts\\consola.ttf"
    ]
    
    for font_path in font_paths:
        try:
            font = ImageFont.truetype(font_path, font_size)
            break
        except:
            continue
    
    # If no font found, use default
    if font is None:
        font = ImageFont.load_default()
    
    # Split text into lines
    lines = braille_text.split('\n')
    
    # Create temporary image to measure text
    temp_img = Image.new('RGB', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # Calculate image dimensions
    max_width = 0
    for line in lines:
        try:
            bbox = temp_draw.textbbox((0, 0), line, font=font)
            width = bbox[2] - bbox[0]
            max_width = max(max_width, width)
        except:
            max_width = len(line) * 50  # fallback width estimation
    
    img_width = max_width + (padding * 2)
    img_height = (len(lines) * line_spacing) + (padding * 2)
    
    # Ensure minimum size
    img_width = max(img_width, 400)
    img_height = max(img_height, 300)
    
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
            attachment_filename=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/braille-preview', methods=['POST'])
def braille_preview():
    """Generate Braille image preview for display on page"""
    try:
        data = request.get_json()
        braille_text = data.get('braille', '').strip()
        
        if not braille_text:
            return jsonify({'error': 'No Braille text'}), 400
        
        # Generate image
        img = generate_braille_image(braille_text)
        
        # Convert to base64
        img_io = io.BytesIO()
        img.save(img_io, 'PNG', quality=95)
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        
        return jsonify({
            'image': f'data:image/png;base64,{img_base64}'
        })
    except Exception as e:
        print(f"Error in braille_preview: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
