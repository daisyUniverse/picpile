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
        preview.style.backgroundImage = `url('${img.src}')`;
        lastSelected = thumb;
        });
    });
});