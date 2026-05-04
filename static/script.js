document.addEventListener('DOMContentLoaded', function() {
    const englishText = document.getElementById('englishText');
    const translateBtn = document.getElementById('translateBtn');
    const errorMessage = document.getElementById('errorMessage');
    const resultSection = document.getElementById('resultSection');
    const originalTextDiv = document.getElementById('originalText');
    const brailleTextDiv = document.getElementById('brailleText');
    const brailleImageContainer = document.getElementById('brailleImage');
    const copyBtn = document.getElementById('copyBtn');
    const downloadBtn = document.getElementById('downloadBtn');
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
                
                // Generate and display Braille image
                generateBrailleImage(data.braille);
                
                // Store braille text for download
                downloadBtn.dataset.braille = data.braille;
            }
        })
        .catch(error => {
            loading.style.display = 'none';
            errorMessage.textContent = 'Error: ' + error.message;
            errorMessage.style.display = 'block';
            resultSection.style.display = 'none';
        });
    }

    function generateBrailleImage(brailleText) {
        fetch('/api/braille-preview', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ braille: brailleText })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to generate preview');
            }
            return response.blob();
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);
            brailleImageContainer.innerHTML = `<img src="${url}" alt="Braille Text">`;
        })
        .catch(error => {
            console.error('Error generating image:', error);
            brailleImageContainer.innerHTML = '<p style="color: red;">Could not generate image preview</p>';
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

    // Download as image
    downloadBtn.addEventListener('click', function() {
        const brailleText = downloadBtn.dataset.braille;
        if (!brailleText) return;

        downloadBtn.disabled = true;
        downloadBtn.textContent = '⏳ Generating...';

        fetch('/api/download-braille', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                braille: brailleText,
                filename: 'braille_translation.png'
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to download image');
            }
            return response.blob();
        })
        .then(blob => {
            // Create download link
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'braille_translation.png';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            // Clean up after a delay
            setTimeout(() => {
                URL.revokeObjectURL(url);
            }, 100);

            downloadBtn.disabled = false;
            downloadBtn.textContent = '🖨️ Download as Image';
        })
        .catch(error => {
            console.error('Download error:', error);
            alert('Error downloading image: ' + error.message);
            downloadBtn.disabled = false;
            downloadBtn.textContent = '🖨️ Download as Image';
        });
    });
});
