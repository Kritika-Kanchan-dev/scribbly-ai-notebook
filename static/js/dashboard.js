function toggleTheme() {
  const dark = document.getElementById("bgVideoDark");
  const light = document.getElementById("bgVideoLight");

  if (dark.classList.contains("hidden")) {
    dark.classList.remove("hidden");
    light.classList.add("hidden");
  } else {
    dark.classList.add("hidden");
    light.classList.remove("hidden");
  }
}

function toggleProfileDropdown() {
  document.getElementById("profileDropdown").classList.toggle("hidden");
}

function toggleSidebar() {
  document.getElementById("sidebarContent").classList.toggle("hidden");
}

function chooseTopic() {
  const topic = prompt("Enter the subject/topic to tag this session:");
  if (topic) {
    alert("Topic saved: " + topic);
    // Later: Store this in Firebase
  }
}
function handleUpload(files) {
  if (files.length === 0) return;

  const file = files[0];

  // Optional: Display a loading animation here

  const formData = new FormData();
  formData.append('file', file);

  // Replace with your actual Django backend URL
  fetch('/upload/', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    // Show generated summary / flashcards
    console.log("Success:", data);
    alert("Upload successful!");
  })
  .catch(error => {
    console.error("Error:", error);
    alert("Upload failed!");
  });
}

