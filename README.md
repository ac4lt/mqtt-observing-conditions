This is an ASCOM Alpaca Observing Conditions driver to take weather data that has been published to MQTT by other applications and present it to astronomy applications in the form of an
ASCOM Alpaca driver.

In the author's use case data is primarily coming from an Ambient Weather WS-2000 weather station along with a Unihedron SQM-LE sky quality meter.

The application FOSHKplugin actually publishes the weather station to MQTT while the SQM data is published to MQTT from a standalone astro dashboard. However, from the point of view 
of this driver, it doesn't matter where the data is coming from, only that it is available via a subscription on MQTT.

Currently, this is hard coded to be specific to the topics that FOSHKplugin and the dashboard use, however, the plan is to make it configurable in the future.

TODO:
- containerize the application
- make topics configurable
- write instructions on hooking up to applications
- 
