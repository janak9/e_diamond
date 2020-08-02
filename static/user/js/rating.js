var stars = document.getElementById("stars");
var row = document.createElement('div');
row.className = "form-row";

var form_group = document.createElement('div');
form_group.className = "col-lg-12";

for (j = 5;j > 0; j--) {
  var star = document.createElement("input");
  var label = document.createElement("label");
  star.type = "radio";
  star.id = 'star' + j;
  star.name = 'star';
  star.className = "star star-" + j;
  star.value = j;
  label.className = "star star-" + j;
  label.htmlFor = 'star' + j;
  form_group.append(star, label);
}
row.append(form_group);
stars.appendChild(row);