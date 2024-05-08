
$(document).ready(function () {
  let searchParams = new URLSearchParams(window.location.search)
  $(`select option[value="${searchParams.get('sizes')}"]`).attr("selected", true);
  $("#size_image").change(function () {
    let sizes = $(this).val()
    let url = $(location).attr('pathname') + "?sizes=" + sizes;
    window.location.assign(url)
  })
  changeColorProcessBar();
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

    var uuid = localStorage.getItem("uuid")
    model = await tf.loadLayersModel(`http://127.0.0.1:8000/static/uploads/${uuid}/model.json`);
    // 1. Chuyen anh ve tensor
    let image = $('#imagePreview')[0];
    let tensor = await convertImageToTensor(image)
    // 2. Predict
    let predictions = await model.predict(tensor);
    predictions = predictions.dataSync();
    console.log(predictions)
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
          className: LIST[i]
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
    let html = ``
    result.forEach((item, index) => {
      html += `
      <div class="d-flex justify-content-between align-items-center mb-3">
      <h6 class="mb-0 mr-3" style="width: 30%">${item.className}</h6>
      <div class="progress" style="width:60%; height: 29px; border-radius: 6px">
        <div class="progress-bar" role="progressbar" style="width: ${item.probability}%; color: ${item.probability > 15 ? `#fff` : `#000`};" aria-valuenow="${item.probability}" aria-valuemin="0" aria-valuemax="100">
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

    changeColorProcessBar()

  });
  Fancybox.bind("[data-fancybox]", {
    groupAll: true,
    buttons: ["zoom", "slideShow", "fullScreen", "thumbs", "close"],
    loop: true,
    protect: true,
  });

  // $("#customSwitch").change(function () {
  //   let label_ele = $("#customSwitch").siblings("label");
  //   console.log();
  //   if (label_ele.text().trim() == "ON") {
  //     label_ele.text("OFF");
  //   } else {
  //     label_ele.text("ON");
  //   }
  // });
});

// function getImageData() {
//   let imageData = [];
//   $('.class_item').each(function () {
//     var label = $(this).find('h5').text().trim();
//     var images = [];

//     $(this).find('.images-container img').each(function () {
//       var imageUrl = $(this).attr('src');
//       images.push(imageUrl);
//     });

//     var imageDataItem = {
//       label: label,
//       images: images
//     };

//     imageData.push(imageDataItem);
//   });

//   return imageData;
// }

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
      console.log(data); // In ra kết quả từ server
      saveUuid(data?.uuid)
      export_model(uuid);
    })
    .catch(error => {
      console.error('Error:', error);
    });
})

