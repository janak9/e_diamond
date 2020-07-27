var host;

$(document).ready(function () {
  host = window.location.origin;
});

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
        response = JSON.parse(response);
        console.log(response);
        alert(response.msg);
      },
      error: function (msg) {
        console.log(msg);
      }
    });
  }
}

// function remove_wishlist(wishlist_id, event = undefined) {
//   event && event.preventDefault();
//   if (wishlist_id > 0) {
//     $.ajax({
//       type: 'POST',
//       url: host + "/remove_wishlist/",
//       data: {
//         "data": JSON.stringify({
//           'wishlist_id': wishlist_id
//         })
//       },
//       success: function (response) {
//         response = JSON.parse(response);
//         if (response.status == "error")
//           alert(response.msg);
//       },
//       error: function (msg) {
//         console.log(msg);
//       }
//     });
//   }
// }

function add_cart(product_id, qty = 1, event = undefined) {
  if (product_id > 0 && qty > 0) {
    $.ajax({
      type: 'POST',
      url: host + "/add_cart/",
      data: {
        "data": JSON.stringify({
          'product_id': product_id,
          'qty': qty
        })
      },
      success: function (response) {
        response = JSON.parse(response);
        console.log(response);
        if (response.status == "error")
          alert(response.msg);
      },
      error: function (msg) {
        console.log(msg);
      }
    });
  }
}

function update_cart(product_id, qty = 1, event = undefined) {
  if (product_id > 0 && qty > 0) {
    const coupon_code = document.getElementById('coupon_code');
    $.ajax({
      type: 'POST',
      url: host + "/update_cart/",
      data: {
        "data": JSON.stringify({
          'product_id': product_id,
          'qty': qty,
          'coupon_code': coupon_code
        })
      },
      success: function (response) {
        response = JSON.parse(response);
        console.log(response);
        if (response.status == "success"){
          document.getElementById('sub_total').innerHTML = response.sub_total;
          document.getElementById('coupon_discount').innerHTML = response.sub_total;
          document.getElementById('tax').innerHTML = response.sub_total;
          document.getElementById('shipping_cost').innerHTML = response.sub_total;
          document.getElementById('grand_total').innerHTML = response.sub_total;
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
        response = JSON.parse(response);
        console.log(response);
        alert(response.msg);
      },
      error: function (msg) {
        console.log(msg);
      }
    });
  }
}