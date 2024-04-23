
function loadImages(e) {
  let image_ele = e.srcElement
  const files = image_ele.files;
  let ImageContainerEle = $(image_ele).parent().parent().parent().parent().siblings(".images-container")
  $.each(files, function (i, file) {
    if (!file.type.startsWith('image/')) return; // Bỏ qua nếu không phải hình ảnh
    const reader = new FileReader();
    reader.onload = function (e) {
      const imgSrc = e.target.result;

      // Tạo và thêm hình ảnh và nút xóa vào container
      ImageContainerEle.append(`
            <div style="display: inline-block; position: relative;">
                <a href="" class="image-link">
                  <img src="${imgSrc}" style="height: 58px;"> <!-- Điều chỉnh kích thước hình ảnh -->
                  </a>
                  <button class="delete-btn" onclick="delete_image(this)"><i class="fas fa-trash-alt text-white"></i></button>
            </div>
        `);
    };
    reader.readAsDataURL(file);
  });
  let countImages = $(ImageContainerEle).find("div").length + files.length
  let label = ImageContainerEle.siblings(".open-samples-label")
  label.text(`${countImages} Image Samples`)
}
function updateCountImages() {
  $(".images-container").find('.image_item').length
}
function delete_class(e) {
  let container = $(e.srcElement).parent().parent().parent().parent()
  console.log(container)
  container.remove()
}

$(document).ready(function () {

  $(".predict_container").hide();
  var index = 1
  $(".btn_add_a_class").click(function () {
    //oninput="adjustWidth(this)"
    let html = `
    <div class="p-2 mb-3 shadow image_item" style="width: 100%; height: auto;border: 1px solid #ccc; border-radius: 10px;">
  <div class="d-flex justify-content-between align-items-center border-bottom pb-4">
    <div>
      <input editing class="mr-1" type="text" style="min-width: 100px;border: 0;font-size: 20px;"
        value="Class ${index++}"  />
      <span type="button" onclick="focusInput(this)"><i class="fas fa-pen"></i></span>
    </div>
    <span class="text-primary" type="button" class="dropdown-toggle" data-toggle="dropdown">
      <span type="button" class="p-2">
        <i class="fas fa-ellipsis-v"></i></span>
      <div class="dropdown-menu dropdown-menu-right">
        <span class="dropdown-item" onclick="delete_class(event)">Delete class</span>
        <!--
        <a class="dropdown-item" href="#">Disable class</a>
        <a class="dropdown-item" href="#">Remove All Samples</a>
        <a class="dropdown-item" href="#">Download Samples</a>
        --->
      </div>
    </span>
  </div>
  <div class="open-samples-label" class="samples-label">
    0 Image Samples
  </div>
  <div class="images-container" style="overflow-x: auto; white-space: nowrap; width: 100%;"></div>
  <div>
    <div class="sample-input-list mt-1">
      <h6><i>Add Image Samples:</i></h6>
      <div class="d-flex justify-content-start align-items-center">
        <!-- <button type="button" style="width: 72px;"
          class="btn-show-webcam btn btn-outline-primary mr-2 d-flex flex-column justify-content-between align-items-center align-self-stretch">
          <i class="fas fa-video"></i>
          <span>Webcam</span>
        </button>
        -->
        <label type="button" style="width: 72px;"
          class="btn btn-outline-primary p-2 d-flex flex-column justify-content-between align-items-center mb-0">
          <i class="fas fa-upload"></i>
          <span>Upload</span>
          <input id="file-input" type="file" hidden required
            accept="application/zip, image/jpg, image/png, image/jpeg, image/bmp" multiple onchange="loadImages(event)" />
        </label>
      </div>
    </div>
    <div class="open-container position-relative">
      <div style="width: 50%">
        <button class="btn position-absolute top-0" style="right: 50%; z-index: 1" onclick="closeContainer()">
          X
        </button
          <div>
          <video id="webcam" autoplay playsinline style="width: 100%"></video>
          <br />
          <canvas id="canvas" width="260" height="260"></canvas>
          <button id="flipButton" class="position-absolute top-0" style="left: 0" onclick="flip()">
            Flip Camera
          </button>
        </div>
        <div class="d-flex justify-content-between align-items-center">
          <button type="button" class="btn btn-outline-primary" style="width: 75%" onclick="Add()">
            Hold to Record
          </button>
          <button type="button" class="btn btn-outline-primary border-0">
            <i class="fas fa-cog"></i>
          </button>
        </div>
      </div>
      <div style="width: 50%">
        
        <div class="inner-samples-container">
          <div class="samples" style=""></div>
        </div>
      </div>
    </div>
    <div class="samples-container"></div>
  </div>
</div>
  `
    $(".class_container").append(html)


  })


})

var loadingEle = $('#loadingSpinner')
// $(".btn_train_model").click(function () {
//   let tmp = []
//   $(".class_container").children().each(function () {
//     var child = $(this);
//     tmp.push({
//       'label': child.find('input[type="text"]').val(),
//       'images': child.find('input[type="file"]')[0].files,

//     })
//   });
//   var formData = new FormData();

//   formData.append("data", JSON.stringify(tmp.map(item => ({ label: item.label }))));

//   // Thêm images, giả định mỗi object có một mảng `images`
//   tmp.forEach((item, index) => {
//     item.images.forEach((file, fileIndex) => {
//       formData.append(`images_${index}_${fileIndex}`, file);
//     });
//   });
//   loadingEle.show();
//   $.ajax({

//     url: "/train-model",
//     type: "POST",
//     data: formData,
//     processData: false,
//     contentType: false,
//     success: function (response) {
//       localStorage.setItem("uuid", response?.uuid)
//       loadingEle.hide();
//     },
//     error: function (xhr, status, error) {
//       // Handle error
//       console.log(error)
//       // ShowToast(jQuery.parseJSON(xhr.responseText)?.image[0])
//       loadingEle.hide();
//     }
//   });

// });

let uuid = localStorage.getItem("uuid");
$("document").ready(async function () {
  model = await tf.loadLayersModel(`http://127.0.0.1:8000/static/uploads/${uuid}/model.json`);
  // console.log('Load model');
  //   console.log(model.summary());
});

$("#btn_predict").click(async function () {
  if (!isUploaded) {
    ShowToast("Please, choose images from your files")
    return
  }
  if (!checkTrained()) {
    ShowToast("Please, train the model before making predictions")
    return
  }

  await loadingEle.show();
  // 1. Chuyen anh ve tensor
  let image = $('#imagePreview')[0];

  let img = tf.browser.fromPixels(image);
  let normalizationOffset = tf.scalar(255); // 127.5
  let tensor = await img
    .resizeNearestNeighbor([112, 112])
    .toFloat()
    .sub(normalizationOffset)
    .div(normalizationOffset)
    .reverse(2)
    .expandDims();


  // const tensor = tf.browser.fromPixels(img)
  //   .resizeNearestNeighbor([32, 32])  // Resize the image
  //   .mean(2)                           // Convert to grayscale
  //   .expandDims(-1)                    // Add the channel dimension
  //   .toFloat()                         // Make sure the data type is float
  //   .div(tf.scalar(255.0))             // Normalize
  //   .expandDims(0);                    // Add the batch dimension


  // const normalizationOffset = tf.scalar(127.5);
  // const tensor = img
  //   .resizeNearestNeighbor([32, 32])
  //   .toFloat()
  //   .sub(normalizationOffset)
  //   .div(normalizationOffset)
  //   .reverse(2)
  //   .expandDims();

  // const tensor = tf.browser.fromPixels(image)
  //   .resizeNearestNeighbor([32, 32])
  //   .toFloat()
  //   // .div(tf.scalar(255.0))
  //   .expandDims(0);
  // 2. Predict
  let predictions = await model.predict(tensor);
  predictions = predictions.dataSync();
  console.log(predictions);
  const CLASS_LABELS = getLabels()
  // let LABELS = trainingData['trainingData'].map((item, index) => item.label)
  let result = await Array.from(predictions)
    .map(function (p, i) {
      return {
        probability: (p * 100).toFixed(1),
        className: CLASS_LABELS[i]
      };
    })
  // .sort(function (a, b) {
  //   return b.probability - a.probability;
  // });
  console.log(result); // Test accuracy: 0.7714285850524902
  await loadingEle.hide();
  showProgressBar(result)
  changeColorProcessBar()
});

function showProgressBar(result) {
  $(".predict_container").show()
  let html = ``
  result.forEach((item) => {
    html += `
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h6 class="mb-0" style="width: 30%">${item.className}</h6>
      <div class="progress " style="width:70%; height: 29px; border-radius: 6px">
        <div class="progress-bar" role="progressbar" style="width: ${item.probability}%; color: #000;" aria-valuenow="${item.probability}" aria-valuemin="0" aria-valuemax="100">
          ${item.probability}%
        </div>
      </div>
  </div>
    `
  })
  $("#output").html(html)
}

// const FLOWER_CLASS = {
//   0: 'daisy',
//   1: 'dandelion',
//   2: 'roses',
//   3: 'sunflowers',
//   4: 'tulips'
// };

function getImageData() {
  var imageData = [];

  // Lặp qua từng phần tử được tạo ra từ vòng lặp Django
  $('.image_item').each(function () {
    var label = $(this).find('input').val().trim(); // Lấy thông tin nhãn từ thẻ h5
    var images = [];

    // Lặp qua từng hình ảnh trong phần tử images-container
    $(this).find('.images-container .image-link img').each(function () {
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
function getLabels() {
  return $.map($('.image_item'), function (val) {
    var label = $(val).find('input').val().trim();
    return label;
  });
}

$(".btn_train_model").click(function () {
  let message = checkClassNotEmptyImages()
  if (message != true) {
    ShowToast(message)
    return;
  }

  loadingEle.show();
  var trainingData = { 'trainingData': getImageData(), 'setting': JSON.parse(localStorage.getItem("setting")) }
  console.log(trainingData)
  fetch('/train-model2', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(trainingData)
  })
    .then(response => {

      return response.json();
    })
    .then(async data => {
      var uuid = data.uuid
      localStorage.setItem("uuid", uuid)
      model = await tf.loadLayersModel(`http://127.0.0.1:8000/static/uploads/${uuid}/model.json`);

      if (checkTrained()) {
        $(".btn_train_model").addClass("bg-success")
        $(".btn_train_model").text("Model Trained")

      }
      console.log('Load model');
      //        console.log(model.summary());
      // console.log(data); // In ra kết quả từ server
    })
    .catch(error => {
      console.error('Error:', error);
      ShowToast("An error occurred while processing your request. Please try again later.")
    })
    .finally(() => {
      loadingEle.hide();
    });
})

if (localStorage.getItem("uuid")) {
  $(".predict_container").show()
}

function focusInput(el) {
  console.log(el)
  $(el).siblings("input").focus()
}
function TotalClass() {
  let total = $(".image_item").length
  console.log(total)
}
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
function ShowToast(message = "This is a toast", title = "Data Error", type = "error") {
  // Toastify({
  //   text: message,
  //   duration: 3000,
  //   close: true,
  //   gravity: "top", // `top` or `bottom`
  //   position: "center", // `left`, `center` or `right`
  //   stopOnFocus: true,
  //   style: {
  //     background: "#ffc107",
  //     height: "60px"
  //   },
  //   title: "Data Error"
  // }).showToast();

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

window.addEventListener('beforeunload', function (e) {
  e.preventDefault();
  e.returnValue = '';
});