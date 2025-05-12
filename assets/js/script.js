// PicPile JS
// Will try to keep this as minimal as possible
// Daisy Universe [D]
// 05 . 09 . 25

document.addEventListener("DOMContentLoaded", ()=> {
    let lastSelected = null;
    const preview = document.getElementById("PIC");
  
    // only bind preview to non‑folder thumbnails
    document.querySelectorAll(".thumbnail:not(.folder)").forEach(thumb => {
      thumb.addEventListener("click", () => {
        if (lastSelected) lastSelected.classList.remove("selected");
        thumb.classList.add("selected");
        const img = thumb.querySelector("img");
        preview.style.backgroundImage = `url('${img.src.replace("Thumbnail=Yes", "Thumbnail=No")}')`;
        lastSelected = thumb;
        });
    });
});

function navigateUp(event) {
  event.preventDefault(); // Prevent the default link behavior

  const currentUrl = window.location.href;
  const lastSlashIndex = currentUrl.lastIndexOf("/");

  if (lastSlashIndex !== -1) {
    const newUrl = currentUrl.substring(0, lastSlashIndex);
    window.location.href = newUrl;
  }
}