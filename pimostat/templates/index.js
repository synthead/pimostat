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

var update_frequency = {{ update_frequency }} * 1000;

{% for form in thermostat_formset %}
  setTimeout(pollThermostat, update_frequency, {{ form.instance.pk }});
{% endfor %}

function pollThermostat(pk) {
  $.getJSON("/poll_thermostat/" + pk, function(response) {
    $("#temperature-" +pk).text(response.temperature);
    $("#actuated-" + pk).text((response.actuated ? "True" : "False"));
  });

  setTimeout(pollThermostat, update_frequency, pk);
}
