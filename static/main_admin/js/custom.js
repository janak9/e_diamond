function loadImage(event, id) {
  var output = document.getElementById(id);
  output.src = URL.createObjectURL(event.target.files[0]);
};
