from flask import Flask, render_template, request, jsonify

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

if __name__ == '__main__':
    app.run(debug=True)
