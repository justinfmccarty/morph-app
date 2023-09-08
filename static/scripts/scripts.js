// import { FileSaver } from 'file-saver';
// import JSZip from 'jszip'

// when page is too small activate the responsive nav menu
function openResponsive() {
  var x = document.getElementById("mainNav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}

// function logSubmit(event) {
//   console.log(`Form Submitted! Timestamp: ${event.timeStamp}`);
// }

// const configForm = document.getElementById("configuration")
// configForm.addEventListener("submit", function (e) {
//   e.preventDefault();

//   const data = new FormData(configForm);
//   let temp = document.getElementById("temp-output")
//   temp.innerText = "---" + "\n"
//   for (const [name, value] of data) {
//     console.log(name, ":", value)
//     temp.innerText += name + ":" + value + "\n"
//   }
//   console.log(data.innerText)
//   // submitFormFlask()
//   // console.log("function run")
// })

// $(document).on('submit', '#configuration', function (e) {
//   const configForm = document.getElementById("configuration")
//   e.preventDefault();
//   $.ajax({
//     type: 'POST',
//     url: '/morpher',
//     data: $('#configuration').serialize(),
//     success: function () {
//       const myForm = new FormData(configForm);
//       let temp = document.getElementById("temp-output")
//       temp.innerText = "---" + "\n"
//       for (const [name, value] of myForm) {
//         temp.innerText += name + ":" + value + "\n"
//       }

//     }
//   })
// });

// $(document).ready(function () {
//   // Wait for the content to load.
//   $("form[name='configuration']").submit(function (evt) {
//     // If the form is to be submitted, ignore the standard behavior.
//     evt.preventDefault();
//     // Serialize the inputs to an array.
//     let inputFields = $(this).serializeArray();
//     // Send the data as JSON via AJAX.
//     $.ajax({
//       method: "POST",
//       url: "/morpher",
//       contentType: "application/json;charset=utf-8",
//       dataType: "json",
//       data: JSON.stringify({ input_fields: inputFields })
//     }).done(data => {
//       // Use the response here.
//       console.log(data);
//     });
//   });
// });

$(function() {
  $('#submit-form').click(function() {
      const configForm = document.getElementById("configuration")
      const downloadBtn = document.getElementById("exec-get-results")
      var form_data = new FormData($('#configuration')[0]);
      configForm.querySelector('.loader-container').style.display = 'block';
      $.ajax({
          type: 'POST',
          url: '/morpher',
          data: form_data,
          contentType: false,
          cache: false,
          processData: false,
          success: function() {
            // console.log(data)
            downloadBtn.style.display = "inline";
            // downloadBtn.href = data.filename;
            // Download(data.filename)
            const myForm = new FormData(configForm);
            let temp = document.getElementById("temp-output")
            temp.innerText = "---" + "\n"
            for (const [name, value] of myForm) {
              temp.innerText += name + ":" + value + "\n"
            };
            console.log("start zip");
            // makeZip(data);
            // Download();
            // Object.keys(data).forEach(function(key) {
            //   console.log('Key : ' + key + ', Value : ' + data[key])
            //   downloadTxt(key, data[key]);
            // })
            configForm.querySelector('.loader-container').style.display = 'none';
            console.log("end zip");
          },
      });
  });
});

function Download() {
  var zip_file_path = "../ssps.jpg"
  var zip_file_name = "s_d.jpg"
  var a = document.createElement("a");
  document.body.appendChild(a);
  a.style = "display: none";
  a.href = zip_file_path;
  a.download = zip_file_name;
  a.click();
  document.body.removeChild(a);
}

function downloadTxt(filename, text) {
  // console.log(data)
  
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
  
  
}

// TYPEWRITER STUFF
var text = $('.typewriter').text();
var length = text.length;
var timeOut;
var character = 0;

(function typeWriter() {
  timeOut = setTimeout(function () {
    character++;
    var type = text.substring(0, character);
    $('.typewriter').text(type);
    typeWriter();

    if (character == length) {
      clearTimeout(timeOut);
    }

  }, 150);
}());


function submitFormFlask() {
  const response = fetch('/form-to-json')
}


function execGetResults() {
  fetch('/exec-get-results')
}

// function makeZip(data) {
//   console.log(data)
//   var zip = new JSZip();
//   console.log("package started")
//   zip.file("file1.txt", "hello world");
//   zip.file("file2.txt", "hello world again");
//   zip.generateAsync({ type: 'blob' }).then(function (content) {
//       FileSaver.saveAs(content, 'download.zip');
//   });
// }


// function showDiv() {
//   document.getElementById('welcomeDiv').style.display = "block";
// }


// function redraw(_id, endpoint) {
//   fetch(endpoint)
//     .then(function(response){return response.text();})
//     .then(function(data){
//             document.getElementById(welcomeDiv).style.display = "none";
//         }
//     )
// }

// $(document).ready( function() {
//     $('#submit-form').click(function() {
//         $.ajax("{{ url_for('morpher') }}").done(function (reply) {
//           $('#welcomeDiv').css({'display': 'none'});
//           // $('#welcomeDiv').html(reply);
//         });
//     });
// });

// async function execGetCMIP() {
//   const response = await fetch('/exec-get-cmip');
// }

// function execMorphEPW() {
//   let data = sessionStorage.getItem("myData");
//   console.log(data)
//   fetch('/exec-morph-epw')
// }
