function loadImage(event, id) {
  var output = document.getElementById(id);
  output.src = URL.createObjectURL(event.target.files[0]);
};

var host;

$(document).ready(function () {
  host = window.location.origin;
});

function responseWrapper(response){
  try {
    response = JSON.parse(response);
    return response;
  } catch (e) {
    top.location.href="/auth/login/";
  }
}

function add_wishlist(product_id, event = undefined) {
  event && event.preventDefault();
  if (product_id > 0) {
    $.ajax({
      type: 'POST',
      url: host + "/add_wishlist/",
      data: {
        "data": JSON.stringify({
          'product_id': product_id
        })
      },
      success: function (response) {
        response = responseWrapper(response)
        console.log(response);
        alert(response.msg);
      },
      error: function (msg) {
        console.log(msg);
      }
    });
  }
}

function apply_coupon() {
  const coupon_code = document.getElementById('coupon_code').value;
  if (coupon_code === '') {
    document.getElementById('coupon_code').classList.add('alert-danger');
  } else {
    $.ajax({
      type: 'POST',
      url: host + "/verify_offer/",
      data: {
        "data": JSON.stringify({
          'coupon_code': coupon_code
        })
      },
      success: function (response) {
        response = responseWrapper(response)
        console.log(response);
        if (response.status == "success"){
          document.getElementById('coupon_code').classList.add('alert-success');
          update_cart_bill(response);
        } else {
          document.getElementById('coupon_code').classList.add('alert-danger');
          alert(response.msg);
        }
      },
      error: function (msg) {
        console.log(msg);
      }
    });
  }
}

function update_cart(product_id, qty = 1, event = undefined) {
  if (product_id > 0 && qty > 0) {
    $.ajax({
      type: 'POST',
      url: host + "/update_cart/",
      data: {
        "data": JSON.stringify({
          'product_id': product_id,
          'qty': qty,
        })
      },
      success: function (response) {
        response = responseWrapper(response)
        console.log(response);
        console.log(response.cart_bill);
        if (response.status == "success"){
          update_cart_bill(response);
        } else {
          alert(response.msg);
        }
      },
      error: function (msg) {
        console.log(msg);
      }
    });
  }
}

function update_cart_bill (response) {
  document.getElementById('sub_total').innerHTML = response.cart_bill.sub_total;
  document.getElementById('coupon_discount').innerHTML = response.cart_bill.coupon_discount;
  document.getElementById('tax').innerHTML = response.cart_bill.tax;
  document.getElementById('shipping_cost').innerHTML = response.cart_bill.shipping_cost;
  document.getElementById('grand_total').innerHTML = response.cart_bill.grand_total;
}

function remove_cart(product_id, event = undefined) {
  event && event.preventDefault();
  if (product_id > 0) {
    $.ajax({
      type: 'POST',
      url: host + "/remove_cart/",
      data: {
        "data": JSON.stringify({
          'product_id': product_id
        })
      },
      success: function (response) {
        response = responseWrapper(response)
        console.log(response);
        alert(response.msg);
      },
      error: function (msg) {
        console.log(msg);
      }
    });
  }
}

function add_review(product_id, event = undefined) {
  if (product_id > 0) {
    let comment = document.getElementById('review_comment').value;
    let star = document.querySelectorAll('input[name="star"]:checked')[0];
    console.log(comment);
    console.log(star);
    if (comment.value != "" && star && star.value) {
      $.ajax({
        type: 'POST',
        url: host + "/add_review/",
        data: {
          "data": JSON.stringify({
            'product_id': product_id,
            'comment': comment,
            'star': star
          })
        },
        success: function (response) {
          response = responseWrapper(response)
          console.log(response);
          if (response.status != 'success') {
            alert(response.msg);
          }
        },
        error: function (msg) {
          console.log(msg);
        }
      });
    } else {
      alert('please fill the message and give rating.')
    }
  }
}

function add_compare(product_id, event = undefined) {
  event && event.preventDefault();
  if (product_id > 0) {
    $.ajax({
      type: 'POST',
      url: host + "/add_compare/",
      data: {
        "data": JSON.stringify({
          'product_id': product_id
        })
      },
      success: function (response) {
        response = responseWrapper(response)
        console.log(response);
        alert(response.msg);
      },
      error: function (msg) {
        console.log(msg);
      }
    });
  }
}
