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
  event && event.preventDefault();
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
        // if (response.status != "updated")
        alert(response.msg);
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