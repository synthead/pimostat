import mysql.connector


# class MySQLCursorDict(mysql.connector.cursor.MySQLCursor):
#   def _row_to_python(self, rowdata, desc=None):
#     row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
#
#     if row:
#       return dict(zip(self.column_names, row))
#
#     return None


class ThermostatAPI:
  def __init__(self, database_config):
    self.connection = mysql.connector.connect(**database_config)
    self.connection.autocommit = True

  def GetActiveSensors(self):
    cursor = self.connection.cursor()
    cursor.execute("""
      SELECT
        id,
        serial

      FROM
        sensors

      WHERE
        enabled = 1
    """)
    sensors = cursor.fetchall()
    cursor.close()

    return sensors

  def GetActiveRelays(self):
    cursor = self.connection.cursor()
    cursor.execute("""
      SELECT
        id,
        channel,
        state

      FROM
        relays

      WHERE
        enabled = true
    """)
    relays = cursor.fetchall()
    cursor.close()

    return relays

  def UpdateSensorTemperature(self, sensor_id, temperature):
    cursor = self.connection.cursor()
    cursor.execute("""
      UPDATE
        sensors

      SET
        temperature = %s

      WHERE
        id = %s
    """, (temperature, sensor_id))
    cursor.close()

  def UpdateRelayState(self, relay_id, state):
    cursor = self.connection.cursor()
    cursor.execute("""
      UPDATE
        relays

      SET
        state = %s

      WHERE
        id = %s
    """, (state, relay_id))
    cursor.close()

  def GetRelayEvents(self):
    cursor = self.connection.cursor()
    cursor.execute("""
      SELECT
        relays.id,
        relays.channel,
        ! relays.state,
        relays.enabled

      FROM
        thermostats

        JOIN relays
          ON relays.id = thermostats.relay_id

        JOIN sensors
          ON sensors.id = thermostats.sensor_id

      WHERE
        (
          (
            relays.enabled = false
            OR sensors.enabled = false
            OR thermostats.enabled = false
            OR sensors.temperature >= thermostats.desired_temperature +
              thermostats.upper_deviation
          ) AND relays.state = true
        ) OR (
          relays.enabled = true
          AND sensors.enabled = true
          AND thermostats.enabled = true
          AND sensors.temperature <= thermostats.desired_temperature -
            thermostats.lower_deviation
          AND relays.state = false
        )
    """)
    events = cursor.fetchall()
    cursor.close()

    return events
