// IE Content JS
// Robin Universe [S]
// 09 . 17 . 25

const textInput = document.getElementById('addressBox');

textInput.addEventListener('keydown', function(event) {
  if (event.key === 'Enter') {
    event.preventDefault(); 
    changeIEtarget(); 
  }
});

function changeIEtarget() {
  document.getElementById('ieframe').src = textInput.value;
}