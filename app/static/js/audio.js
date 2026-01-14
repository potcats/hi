// Carrie Ko, Christine Chen, Cindy Liu, Joyce Lin
// hi
// SoftDev
// P02: Makers Makin' It, Act I
// 01/16/2026

window.onload = function() {
  document.getElementById('audio').checked = false;
};

/* AUDIO BUTTON INTERACTIONS */
var Aud = function() {
  let bgm = document.getElementById('bgm');
  if (bgm.paused) {
    bgm.play();
  }
  else {
    bgm.pause();
  }
};
