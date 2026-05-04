from flask import Flask, render_template, request, jsonify
import louis

app = Flask(__name__)

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
        # Using English Unified Braille (EUB)
        braille_text = louis.translateString('en-us-g2.ctb', text)
        
        return jsonify({
            'original': text,
            'braille': braille_text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
