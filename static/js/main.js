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

function delete_image(event) {
  let containeraImagesEle = $(event).parent().parent()
  let childrenEle = $(containeraImagesEle).children("div")
  $(containeraImagesEle).siblings(".open-samples-label").text(`${childrenEle.length} Image Samples`)

  $(event).parent().remove()
}
$('.images-container').on('click', '.delete-btn', function (event) {
  event.preventDefault();
  event.stopPropagation();

  // Xóa hình ảnh
  $(this).closest('.image-link').remove();
});

$('.sample-source-btn').click(function () {
  // Kích hoạt sự kiện click cho input type file ẩn
  $('#file-input').click();
});

var isUploaded = false;

$('#file-input').change(function () {
  var files = this.files;
  isUploaded = true
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
    };
  }
});
// function getImageData() {
//   var imageData = [];

//   // Lặp qua từng phần tử được tạo ra từ vòng lặp Django
//   $('.border.mb-3.shadow.bg-light').each(function () {
//     var label = $(this).find('h5').text().trim(); // Lấy thông tin nhãn từ thẻ h5
//     var images = [];

//     // Lặp qua từng hình ảnh trong phần tử images-container
//     $(this).find('.images-container .image-link').each(function () {
//       var imageUrl = $(this).attr('href'); // Lấy đường dẫn hình ảnh
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

// $(".btn_train_model").click(function () {
//   loadingEle.show();
//   let trainingData = { 'trainingData': getImageData(), 'setting': JSON.parse(localStorage.getItem("setting")) }
//   console.log(trainingData)
//   fetch('/train-model2', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify(trainingData)
//   })
//     .then(response => {
//       loadingEle.hide();
//       return response.json();
//     })
//     .then(async data => {
//       var uuid = data.uuid
//       model = await tf.loadLayersModel(`http://127.0.0.1:8000/static/uploads/${uuid}/model.json`);
//       console.log('Load model');
//       //        console.log(model.summary());
//       console.log(data); // In ra kết quả từ server
//     })
//     .catch(error => {
//       console.error('Error:', error);
//     });
// })
// var LIST = [
//   'airplane', 'automobile', 'bird', 'cat', 'deer',
//   'dog', 'frog', 'horse', 'ship', 'truck'
// ];
// var LIST = [
//   '0', '1', '2', '3', '4',
//   '5', '6', '7', '8', '9'
// ];

// $("#btn_predict").click(async function () {
//   await loadingEle.show();

//   var uuid = localStorage.getItem("uuid")
//   model = await tf.loadLayersModel(`http://127.0.0.1:8000/static/uploads/${uuid}/model.json`);
//   // 1. Chuyen anh ve tensor
//   let image = $('#imagePreview')[0];
//   let img = tf.browser.fromPixels(image);
//   let normalizationOffset = tf.scalar(255); // 127.5
//   let tensor = await img
//     .resizeNearestNeighbor([28, 28])
//     .toFloat()
//     .sub(normalizationOffset)
//     .div(normalizationOffset)
//     .reverse(2)
//     .expandDims();
//   // 2. Predict
//   let predictions = await model.predict(tensor);
//   predictions = predictions.dataSync();
//   let result = await Array.from(predictions)
//     .map(function (p, i) {
//       return {
//         probability: (p * 100).toFixed(1),
//         className: LIST[i]
//       };
//     })
//   // .sort(function (a, b) {
//   //   return b.probability - a.probability;
//   // });
//   console.log(result);
//   await loadingEle.hide();
//   let html = ``
//   result.forEach((item) => {
//     html += `
//         <div class="d-flex justify-content-between align-items-center">
//         <h6 class="mb-0" style="width: 30%">${item.className}</h6>
//         <div class="progress mb-3" style="width:70%; height: 29px; border-radius: 6px">
//           <div class="progress-bar" role="progressbar" style="width: ${item.probability}%; color: #000;" aria-valuenow="${item.probability}" aria-valuemin="0" aria-valuemax="100">
//             ${item.probability}%
//           </div>
//         </div>
//       </div>
//         `
//   })
//   $("#output").html(html)
//   changeColorProcessBar()
// });

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
});