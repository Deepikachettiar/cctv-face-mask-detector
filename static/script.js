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
