
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
            <img src="${imgSrc}" style="height: 58px;">
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


$(document).ready(function () {

  $(".predict_container").hide();
  var index = 1
  $(".btn_add_a_class").click(function () {
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
        <label type="button" style="width: 72px;"
          class="btn btn-outline-primary p-2 d-flex flex-column justify-content-between align-items-center mb-0">
          <i class="fas fa-upload"></i>
          <span>Upload</span>
          <input id="file-input" type="file" hidden required
            accept="application/zip, image/*" multiple onchange="loadImages(event)" />
        </label>
      </div>
    </div>
    <div class="samples-container"></div>
  </div>
</div>
  `
    $(".class_container").append(html)


  })
})

var isUploaded = false;

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

  let tensor = await convertImageToTensor(image)

  // 2. Predict
  let predictions = await predict(model, tensor);

  console.log(predictions);
  const CLASS_LABELS = getLabels();
  let sum = 0;
  let maxPerIndex = 0
  let maxPer = 0
  let result = await Array.from(predictions)
    .map(function (p, i) {
      let per = (p * 100).toFixed(1)
      if (maxPer < per) {
        maxPer = per
        maxPerIndex = +i
      }
      sum += +per
      return {
        probability: parseFloat(per).toFixed(1),
        className: CLASS_LABELS[i]
      };
    })
    .sort(function (a, b) {
      return b.probability - a.probability;
    });


  console.log(result)
  if (sum < 100) {
    result[maxPerIndex].probability = +result[maxPerIndex].probability + 0.1;
    result[maxPerIndex].probability = result[maxPerIndex].probability.toFixed(1)

  } else if (sum > 100) {
    result[maxPerIndex].probability = +result[maxPerIndex].probability - 0.1;
    result[maxPerIndex].probability = result[maxPerIndex].probability.toFixed(1)
  }
  console.log(result)
  result = result.filter((item) => item.probability > 5)
  await loadingEle.hide();
  showProgressBar(result)
  changeColorProcessBar()
});

function showProgressBar(result) {
  $(".predict_container").show()
  let html = ``
  result.forEach((item, index) => {
    html += `
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h6 class="mb-0 mr-3" style="width: 30%">${item.className}</h6>
      <div class="progress" style="width:60%; height: 29px; border-radius: 6px">
        <div class="progress-bar" role="progressbar" style="width: ${item.probability}%; color: #000;" aria-valuenow="${item.probability}" aria-valuemin="0" aria-valuemax="100">
          <!-- ${item.probability}% -->
        </div>
      </div>
      <div style="width: 10%" class="pl-2"><b>${index === 0 ? 1 : 0}</b></div>
  </div>
    `
  })
  $("#output").html(html)
  $("#prediction-result").html(`<hr >
  <div class="w-100 p-3 bg-success text-center text-white font-weight-bold" style="font-size: 20px; border-radius: 10px;">
    Prediction Result:
    <div style="font-size: 26px">${result[0].className}</div>
  </div>`)
}


// function getImageData() {
//   var imageData = [];

//   // Lặp qua từng phần tử được tạo ra từ vòng lặp Django
//   $('.image_item').each(function () {
//     var label = $(this).find('input').val().trim() || $(this).find('h5').text().trim(); // Lấy thông tin nhãn từ thẻ h5
//     var images = [];

//     // Lặp qua từng hình ảnh trong phần tử images-container
//     $(this).find('.images-container .image-link img').each(function () {
//       var imageUrl = $(this).attr('src'); // Lấy đường dẫn hình ảnh
//       images.push(imageUrl); // Thêm đường dẫn hình ảnh vào mảng images
//     });

//     // Tạo đối tượng JSON chứa thông tin nhãn và hình ảnh
//     var imageDataItem = {
//       label: label,
//       images: images
//     };

//     // Thêm đối tượng vào mảng imageData
//     imageData.push(imageDataItem);
//   });

//   return imageData;
// }
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
      export_model(uuid);
      console.log(model.summary());
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



window.addEventListener('beforeunload', function (e) {
  e.preventDefault();
  e.returnValue = '';
});
function delete_image(event) {
  let containeraImagesEle = $(event).parent().parent()
  $(event).parent().remove()
  $(containeraImagesEle).siblings(".open-samples-label").text(`${$(containeraImagesEle).find('img').length} Image Samples`)
}
let uuid = localStorage.getItem("uuid");
$("document").ready(async function () {
  loadModel(uuid)
});
