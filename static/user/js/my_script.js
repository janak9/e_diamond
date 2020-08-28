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
          update_cart_bill(response.cart_bill);
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
        if (response.status == "success"){
          update_cart_bill(response.cart_bill);
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

function update_cart_bill (cart_bill) {
  document.getElementById('sub_total').innerHTML = cart_bill.sub_total;
  document.getElementById('coupon_discount').innerHTML = cart_bill.coupon_discount;
  document.getElementById('tax').innerHTML = cart_bill.tax;
  document.getElementById('shipping_cost').innerHTML = cart_bill.shipping_cost;
  document.getElementById('grand_total').innerHTML = cart_bill.grand_total;
  if (cart_bill.offer_response) {
    let coupon_code = document.getElementById('coupon_code');
    let coupon_text = document.getElementById('coupon_text');
    coupon_code.classList = "";
    coupon_text.classList = "";
    coupon_text.style = "display:block";
    if (cart_bill.offer_response.status === 'error') {
      coupon_code.classList.add('form-control', 'alert-danger');
      coupon_text.classList.add('alert', 'alert-danger');
      coupon_text.innerHTML = `${cart_bill.offer_response.msg}`;
    } else {
      coupon_code.classList.add('form-control', 'alert-success');
      coupon_text.classList.add('alert', 'alert-success');
      coupon_text.innerHTML = `Offer '${cart_bill.offer_response.offer_title}' Applied!`;
    }
  }
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
        document.getElementById('compare_count').innerHTML = response.compare_products_count;
        document.getElementById('compare_list').innerHTML = response.compare_products_list;
        alert(response.msg);
      },
      error: function (msg) {
        console.log(msg);
      }
    });
  }
}
