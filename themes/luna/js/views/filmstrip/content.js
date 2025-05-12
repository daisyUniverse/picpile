// PicPile Content JS
// Keep any logic specific to the Content (Filmreel, Preview) in here!
// Daisy Universe [D]
// 05 . 09 . 25

// Listen for thumbnail clicks, and set the preview image
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

