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
        let output = '<option value="" readonly>Select Category</option>';
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

function get_sub_category (category, sub_category) {
  const category_id = document.getElementById(category).value;
  const sub_category_element = document.getElementById(sub_category);
  if (category_id > 0) {
    $.ajax({
      type: 'POST',
      url: host + "/main_admin/get_sub_category/",
      data: {
        "data": JSON.stringify({
          'category_id': category_id
        })
      },
      success: function (response) {
        response = JSON.parse(response);
        console.log(response);
        let output = '<option value="" readonly>Select Sub Category</option>';
        response.sub_categories.forEach(sub_category => {
          output += `<option value="${sub_category.id}">${sub_category.name}</option>`;
        });
        sub_category_element.innerHTML = output;
      },
      error: function (msg) {
        console.log(msg);
      }
    });
  }
}

function get_more_info (event) {
  event.preventDefault();
  let cnt = $("#more_info").data("cnt");
  console.log('cnt: ', cnt);
  const info_str = `<div class="row" id="info_${cnt}">
  <div class="col-md-4 form-group" >
  <input type="text" class="form-control" name="new_info_title_${cnt}" placeholder="Enter Title" value="" required>
  </div>
  <div class="col-md-6 form-group">
  <input type="text" class="form-control" name="new_info_description_${cnt}" placeholder="Enter Description" value='' required>
  </div>
  <div class="col-md-2 form-group remove">
  <div class="btn btn-danger" onclick="remove_more_info('info_${cnt}')"><i class='fa fa-times'></i></div>
  </div>
  </div>`;
  console.log(info_str);
  $("#info_list").append(info_str);
  $("#more_info").data("cnt", cnt+1);
}

function remove_more_info (id) {
  $("#"+id).remove();
}