// PicPile NavBar JS
// Keep any logic specific to the Navbar in here!
// Daisy Universe [D]
// 05 . 11 . 25

// Navigate up in the filesystem 
function navigateUp(event) {
  event.preventDefault(); // Prevent the default link behavior
  
  const currentUrl = window.location.href;
  const lastSlashIndex = currentUrl.lastIndexOf("/");
  
  if (lastSlashIndex !== -1) {
    const newUrl = currentUrl.substring(0, lastSlashIndex);
    window.location.href = newUrl;
  }
}

const textInput = document.getElementById('addressBox');

textInput.addEventListener('keydown', function(event) { if (event.key === 'Enter') { event.preventDefault(); loadFrame(textInput.value); }; } );

function loadFrame(target) {
  if ( window.location.href.endsWith("?view=ie") ) 
    { loadiFrame(target) } 
  else { loadPage(target) }
}

function loadPage(target) {
  window.location.href = target;
}

function loadiFrame(target) {
  document.getElementById('ieframe').src = target;
}
