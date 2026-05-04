document.addEventListener('DOMContentLoaded', function() {
    const englishText = document.getElementById('englishText');
    const translateBtn = document.getElementById('translateBtn');
    const errorMessage = document.getElementById('errorMessage');
    const resultSection = document.getElementById('resultSection');
    const originalTextDiv = document.getElementById('originalText');
    const brailleTextDiv = document.getElementById('brailleText');
    const copyBtn = document.getElementById('copyBtn');
    const loading = document.getElementById('loading');

    // Translate on button click
    translateBtn.addEventListener('click', translate);

    // Translate on Enter key (Ctrl/Cmd + Enter)
    englishText.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            translate();
        }
    });

    function translate() {
        const text = englishText.value.trim();

        // Clear previous error
        errorMessage.style.display = 'none';
        errorMessage.textContent = '';

        if (!text) {
            errorMessage.textContent = 'Please enter some text to translate.';
            errorMessage.style.display = 'block';
            resultSection.style.display = 'none';
            return;
        }

        // Show loading state
        loading.style.display = 'block';
        resultSection.style.display = 'none';

        // Send request to backend
        fetch('/api/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        })
        .then(response => response.json())
        .then(data => {
            loading.style.display = 'none';

            if (data.error) {
                errorMessage.textContent = data.error;
                errorMessage.style.display = 'block';
                resultSection.style.display = 'none';
            } else {
                originalTextDiv.textContent = data.original;
                brailleTextDiv.textContent = data.braille;
                resultSection.style.display = 'block';
                errorMessage.style.display = 'none';
            }
        })
        .catch(error => {
            loading.style.display = 'none';
            errorMessage.textContent = 'Error: ' + error.message;
            errorMessage.style.display = 'block';
            resultSection.style.display = 'none';
        });
    }

    // Copy to clipboard
    copyBtn.addEventListener('click', function() {
        const braille = brailleTextDiv.textContent;
        navigator.clipboard.writeText(braille).then(function() {
            const originalText = copyBtn.textContent;
            copyBtn.textContent = '✓ Copied!';
            setTimeout(function() {
                copyBtn.textContent = originalText;
            }, 2000);
        });
    });
});
