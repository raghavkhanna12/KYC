var photoCaptured = false; // Flag to track whether a photo has been captured

// Get access to the front camera
navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } })
  .then(function(stream) {
    var video = document.getElementById('video');
    video.srcObject = stream;
    video.play();
  })
  .catch(function(err) {
    console.log("An error occurred: " + err);
  });

// Capture photo
document.getElementById('capture-btn').addEventListener('click', function() {
  var video = document.getElementById('video');
  var canvas = document.getElementById('canvas');
  var context = canvas.getContext('2d');
  
  // Set canvas dimensions to match video dimensions
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  
  // Draw video frame onto canvas
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  
  // Convert canvas to base64 encoded image
  var imgData = canvas.toDataURL('image/png');
  
  // Change button text and instruction text without redirecting to next page
  if (!photoCaptured) {
    changeTextOnly();
  } else {
    // Send image data to backend and redirect to the next page
    saveImageAndRedirect(imgData);
  }
});

// Function to change button and instruction text only
function changeTextOnly() {
  // Set the flag to true after the first photo capture
  photoCaptured = true;

  // Change button text and instruction text
  document.getElementById('capture-btn').innerText = "Capture Aadhar Card";
  document.getElementById('instruction-text').innerText = "Capture image of Aadhar card";
}

// Function to send image data to backend and redirect to the next page
function saveImageAndRedirect(imgData) {
  fetch('/save_image', {
    method: 'POST',
    body: new URLSearchParams({
      'image': imgData
    })
  })
  .then(response => response.json())
  .then(data => {
    // Redirect to the next page after capturing Aadhar card front image
    window.location.href = "/display_info";
  })
  .catch(error => console.error('Error:', error));
}
