
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# observingconditions.py - Alpaca API responders for Observingconditions
#
# Author:   Your R. Name <your@email.org> (abc)
#
# -----------------------------------------------------------------------------
# Edit History:
#   Generated by Python Interface Generator for AlpycaDevice
#
# ??-???-????   abc Initial edit

from falcon import Request, Response, HTTPBadRequest, before
from logging import Logger
from shr import PropertyResponse, MethodResponse, PreProcessRequest, \
                get_request_field, to_bool
from exceptions import *        # Nothing but exception classes
from mqttobservingconditions import MQTTObservingConditions

logger: Logger = None

# ----------------------
# MULTI-INSTANCE SUPPORT
# ----------------------
# If this is > 0 then it means that multiple devices of this type are supported.
# Each responder on_get() and on_put() is called with a devnum parameter to indicate
# which instance of the device (0-based) is being called by the client. Leave this
# set to 0 for the simple case of controlling only one instance of this device type.
#
maxdev = 0                      # Single instance

# -----------
# DEVICE INFO
# -----------
# Static metadata not subject to configuration changes
## EDIT FOR YOUR DEVICE ##
class ObservingconditionsMetadata:
    """ Metadata describing the Observingconditions Device. Edit for your device"""
    Name = 'MQTT Observing Conditions'
    Version = '1.2.1'
    Description = 'Get current observing conditions from weather data via MQTT subscription'
    DeviceType = 'Observingconditions'
    DeviceID = '6cf676ff-22c1-4f4b-992a-5779d94b692b' # https://guidgenerator.com/online-guid-generator.aspx
    Info = 'Alpaca MQTT Observing Conditions\nImplements IObservingconditions\nLinda Thomas-Fowler'
    MaxDeviceNumber = maxdev
    InterfaceVersion = 1       # IObservingconditionsVxxx

mqttoc = None
def start_oc_device(logger: logger):
    logger = logger
    global mqttoc
    mqttoc = MQTTObservingConditions(logger)

# --------------------
# RESOURCE CONTROLLERS
# --------------------

@before(PreProcessRequest(maxdev))
class action:
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class commandblind:
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class commandbool:
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class commandstring:
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class connected:
    def on_get(self, req: Request, resp: Response, devnum: int):
        # -------------------------------
        is_conn = mqttoc.isConnected() 
        ### READ CONN STATE ###
        # -------------------------------
        resp.text = PropertyResponse(is_conn, req).json

    def on_put(self, req: Request, resp: Response, devnum: int):
        conn_str = get_request_field('Connected', req)
        conn = to_bool(conn_str)              # Raises 400 Bad Request if str to bool fails
        try:
            # --------------------------------
            ### CONNECT/DISCONNECT()PARAM) ###
            # --------------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req, DriverException(0x500, 'Observingconditions.Connected failed', ex)).json

@before(PreProcessRequest(maxdev))
class description:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(ObservingconditionsMetadata.Description, req).json

@before(PreProcessRequest(maxdev))
class driverinfo:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(ObservingconditionsMetadata.Info, req).json

@before(PreProcessRequest(maxdev))
class interfaceversion:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(ObservingconditionsMetadata.InterfaceVersion, req).json

@before(PreProcessRequest(maxdev))
class driverversion():
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(ObservingconditionsMetadata.Version, req).json

@before(PreProcessRequest(maxdev))
class name():
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(ObservingconditionsMetadata.Name, req).json

@before(PreProcessRequest(maxdev))
class supportedactions:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse([], req).json  # Not PropertyNotImplemented

@before(PreProcessRequest(maxdev))
class averageperiod:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not mqttoc.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # ----------------------
            val = mqttoc.averageperiod
            ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Observingconditions.Averageperiod failed', ex)).json

    def on_put(self, req: Request, resp: Response, devnum: int):
        if not mqttoc.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        averageperiodstr = get_request_field('AveragePeriod', req)      # Raises 400 bad request if missing
        try:
            averageperiod = float(averageperiodstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'AveragePeriod " + averageperiodstr + " not a valid number.')).json
            return
        ### RANGE CHECK AS NEEDED ###         # Raise Alpaca InvalidValueException with details!
        if averageperiod != 0:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'AveragePeriod " + averageperiodstr + " only zero is valid.')).json     
        else:
            try:
                # -----------------------------
                ### DEVICE OPERATION(PARAM) ###
                # -----------------------------
                mqttoc.averageperiod = averageperiod
                resp.text = MethodResponse(req).json
            except Exception as ex:
                resp.text = MethodResponse(req,
                                DriverException(0x500, 'Observingconditions.Averageperiod failed', ex)).json

@before(PreProcessRequest(maxdev))
class cloudcover:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not mqttoc.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # ----------------------
            val = mqttoc.cloudCover
             ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Observingconditions.Cloudcover failed', ex)).json

@before(PreProcessRequest(maxdev))
class dewpoint:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not mqttoc.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # ----------------------
            val = mqttoc.dewPoint
            ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Observingconditions.Dewpoint failed', ex)).json

@before(PreProcessRequest(maxdev))
class humidity:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not mqttoc.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # ----------------------
            val = mqttoc.humidity
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Observingconditions.Humidity failed', ex)).json

@before(PreProcessRequest(maxdev))
class pressure:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not mqttoc.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # ----------------------
            val = mqttoc.pressure
            ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Observingconditions.Pressure failed', ex)).json

@before(PreProcessRequest(maxdev))
class rainrate:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not mqttoc.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # ----------------------
            val = mqttoc.rainRate
            ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Observingconditions.Rainrate failed', ex)).json

@before(PreProcessRequest(maxdev))
class skybrightness:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not mqttoc.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # ----------------------
            val = mqttoc.skyBrightness
            ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Observingconditions.Skybrightness failed', ex)).json

@before(PreProcessRequest(maxdev))
class skyquality:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not mqttoc.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # ----------------------
            val = mqttoc.skyQuality
            ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Observingconditions.Skyquality failed', ex)).json

@before(PreProcessRequest(maxdev))
class skytemperature:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not mqttoc.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        resp.text = PropertyResponse(None, req,
                            NotImplementedException("This hardware does not supply sky temperature")).json

@before(PreProcessRequest(maxdev))
class starfwhm:

    def on_get(self, req: Request, resp: Response, devnum: int):    
        resp.text = PropertyResponse(None, req,
                            NotImplementedException("This hardware does not supply star fwhm")).json

@before(PreProcessRequest(maxdev))
class temperature:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not mqttoc.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # ----------------------
            val = mqttoc.temperature
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Observingconditions.Temperature failed', ex)).json

@before(PreProcessRequest(maxdev))
class winddirection:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not mqttoc.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # ----------------------
            val = mqttoc.windDirection
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Observingconditions.Winddirection failed', ex)).json

@before(PreProcessRequest(maxdev))
class windgust:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not mqttoc.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # ----------------------
            val = mqttoc.windGust
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Observingconditions.Windgust failed', ex)).json

@before(PreProcessRequest(maxdev))
class windspeed:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not mqttoc.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # ----------------------
            val = mqttoc.windSpeed
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Observingconditions.Windspeed failed', ex)).json

@before(PreProcessRequest(maxdev))
class refresh:

    def on_put(self, req: Request, resp: Response, devnum: int):
        if not mqttoc.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            resp.text = MethodResponse(req, NotImplementedException("Unable to refresh. Data arrives at its own rate.")).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Observingconditions.Refresh failed', ex)).json

@before(PreProcessRequest(maxdev))
class sensordescription:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not mqttoc.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            match req.params['SensorName']:
                case "CloudCover":
                    val = "Percentage of the sky covered by clouds."
                case "DewPoint":
                    val = "Dew point in degrees Celsius"
                case "Humidity":
                    val = "Relative humidity as a precentage"
                case "Pressure":
                    val = "Barometric pressure in hpa"
                case "RainRate":
                    val = "Rain rate in mm/hour"
                case "SkyBrightness":
                    val = "Sky Brightness in lux"
                case "SkyQuality":
                    val = "Sky quality in magnitudes per arcsecond squared"
                case "SkyTemperature":
                    val = None
                case "StarFWHM":
                    val = None
                case "Temperature":
                    val = "Temperature in degrees Celsius"
                case "WindDirection":
                    val = "Wind direction in degrees clockwise from north"
                case "WindGust":
                    val = "Wind Gust in m/s"
                case "WindSpeed":
                    val = "Wind speed in m/s"
                case _:
                    val = "not implemented yet"
            if val != None:
                resp.text = PropertyResponse(val, req).json
            else:
                resp.text = PropertyResponse(None, req,
                                             NotImplementedException(f"{req.params['SensorName']} is not supported")).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Observingconditions.Sensordescription failed', ex)).json

@before(PreProcessRequest(maxdev))
class timesincelastupdate:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not mqttoc.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            match req.params['SensorName']:
                case "":
                    val = mqttoc.lastUpdate                
                case "CloudCover":
                    val = mqttoc.lastCloudCoverUpdate
                case "DewPoint":
                    val = mqttoc.lastDewPointUpdate
                case "Humidity":
                    val = mqttoc.lastHumidityUpdate
                case "Pressure":
                    val = mqttoc.lastPressureUpdate
                case "RainRate":
                    val = mqttoc.lastRainRateUpdate
                case "SkyBrightness":
                    val = mqttoc.lastSkyBrightnessUpdate
                case "SkyQuality":
                    val = mqttoc.lastSkyQualityUpdate
                case "Temperature":
                    val = mqttoc.lastTemperatureUpdate
                case "WindDirection":
                    val = mqttoc.lastWindDirectionUpdate
                case "WindGust":
                    val = mqttoc.lastWindGustUpdate
                case "WindSpeed":
                    val = mqttoc.lastWindSpeedUpdate
                case _:
                    val = None
            if val != None:
                resp.text = PropertyResponse(val, req).json
            else:
                resp.text = PropertyResponse(None, req,
                                             NotImplementedException(f"{req.params['SensorName']} is not supported")).json                
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Observingconditions.Timesincelastupdate failed', ex)).json

@before(PreProcessRequest(maxdev))
class connected:
    """Retrieves or sets the connected state of the device

    * Set True to connect to the device hardware. Set False to disconnect
      from the device hardware. Client can also read the property to check
      whether it is connected. This reports the current hardware state.
    * Multiple calls setting Connected to true or false must not cause
      an error.

    """
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(mqttoc.connected, req).json

    def on_put(self, req: Request, resp: Response, devnum: int):
        conn_str = get_request_field('Connected', req)
        conn = to_bool(conn_str)              # Raises 400 Bad Request if str to bool fails

        try:
            # ----------------------
            mqttoc.connected = conn
            # ----------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req, # Put is actually like a method :-(
                            DriverException(0x500, 'Rotator.Connected failed', ex)).json