var buttonRecord = document.getElementById("record");
var buttonStop = document.getElementById("stop");


buttonStop.disabled = true;

buttonRecord.onclick = function() {
    // var url = window.location.href + "record_status";
    buttonRecord.disabled = true;
    buttonStop.disabled = false;
    
    // disable download link
    var downloadLink = document.getElementById("download");
    downloadLink.text = "";
    downloadLink.href = "";

    // XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // alert(xhr.responseText);
        }
    }

    // get user input select ROI id
    var X = document.getElementById("start_X").value;
    var Y = document.getElementById("start_Y").value;
    var h = document.getElementById("height").value;
    var w = document.getElementById("width").value;
    var roi={
        status:'true',
        x:X,
        y:Y,
        w:w,
        h:h,
    };
    
    xhr.open("POST", "/record_status");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify(roi));
    
};

buttonStop.onclick = function() {
    buttonRecord.disabled = false;
    buttonStop.disabled = true;    

    // XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // alert(xhr.responseText);

            // enable download link
            var downloadLink = document.getElementById("download");
            downloadLink.text = "Download Video";
            downloadLink.href = "/static/video.avi";
        }
    }

    var X = document.getElementById("start_X").value;
    var Y = document.getElementById("start_Y").value;
    var h = document.getElementById("height").value;
    var w = document.getElementById("width").value;
    var roi={
        status:'false',
        x:X,
        y:Y,
        w:w,
        h:h,
    };
    console.log(roi);
    xhr.open("POST", "/record_status");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify(roi));
};


