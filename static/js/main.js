function changeColorProcessBar() {
  // var colors = ["#dc2f02", "#ccd5ae", "#d4a373", "#cdb4db", "#00b4d8", "#588157", "#a3b18a", "#eae2b7", "#e9c46a", "#e76f51"];
  var colors = ["#E67701", "#D84C6F", "#794AEF", "#1967D2"];
  $(".progress-bar").each(function (index) {
    var colorIndex = index % colors.length;
    $(this).css("background-color", colors[colorIndex]);
    $(this).parent().css("background-color", `rgba(${hexToRgb(colors[colorIndex])}, 0.1)`);
  });
}
function hexToRgb(hex) {
  hex = hex.substring(1);
  var r = parseInt(hex.substring(0, 2), 16);
  var g = parseInt(hex.substring(2, 4), 16);
  var b = parseInt(hex.substring(4, 6), 16);
  return `${r}, ${g}, ${b}`;
}
function ShowToast(message = "This is a toast", title = "Error", type = "error") {
  toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": true,
    "progressBar": true,
    "positionClass": "toast-top-right",
    "preventDuplicates": true,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
  }
  toastr[type](message, title);
}

$('.images-container').on('click', '.delete-btn', function (event) {
  event.preventDefault();
  event.stopPropagation();
  let container = $(this).parent().parent()

  $(this).closest('.image-link').remove();

  // console.log($(container).find(".image-link"))
  $(container).parent().siblings("h6").text(`${$(container).find(".image-link").length} Images Samples`)
  // Xóa hình ảnh
});

$('.sample-source-btn').click(function () {
  $('#file-input').click();
});


$('#file-input').change(function () {
  let containerEle = $(this).parent().parent()
  let labelEle = $(containerEle).siblings("h6")
  let totalImageCurrent = $(containerEle).find("img").length

  var files = this.files;
  for (var i = 0; i < files.length; i++) {
    var file = files[i];
    var reader = new FileReader();

    reader.readAsDataURL(file);

    reader.onload = function (e) {
      var imageUrl = e.target.result;

      var newImageLink = $('<a>', {
        href: imageUrl,
        'data-fancybox': true,
        'data-caption': 'New Image',
        class: 'image-link',
        style: 'width: 58px; height: 58px; margin-right: 5px; display: inline-block; border-radius: 6px; position: relative;'
      });

      var newImage = $('<img>', {
        src: imageUrl,
        style: 'width: 100%; border-radius: 4px; height: 58px;',
        class: 'border',
        loading: 'lazy'
      });
      // Tạo nút xóa và thêm vào thẻ a
      var deleteButton = $('<button>', {
        class: 'delete-btn',
        click: function () {
          $(this).closest('.image-link').remove();

        }
      }).append($('<i>', {
        class: 'fas fa-trash-alt text-white'
      }));

      // Thêm thẻ img và nút xóa vào thẻ a
      newImageLink.append(newImage);
      newImageLink.append(deleteButton);
      $('.images-container').append(newImageLink);

      labelEle.text(`${+totalImageCurrent + files.length} Images Samples`)

    };
  }

});

$('#upload_img').change(function () {
  const file = this.files[0];
  // console.log(file)
  if (file) {
    const reader = new FileReader();
    isUploaded = true
    reader.onload = function (e) {
      $('#imagePreview').attr('src', e.target.result);
    }
    reader.readAsDataURL(file);
  }
  $("#output").empty();
  $("#prediction-result").empty();
});

function checkClassNotEmptyImages() {
  let total_image_list = []
  $(".image_item").each(function (index, item) {
    let total_image = $(item).find("img").length
    total_image_list.push(total_image)
  })
  if (total_image_list.length === 0) return `Cannot train model without data. Click "add a class" below.`
  for (let index = 0; index < total_image_list.length; index++) {
    let item = total_image_list[index];
    if (item === 0) {
      let class_name = $($($('.image_item')[index]).find('input')[0]).val();
      return `"${class_name}" requires at least 1 image. Click "Upload" below to begin.`;
    }
  }
  return true
}
function checkTrained() {
  return localStorage.getItem("uuid") ? true : false
}
function delete_class(e) {
  let container = $(e.srcElement).parent().parent().parent().parent()
  // console.log(container)
  container.remove()
}

var loadingEle = $('#loadingSpinner')

async function convertImageToTensor(image) {

  let img = tf.browser.fromPixels(image);
  let normalizationOffset = tf.scalar(255); // 127.5
  let tensor = await img
    .resizeNearestNeighbor([128, 128])
    .toFloat()
    .sub(normalizationOffset)
    .div(normalizationOffset)
    .reverse(2)
    .expandDims();
  return tensor
}
async function predict(model, tensor) {
  let predictions = await model.predict(tensor);
  predictions = predictions.dataSync();
  return predictions
}

async function loadModel(uuid) {
  model = await tf.loadLayersModel(`http://127.0.0.1:8000/static/uploads/${uuid}/model.json`);
  console.log('Load model done')
  console.log(model.summary());
  return model;
}

function clear() {
  localStorage.removeItem("uuid")
}
function getUuid() {
  return localStorage.getItem("uuid");
}
function saveUuid(uuid) {
  localStorage.setItem("uuid", uuid);
}
var isUploaded = false
function getImageData() {
  var imageData = [];

  // Lặp qua từng phần tử được tạo ra từ vòng lặp Django
  $('.image_item').each(function () {
    var label = $(this).find('input')?.val()?.trim();
    var images = [];

    // Lặp qua từng hình ảnh trong phần tử images-container
    $(this).find('.images-container  img').each(function () {
      var imageUrl = $(this).attr('src'); // Lấy đường dẫn hình ảnh
      images.push(imageUrl); // Thêm đường dẫn hình ảnh vào mảng images
    });

    // Tạo đối tượng JSON chứa thông tin nhãn và hình ảnh
    var imageDataItem = {
      label: label,
      images: images
    };

    // Thêm đối tượng vào mảng imageData
    imageData.push(imageDataItem);
  });

  return imageData;
}
function export_model(uuid) {
  let export_link = `/static/uploads/${uuid}/tfjs.zip`
  $('.btn_export_model').attr('href', export_link);
  $('.btn_export_model').attr('download', export_link);
}
$(".btn_export_model").click(function () {
  if (!$('.btn_export_model').attr('href')) {
    ShowToast("The model must be trained before exporting.")
  }
})

function showAnalyst(uuid) {
  let html = `
  <a class="btn btn-outline-success mt-3" href="/static/uploads/${uuid}/analyst.png" data-fancybox="single" data-caption="Single image">Show Analyst <i class="fas fa-chart-line ml-2"></i>
  </a>
  `
  $(".show_analyst").html(html)
  $(".show_analyst").removeClass("d-none");
}