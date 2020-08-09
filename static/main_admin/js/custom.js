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
  $("#info_list").append(info_str);
  $("#more_info").data("cnt", cnt+1);
}

function remove_more_info (id) {
  $("#"+id).remove();
}

function get_more_social (event) {
  event.preventDefault();
  let cnt = $("#more_social").data("cnt");
  const social_str = `<div class="row" id="social_${cnt}">
    <div class="col-md-6 form-group">
        <div class="input-group">
            <label class="col-sm-1 control-label">${cnt+1}</label>
            <span class="input-group-addon btn-white"><i class="fas fa-external-link-alt"></i></span>
            <input type="hidden" name="new_social_icon_${cnt}" value="fas fa-external-link-alt">
            <input type="text" class="form-control" name="new_social_link_${cnt}" placeholder="Enter Link" value='' required>
        </div>
    </div>
    <div class="col-md-2 form-group remove">
        <div class="btn btn-danger" onclick="remove_more_social('social_${cnt}', 'social_opt_${cnt}')"><i class='fa fa-times'></i></div>
    </div>
  </div>`;
  $("#social_list").append(social_str);
  $("#social_link_id").append(`<option id="social_opt_${cnt}" value="social_${cnt}" >${cnt+1}</option>`);
  $("#more_social").data("cnt", cnt+1);
}

function remove_more_social (id, opt_id) {
  $("#"+id).remove();
  $("#"+opt_id).remove();
}

function get_more_image (event) {
  event.preventDefault();
  let cnt = $("#more_image").data("cnt");
  const image_str = `<div class="row" id="image_${cnt}">
  <div class="form-group">
      <label class="col-sm-3 control-label">Image ${cnt+1}</label>
      <div class="col-sm-6">
          <input type="file" name="form-${cnt}-src" accept="image/*" class="form-control" id="id_form-${cnt}-src" onchange="loadImage(event,'id_form-${cnt}-src_preview')" >
          <input type="hidden" name="form-${cnt}-id" id="id_form-${cnt}-id" value="">
          <img id="id_form-${cnt}-src_preview" src="" height="150" width="150"/>
      </div>
      <div class="col-md-2 form-group remove">
        <div class="btn btn-danger" onclick="remove_more_image('image_${cnt}')"><i class='fa fa-times'></i></div>
      </div>
  </div>
  </div>`;
  $("#image_list").append(image_str);
  $("#more_image").data("cnt", cnt+1);
  $('#id_form-TOTAL_FORMS').val(cnt+1)
}

function remove_more_image (id) {
  $("#"+id).remove();
}
