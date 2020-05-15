// Set constraints for the video stream
//IF facingMode to user then front cammera and if environment then back
//{ audio: true, video: { facingMode: { exact: "environment" } } }
//{ audio: true, video: { facingMode: "user" } }
var constraints = { video: {facingMode:{exact: 'environment'}}, audio: false };
var track = null;

// Define constants
const cameraView = document.querySelector("#camera--view"),
    cameraOutput = document.querySelector("#camera--output"),
    cameraSensor = document.querySelector("#camera--sensor"),
    cameraTrigger = document.querySelector("#camera--trigger");

var select = document.createElement("select");
var frag = document.createDocumentFragment();
var language = document.querySelector('.caption1')

var flag = 0;

//Language MAP
const langMap = {
    english: 'en',
    spanish: 'es',
    german: 'de',
    french: 'fr',
    chinese: 'zh',
    italian: 'it',
    korean: 'ko',
    japanese: 'ja',
    dutch: 'nl',
    hindi: 'hi'
  }

// Access the device camera and stream to cameraView
function cameraStart() {
    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) 
    {
        track = stream.getTracks()[0];
        cameraView.srcObject = stream;
    })
    .catch(function(error) 
    {
        console.error("Oops. Something is broken.", error);
    });
}

// Take a picture when cameraTrigger is tapped
cameraTrigger.onclick = function() {

    //$('.loader').show();

    cameraSensor.width = cameraView.videoWidth;
    cameraSensor.height = cameraView.videoHeight;
    cameraSensor.getContext("2d").drawImage(cameraView, 0, 0);
    cameraOutput.src = cameraSensor.toDataURL("image/png");
    //console.log(cameraOutput.src);
    console.log("YOYO");

    //AJAX call for sending data and fetching it
    $.post("/predict",{data: cameraOutput.src.split(",")[1]})
    .done(function( trans ) {
            $('#result').fadeIn(600);
            $('#result2').fadeIn(600);
            $('#result').text(trans.split("-")[0]);
            console.log(trans);
            $('#result2').text(trans.split("-")[1]);
            $('.caption1')[0].style.display='block';

            if(flag==0)
            {
                select.options.add( new Option("French:","1", true, true) );
                select.options.add( new Option("German:","4") );
                select.options.add( new Option("Spanish:","2") );
                select.options.add( new Option("Italian:","3") );
                
                frag.appendChild(select);
                language.appendChild(frag);
                flag=1;
            }
            

            console.log('Success!');
      });   

    cameraOutput.classList.add("taken");
    //track.stop();
};

// select.onChange(function(){
//     console.log( select.options[select.selectedIndex].value)
// })

select.addEventListener('change', function() {
    console.log('You selected: ', this.value);
    $.post("/otherlang",{lan:this.value, sen:document.getElementById('result2').outerText})
    .done(function(tran){
        console.log("moshi")
        console.log(tran)
        // $('#result2').text(tran.split("-")[1]);  
    })
});

// Start the video stream when the window loads
window.addEventListener("load", cameraStart, false);


if('serviceWorker' in navigator){
    navigator.serviceWorker.register('/sw.js')
      .then(reg => console.log('service worker registered'))
      .catch(err => console.log('service worker not registered', err));
  }