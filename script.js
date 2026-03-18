const directoryPath = './images';

// Array of image filenames in the images folder
// Replace with your actual image filenames
const imageFiles = [
  "pfp.png",
  "shinji.gif"

];

const gallery = document.getElementById('gallery');

// Variable to track the currently focused image
let focusedImage = null;

function setFocusedImage(img) {
    // Clear previous focus
    if (focusedImage) {
        focusedImage.removeAttribute('data-focused');
    }

    focusedImage = img;

    if (focusedImage) {
        focusedImage.setAttribute('data-focused', 'true');

    }
}

// Function to load images into the gallery
async function loadGallery() {
    imageFiles.forEach(file => {
        const img = document.createElement('img');
        img.src = `images/${file}`;
        img.alt = file;
        gallery.appendChild(img);

        // Add right-click event to focus/unfocus the image
        img.addEventListener('contextmenu', function (event) {
            event.preventDefault();

            const isFocused = this.getAttribute('data-focused') === 'true';

            // Toggle focus on this image
            if (isFocused) {
                setFocusedImage(null);
            } else {
                setFocusedImage(this);
            }
        });
    });
}


// Load the gallery when the page loads
window.onload = loadGallery;