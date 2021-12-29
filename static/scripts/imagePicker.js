/**
 * Script to change the main image when the thumbnail images are selected.
 */

/**
 * Function to change the main display image when the smaller thumbnail images are selected.
 * @param image Thumbnail image being selected.
 */
function thumbnailPicker(image) {
    document.querySelector('.image').src = image;
}
