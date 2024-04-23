
$(document).ready(function () {
  changeColorProcessBar();
  console.log(LIST)
  $("#btn_predict").click(async function () {
    await loadingEle.show();

    var uuid = localStorage.getItem("uuid")
    model = await tf.loadLayersModel(`http://127.0.0.1:8000/static/uploads/${uuid}/model.json`);
    // 1. Chuyen anh ve tensor
    let image = $('#imagePreview')[0];
    let img = tf.browser.fromPixels(image);
    let normalizationOffset = tf.scalar(255);
    let tensor = await img
      .resizeNearestNeighbor([112, 112])
      .toFloat()
      .sub(normalizationOffset)
      .div(normalizationOffset)
      .reverse(2)
      .expandDims();
    /*
    
    */
    // 2. Predict
    let predictions = await model.predict(tensor);
    predictions = predictions.dataSync();
    console.log(predictions)
    let sum = 0;
    let maxPerIndex = 0
    let maxPer = 0
    console.log(LIST)
    let result = await Array.from(predictions)
      .map(function (p, i) {
        let per = (p * 100).toFixed(1)
        if (maxPer < per) {
          maxPer = per
          maxPerIndex = i
        }
        sum += per
        return {
          probability: per,
          className: LIST[i]
        };
      });
    if (sum < 100) {
      result[maxPerIndex].probability += 0.1
    } else if (sum > 100) {
      result[maxPerIndex].probability -= 0.1
    }
    // .sort(function (a, b) {
    //   return b.probability - a.probability;
    // });
    console.log(result);
    await loadingEle.hide();
    let html = ``
    result.forEach((item) => {
      html += `
      <div class="d-flex justify-content-between align-items-center mb-3">
      <h6 class="mb-0 mr-3" style="width: 30%">${item.className}</h6>
      <div class="progress" style="width:70%; height: 29px; border-radius: 6px">
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

  $("#btn_predictt").click(function () {
    // var formData = new FormData($("#form_predict")[0]);
    var formData = new FormData();
    formData.append('image', $('input[type=file]')[0].files[0]);
    formData.append('dataset', 'cifar-10');
    console.log(formData)
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
      headers: {
        'X-CSRFToken': csrftoken
      }
    });
    $.ajax({

      url: "/predict",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        // Handle success response
        console.log(response);

        let html = ``
        response.forEach((item, index) => {

          html += `
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h6 class="mb-0" style="width: 30%">${item.name}</h6>
                        <div class="progress" style="width: 70%; height: 29px; border-radius: 6px">
                            <div class="progress-bar" role="progressbar" style="width: ${item.accuracy * 100}%; color: #000;" aria-valuenow="${item.accuracy * 100}" aria-valuemin="0" aria-valuemax="100">
                                ${Math.round(item.accuracy * 100)}%
                            </div>
                        </div>
                    </div>
                `
        })
        $("#output").empty();
        $("#output").html(html)
        changeColorProcessBar();
      },
      error: function (xhr, status, error) {
        // Handle error
        console.log(error)
        // ShowToast(jQuery.parseJSON(xhr.responseText)?.image[0])
      }
    });
  });
  // $("select").select2({
  //   width: "resolve",
  // });

  Fancybox.bind("[data-fancybox]", {
    groupAll: true,
    buttons: ["zoom", "slideShow", "fullScreen", "thumbs", "close"],
    loop: true,
    protect: true,
  });

  $("#customSwitch").change(function () {
    let label_ele = $("#customSwitch").siblings("label");
    console.log();
    if (label_ele.text().trim() == "ON") {
      label_ele.text("OFF");
    } else {
      label_ele.text("ON");
    }
  });


  function ShowToast(text = "This is Toast") {
    Toastify({
      text: text,
      duration: 3000,
      newWindow: true,
      close: true,
      gravity: "top", // `top` or `bottom`
      position: "right", // `left`, `center` or `right`
      stopOnFocus: true, // Prevents dismissing of toast on hover
      style: {
        background: "linear-gradient(to right, #00b09b, #96c93d)",
        color: "#fff" // Màu chữ
      },
      onClick: function () { } // Callback sau khi click
    }).showToast();
  }

});

function getImageData() {
  let imageData = [];
  $('.class_item').each(function () {
    var label = $(this).find('h5').text().trim();
    var images = [];

    $(this).find('.images-container img').each(function () {
      var imageUrl = $(this).attr('src');
      images.push(imageUrl);
    });

    var imageDataItem = {
      label: label,
      images: images
    };

    imageData.push(imageDataItem);
  });

  return imageData;
}

$(".btn_train_model").click(function () {
  loadingEle.show();
  let trainingData = { 'trainingData': getImageData(), 'setting': JSON.parse(localStorage.getItem("setting")) }
  console.log(trainingData)
  fetch('/train-model2', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(trainingData)
  })
    .then(response => {
      loadingEle.hide();
      return response.json();
    })
    .then(async data => {
      var uuid = data.uuid
      model = await tf.loadLayersModel(`http://127.0.0.1:8000/static/uploads/${uuid}/model.json`);
      console.log('Load model');
      //        console.log(model.summary());
      console.log(data); // In ra kết quả từ server
    })
    .catch(error => {
      console.error('Error:', error);
    });
})