function pollSensor(pk) {
  var ajax = new XMLHttpRequest();

  ajax.onreadystatechange = function() {
    if (ajax.readyState == 4) {
      if (ajax.status == 200) {
        document.getElementById(
            "sensor-" + pk + "-temperature").innerHTML = ajax.responseText;
        setTimeout(pollSensor, 5000, pk);
      }
    }
  }

  ajax.open("GET", "/get_temperature/" + pk, true);
  ajax.send();
}
