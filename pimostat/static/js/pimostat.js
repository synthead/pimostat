function pollThermostat(pk) {
  var ajax = new XMLHttpRequest();

  ajax.onreadystatechange = function() {
    if (ajax.readyState == 4) {
      if (ajax.status == 200) {
        var response = JSON.parse(ajax.responseText);

        document.getElementById(
            "temperature-" + pk).innerHTML = response.temperature;
        document.getElementById("actuated-" + pk).innerHTML = (
            response.actuated ? "True" : "False");

        setTimeout(pollThermostat, 5000, pk);
      }
    }
  }

  ajax.open("GET", "/poll_thermostat/" + pk, true);
  ajax.send();
}
