function loadImage(event, id) {
  var output = document.getElementById(id);
  output.src = URL.createObjectURL(event.target.files[0]);
};

var host;

$(document).ready(function () {
  host = window.location.origin;
});

function get_category (main_category, category) {
  const main_category_id = document.getElementById(main_category).value;
  const category_element = document.getElementById(category);
  if (main_category_id > 0) {
    $.ajax({
      type: 'POST',
      url: host + "/main_admin/get_category/",
      data: {
        "data": JSON.stringify({
          'main_category_id': main_category_id
        })
      },
      success: function (response) {
        response = JSON.parse(response);
        console.log(response);
        let output = '';
        response.categories.forEach(category => {
          output += `<option value="${category.id}">${category.name}</option>`;
        });
        category_element.innerHTML = output;
      },
      error: function (msg) {
        console.log(msg);
      }
    });
  }
}