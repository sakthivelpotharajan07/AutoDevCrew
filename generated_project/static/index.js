// Static/index.js

// To handle directory traversal attacks, we should explicitly specify the directory path.
const imagesDir = './images';

// Use a path library like node-path to handle path manipulation securely
const path = require('path');

// Use a try-catch block to handle potential data loss
try {
    // Use fs.readdirSync instead of fs.readdirSync('.') to avoid traversing through the parent directories
    const fs = require('fs');
    const imageFiles = fs.readdirSync(imagesDir).filter(file => file.endsWith('.jpg') || file.endsWith('.png') || file.endsWith('.gif'));

    // Remove the security issue by handling the case when no images are found
    if (imageFiles.length === 0) {
        // Return a JSON response with an error message instead of raising an exception
        res.json({ status: 404, error: 'No images found' });
    } else {
        // Process the image files and return them as a JSON response
        const images = imageFiles.map(file => {
            return {
                id: file,
                // For this example, we're just returning some default image metadata. In a real application, you'd replace this with actual image data.
                metadata: {
                    name: file,
                    size: 0,
                    type: fs.statSync(path.join(imagesDir, file)).isDirectory() ? 'directory' : 'file',
                }
            };
        });
        res.json({ status: 200, images });
    }
} catch (err) {
    // Return a JSON response with the error
    res.json({ status: 500, error: 'Failed to load images: ' + err.message });
}