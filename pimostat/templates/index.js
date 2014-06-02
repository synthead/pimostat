$(".thermostat-submit").click(function() {
  var button = this;
  var pk = this.id.replace(/submit-/, "");

  $.ajax({
    type: "POST",
    url: "/update_thermostat",
    data: $(button.parentNode).serialize(),
    beforeSend: function() {
      clearInterval(pollers[pk]);
      $(button).prop("disabled", true);
    }
  }).done(function() {
    pollThermostat(pk);
    $(button).prop("disabled", false);
  });
});

var update_frequency = {{ update_frequency }} * 1000;

var pollers = {
    {% for form in thermostat_formset %}
      {{ form.instance.pk}}: setTimeout(
          pollThermostat, update_frequency, {{ form.instance.pk }}),
    {% endfor %}
};

function pollThermostat(pk) {
  pollers[pk] = setTimeout(pollThermostat, update_frequency, pk);

  $.getJSON("/poll_thermostat/" + pk, function(response) {
    $("#temperature-" +pk).text(response.temperature);
    $("#actuated-" + pk).text((response.actuated ? "True" : "False"));
  });
}
