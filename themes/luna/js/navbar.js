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