// this file contains java script
const fileInput = document.getElementById('pic');
const previewSection = document.getElementById('preview');
const previewImage = document.getElementById('previewImage');
const loadingSection = document.getElementById('load');
const resultsSection = document.getElementById('results');
const uploadArea = document.querySelector('.upl-area');

let detectionActive = false;
let uplimgpath = null;


fileInput.addEventListener('change', 
    function(event) 
    {
    const file = event.target.files[0];
    if (file) {
        // Validate file type
        if (!file.type.startsWith('image/')) {
            alert('Please select a valid image file');
            return;
        }
        
        // Validate file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            alert('File size too large. Please select an image under 10MB');
            return;
        }

        // Show preview
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            previewSection.style.display = 'block';
            resultsSection.style.display = 'none';
            loadingSection.style.display = 'none';
        };
        reader.readAsDataURL(file);
    }
});





async function analyzeImage() {
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select an image first');
        return;
    }

     // Show loading state
    previewSection.style.display = 'none';
    loadingSection.style.display = 'block';
    resultsSection.style.display = 'none';

    try {
        // Upload file to Flask backend
        const formdata = new FormData();
        formdata.append('file', file);

        const uploadResponse = await fetch('/upload', {
            method: 'POST',
            body: formdata
        });

         if (!uploadResponse.ok) {
            throw new Error('Upload failed');
        }

        const uploadResult = await uploadResponse.text();
        console.log('Upload result:', uploadResult);

        // Start detection
        const startResponse = await fetch('/start_detection');
        const startResult = await startResponse.json();
        console.log('Detection started:', startResult);

        // Simulate processing time and get results
        await simulateDetection();

        // Stop detection
        const stopResponse = await fetch('/stop_detection');
        const stopResult = await stopResponse.json();
        console.log('Detection stopped:', stopResult);

    } catch (error) {
        console.error('Error during analysis:', error);
        alert('Error analyzing image. Please try again.');
        loadingSection.style.display = 'none';
        previewSection.style.display = 'block';
    }
}
// Animate result numbers
function animateNumbers() {
    const numbers = document.querySelectorAll('#withnum, #withoutnum, #totalnum');
    numbers.forEach(number => {
        const target = parseInt(number.textContent);
        number.textContent = '0';
        
        const increment = target / 50;
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                number.textContent = target;
                clearInterval(timer);
            } else {
                number.textContent = Math.floor(current);
            }
        }, 50);
    });
}


async function simulateDetection() {
    return new Promise((resolve) => {
        setTimeout(() => {
            
            // Update results
            document.getElementById('withMaskCount').textContent = withMask;
            document.getElementById('withoutMaskCount').textContent = withoutMask;
            document.getElementById('totalPeople').textContent = total;
            
            // Show results
            loadingSection.style.display = 'none';
            resultsSection.style.display = 'block';
            
            // Animate numbers
            animateNumbers();
            resolve();
        }, 3000);
    });
}

function resetApp() {
    previewSection.style.display = 'none';
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    fileInput.value = '';
    uploadedImagePath = null;
    
    // Reset detection state
    if (detectionActive) {
        fetch('/stop_detection')
            .then(response => response.json())
            .then(result => {
                console.log('Detection stopped:', result);
                detectionActive = false;
            });
    }
}

uploadArea.addEventListener('dragover', function(e) {
    e.preventDefault();
    uploadArea.style.borderColor = 'rgba(255, 255, 255, 0.6)';
    uploadArea.style.background = 'linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.15) 100%)';
});

uploadArea.addEventListener('dragleave', function(e) {
    e.preventDefault();
    uploadArea.style.borderColor = 'rgba(255, 255, 255, 0.3)';
    uploadArea.style.background = 'linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.1) 100%)';
});

uploadArea.addEventListener('drop', function(e) {
    e.preventDefault();
    uploadArea.style.borderColor = 'rgba(255, 255, 255, 0.3)';
    uploadArea.style.background = 'linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.1) 100%)';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        fileInput.dispatchEvent(new Event('change'));
    }
});
