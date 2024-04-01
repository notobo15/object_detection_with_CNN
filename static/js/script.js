function delete_iamge(self) {
  $(self).parent().remove()
}
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
                <img src="${imgSrc}" style="height: 58px;"> <!-- Điều chỉnh kích thước hình ảnh -->
                <button class="delete-btn" onclick="delete_iamge(this)"><i class="fas fa-trash-alt text-white"></i></button>
            </div>
        `);
    };
    reader.readAsDataURL(file);
  });
  let countImages = $(ImageContainerEle).find("div").length + files.length
  let label = ImageContainerEle.siblings(".open-samples-label")
  label.text(`${countImages} Image Samples`)
}

function delete_class(e) {
  let container = $(e.srcElement).parent().parent().parent().parent()
  console.log(container)
  container.remove()
}

$(document).ready(function () {
  changeColorProcessBar()
  var index = 1
  $(".btn_add_a_class").click(function () {
    //oninput="adjustWidth(this)"
    let html = `
    <div class="p-2 mb-3 shadow" style="width: 100%; height: auto;border: 1px solid #ccc; border-radius: 10px;">
  <div class="d-flex justify-content-between align-items-center border-bottom pb-4">
    <div>
      <input editing class="mr-1" type="text" style="width: 100px; min-width: 100px;border: 0;font-size: 20px;"
        value="Class ${index++}"  />
      <span type="button" onclick="focusInput(this)"><i class="fas fa-pen"></i></span>
    </div>
    <span class="text-primary" type="button" class="dropdown-toggle" data-toggle="dropdown">
      <span type="button" class="p-2">
        <i class="fas fa-ellipsis-v"></i></span>
      <div class="dropdown-menu dropdown-menu-right">
        <span class="dropdown-item" onclick="delete_class(event)">Delete class</span>
        <a class="dropdown-item" href="#">Disable class</a>
        <a class="dropdown-item" href="#">Remove All Samples</a>
        <a class="dropdown-item" href="#">Download Samples</a>
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
        <button type="button" style="width: 72px;"
          class="btn-show-webcam btn btn-outline-primary mr-2 d-flex flex-column justify-content-between align-items-center align-self-stretch">
          <i class="fas fa-video"></i>
          <span>Webcam</span>
        </button>
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



  // -------- 
  var sample_input_list = $(".sample-input-list");
  var openContainer = $(".open-container");
  $(".btn-show-webcam").on("click", () => {
    sample_input_list.hide();
    openContainer.css("display", "flex");
    startWebCam();
  });

  var list_images = [];
  function shortcut() {
    var picture = webcam.snap();
    // list_images.push(picture);
    return picture;
  }
  function Add() {
    list_images.push(shortcut());
    var html = convertListToElement();
    $(".samples").html(html);
  }
  function convertListToElement() {
    var html = "";
    list_images.forEach((value, index) => {
      html += `<img class='samples_image' src=${value} alt=''/>`;
    });
    return html;
  }
  function closeContainer() {
    sample_input_list.show();
    openContainer.css("display", "none");
    stopWebCam();
  }
  function focusInput(ele) {
    $(ele).siblings("input").focus();
  }
  function adjustWidth(input) {
    // Reset input width to auto to allow it to expand
    // input.style.width = 'auto';
    // Calculate the width required to fit the content
    var width = input.scrollWidth;
    if (width <= 100) return;
    // Set the input width to the calculated width
    input.style.width = width + "px";
  }
  var video = document.getElementById("videoElement");

  var stream;
  const webcamElement = document.getElementById("webcam");
  const canvasElement = document.getElementById("canvas");
  const webcam = new Webcam(webcamElement, "user", canvasElement);

  function flipCamera() {
    if (webcamElement.style.transform === "scaleX(1)") {
      video.style.transform = "scaleX(-1)";
    } else {
      video.style.transform = "scaleX(1)";
    }
  }
  function flip() {
    webcam.flip();
  }
  function startWebCam() {
    webcam
      .start()
      .then((result) => {
        const canvas = document.querySelector("canvas");
        const ctx = canvas.getContext("2d");
        const video = document.querySelector("video");
        video.addEventListener("play", () => {
          function step() {
            // Lấy kích thước của video
            const videoWidth = video.videoWidth;
            const videoHeight = video.videoHeight;

            // Tính toán kích thước hình vuông
            const size = Math.min(videoWidth, videoHeight);

            // Tính toán vị trí để cắt video theo chiều ngang giữa để tạo thành hình vuông
            const offsetX = (videoWidth - size) / 2;
            const offsetY = (videoHeight - size) / 2;

            // Cắt video chỉ lấy hình vuông
            ctx.drawImage(
              video,
              offsetX,
              offsetY,
              size,
              size,
              0,
              0,
              canvas.width,
              canvas.height
            );

            // Gọi lại hàm này để vẽ tiếp mỗi frame của video
            requestAnimationFrame(step);
          }

          // Bắt đầu vẽ video lên canvas
          step();
        });
      })
      .catch((err) => {
        console.log(err);
      });
  }
  function stopWebCam() {
    webcam.stop();
  }


})

var loadingEle = $('#loadingSpinner')
$(".btn_train_model").click(function () {
  let tmp = []
  $(".class_container").children().each(function () {
    var child = $(this);
    console.log(child.find("img"))
    tmp.push({
      'label': child.find('input[type="text"]').val(),
      'images': child.find('input[type="file"]')[0].files,

    })
  });
  var formData = new FormData();

  formData.append("data", JSON.stringify(tmp.map(item => ({ label: item.label }))));

  // Thêm images, giả định mỗi object có một mảng `images`
  tmp.forEach((item, index) => {
    item.images.forEach((file, fileIndex) => {
      formData.append(`images_${index}_${fileIndex}`, file);
    });
  });
  loadingEle.show();

  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    headers: {
      'X-CSRFToken': csrftoken
    }
  });
  $.ajax({

    url: "/train-model",
    type: "POST",
    data: formData,
    processData: false,
    contentType: false,
    success: function (response) {
      localStorage.setItem("uuid", response?.uuid)
      loadingEle.hide();
    },
    error: function (xhr, status, error) {
      // Handle error
      console.log(error)
      // ShowToast(jQuery.parseJSON(xhr.responseText)?.image[0])
      loadingEle.hide();
    }
  });

});


function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Check if the cookie name matches the CSRF token cookie name
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
let uuid = localStorage.getItem("uuid");
$("document").ready(async function () {
  model = await tf.loadLayersModel(`http://127.0.0.1:8000/static/uploads/${uuid}/model.json`);
  // console.log('Load model');
  // console.log(model.summary());
});

$("#btn_predict").click(async function () {
  await loadingEle.show();
  // 1. Chuyen anh ve tensor
  let image = $('#imagePreview')[0];
  let img = tf.browser.fromPixels(image);
  let normalizationOffset = tf.scalar(255 / 2); // 127.5
  let tensor = await img
    .resizeNearestNeighbor([112, 112])
    .toFloat()
    .sub(normalizationOffset)
    .div(normalizationOffset)
    .reverse(2)
    .expandDims();
  // 2. Predict
  let predictions = await model.predict(tensor);
  predictions = predictions.dataSync();
  // console.log(predictions);
  // const FLOWER_CLASS = ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']
  let result = await Array.from(predictions)
    .map(function (p, i) {
      return {
        probability: (p * 100).toFixed(1),
        className: FLOWER_CLASS[i]
      };
    })
  // .sort(function (a, b) {
  //   return b.probability - a.probability;
  // });
  console.log(result);
  await loadingEle.hide();
  let html = ``
  result.forEach((item) => {
    html += `
    <div class="d-flex justify-content-between align-items-center">
    <h6 class="mb-0" style="width: 30%">${item.className}</h6>
    <div class="progress mb-3" style="width:70%; height: 29px; border-radius: 6px">
      <div class="progress-bar" role="progressbar" style="width: ${item.probability}%; color: #000;" aria-valuenow="${item.probability}" aria-valuemin="0" aria-valuemax="100">
        ${item.probability}%
      </div>
    </div>
  </div>
    `
  })
  $("#output").html(html)
  changeColorProcessBar()


});

$('#upload_img').change(function () {
  const file = this.files[0];
  // console.log(file)
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      $('#imagePreview').attr('src', e.target.result);
    }
    reader.readAsDataURL(file);
  } else {
    $('#imagePreview').attr('src', '');
  }
});
// const FLOWER_CLASS = {
//   0: 'daisy',
//   1: 'dandelion',
//   2: 'roses',
//   3: 'sunflowers',
//   4: 'tulips'
// };

function changeColorProcessBar() {

  var colors = ["#dc2f02", "#ccd5ae", "#d4a373", "#cdb4db", "#00b4d8", "#588157", "#a3b18a", "#eae2b7", "#e9c46a", "#e76f51"];

  // Lặp qua từng div và đặt màu cho chúng
  $(".progress-bar").each(function (index) {
    $(this).css("background-color", colors[index]);
  });
}