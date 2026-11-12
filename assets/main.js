"use strict";
const toast = document.querySelector(".toast");
let toastTimer;
document.querySelectorAll("[data-copy]").forEach((button) => {
  button.addEventListener("click", async () => {
    const text = button.closest("details").querySelector("pre").textContent;
    try {
      await navigator.clipboard.writeText(text);
      toast.textContent = "Citation copied.";
      button.textContent = "Copied";
      setTimeout(() => { button.textContent = "Copy citation"; }, 1800);
    } catch {
      toast.textContent = "Please select the citation text and copy it manually.";
    }
    clearTimeout(toastTimer);
    toast.hidden = false;
    toastTimer = setTimeout(() => { toast.hidden = true; }, 2600);
  });
});
