$(document).ready(function() {
  $(".thermostat-submit").click(function() {
    var button = this;

    $.ajax({
      type: "POST",
      url: "/update_thermostat",
      data: $(button.parentNode).serialize(),
      beforeSend: function() {
        $(button).prop("disabled", true);
      }
    }).done(function() {
      $(button).prop("disabled", false);
    });
  });
});

function pollThermostat(pk) {
  $.getJSON("/poll_thermostat/" + pk, function(response) {
    $("#temperature-" +pk).text(response.temperature);
    $("#actuated-" + pk).text((response.actuated ? "True" : "False"));
  });

  setTimeout(pollThermostat, 10000, pk);
}
