function changeColorProcessBar() {

  var colors = ["#dc2f02", "#ccd5ae", "#d4a373", "#cdb4db", "#00b4d8", "#588157", "#a3b18a", "#eae2b7", "#e9c46a", "#e76f51"];

  // Lặp qua từng div và đặt màu cho chúng
  $(".progress-bar").each(function (index) {
    $(this).css("background-color", colors[index]);
  });
}