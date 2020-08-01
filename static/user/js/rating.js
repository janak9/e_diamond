var data = [
  {
    "ATTRIBUTEID": "FOODQUALITY",
    "ATTRIBUTENAME": "Quality Of Food",
    "POSITION": 1
  },
  {
    "ATTRIBUTEID": "CLEANLINESS",
    "ATTRIBUTENAME": "Cleanliness",
    "POSITION": 2
  },
  {
    "ATTRIBUTEID": "SERVICE",
    "ATTRIBUTENAME": "Service",
    "POSITION": 3
  },
  {
    "ATTRIBUTEID": "STAFFBEHAVE",
    "ATTRIBUTENAME": "Staf Behavior",
    "POSITION": 4
  },
  {
    "ATTRIBUTEID": "AMBIENCE",
    "ATTRIBUTENAME": "Ambience",
    "POSITION": 5
  }
];

for (i = 0; i < data.length; i++){
  var container = document.getElementById("container");

  var row = document.createElement('div');
  row.className = "form-row";

  var commonLabel = document.createElement('label');
  commonLabel.className = "commonLable";
  commonLabel.innerHTML = data[i].ATTRIBUTENAME;


  var form_group = document.createElement('div');
  form_group.className = "form-group col-lg-12";

  for (j = 5;j > 0; j--) {
    var star = document.createElement("input");
    var label = document.createElement("label");
    star.type = "radio";
    star.id = data[i].ATTRIBUTEID + j;
    star.name = data[i].ATTRIBUTEID;
    star.className = "star star-" + j;
    star.value = j;
    label.className = "star star-" + j;
    label.htmlFor = data[i].ATTRIBUTEID + j;
    form_group.append(star, label);
  }

  row.append(commonLabel, form_group);
  container.appendChild(row);
}

$('#submit').click(function(){
  var formData = $('#container').serialize();
  alert(formData);
});