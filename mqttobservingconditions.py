# ASCOM Alpaca Observing Conditions low level device
#
# This class is meant to be used from the high level ObservingConditions class
#
# linda 2023-12-25 initial coding

import paho.mqtt.client as mqtt
import time
from logging import Logger
from threading import Lock
from config import Config

class MQTTObservingConditions:

    # lock
    _lock = None

    # observing conditions values
    _cloudCover = 0
    _dewPoint = -273
    _humidity = 0
    _pressure = 0
    _rainRate = 0
    _skyBrightness = 0
    _skyQuality = 0
    _temperature = -273
    _windDirection = 0
    _windGust = 0
    _windSpeed = 0

    # average period (seconds)
    _averageperiod = 0

    # last update time for the values
    _lastCloudCoverUpdate = 0
    _lastDewPointUpdate = 0
    _lastHumidityUpdate = 0
    _lastPressureUpdate = 0
    _lastRainRateUpdate = 0
    _lastSkyBrightnessUpdate = 0
    _lastSkyQualityUpdate = 0
    _lastTemperatureUpdate = 0
    _lastWindDirectionUpdate = 0
    _lastWindGustUpdate = 0
    _lastWindSpeedUpdate = 0   

    # to calculate rain rate
    last_rain_reading = 0
    current_rain_reading = 0
    last_rain_time = 0
    current_rain_time = 0


    def __init__(self, logger):
        # internal state
        self.logger = logger
        self._connected = False
        self._lock = Lock()
        # MQTT client
        self.client = mqtt.Client("MQTTObservingConditions", userdata = self)
        self.client.username_pw_set(Config.mqtt_user, Config.mqtt_password)
        self.client.connect(Config.mqtt_server, Config.mqtt_port)
        # add callbacks
        self.client.message_callback_add(Config.topic_cloud_cover, on_message_cloud_cover)  
        self.client.message_callback_add(Config.topic_dew_point, on_message_dew_point)  
        self.client.message_callback_add(Config.topic_event_rain, on_message_event_rain)        
        self.client.message_callback_add(Config.topic_humidity, on_message_hummidity)     
        self.client.message_callback_add(Config.topic_pressure, on_message_pressure)   
        self.client.message_callback_add(Config.topic_solar_radiation, on_message_solar_radiation)
        self.client.message_callback_add(Config.topic_sqm, on_message_sqm)
        self.client.message_callback_add(Config.topic_temperature, on_message_temperature)
        self.client.message_callback_add(Config.topic_wind_direction, on_message_wind_direction)
        self.client.message_callback_add(Config.topic_wind_gust, on_message_wind_gust)
        self.client.message_callback_add(Config.topic_wind_speed, on_message_wind_speed)
        # subscriptions
        self.client.subscribe(Config.topic_cloud_cover)
        self.client.subscribe(Config.topic_dew_point)     
        self.client.subscribe(Config.topic_event_rain)   
        self.client.subscribe(Config.topic_humidity)
        self.client.subscribe(Config.topic_pressure)
        self.client.subscribe(Config.topic_solar_radiation)
        self.client.subscribe(Config.topic_sqm)
        self.client.subscribe(Config.topic_temperature)
        self.client.subscribe(Config.topic_wind_direction)
        self.client.subscribe(Config.topic_wind_gust)
        self.client.subscribe(Config.topic_wind_speed)
        # publish that we are alive
        self.client.publish("client/mqtt-observing-conditions", True, retain=True)
        self.client.will_set("client/mqtt-observing-conditions", False, retain=True)        
        # start handling subscriptions
        self.client.loop_start()
    
    @property
    def averageperiod(self) -> float:
        self._lock.acquire()
        res =  self._averageperiod
        self._lock.release()
        return res    
    @averageperiod.setter 
    def averageperiod(self, period: float):
        self._lock.acquire()
        self._averageperiod = period
        self._lock.release()
        self.logger.info(f"[average period: {period}") 

    @property
    def connected(self) -> bool:
        self._lock.acquire()
        res = self._connected
        self._lock.release()
        return res
    @connected.setter
    def connected (self, connected: bool):
        self._lock.acquire()
        self._connected = connected
        self._lock.release()
        if connected:
            self.logger.info('[connected]')
        else:
            self.logger.info('[disconnected]')    

    @property
    def lastUpdate(self) -> float:
        self._lock.acquire()
        res =  max(self._lastCloudCoverUpdate, self._lastDewPointUpdate, self._lastHumidityUpdate,
                    self._lastPressureUpdate, self._lastRainRateUpdate, self._lastSkyBrightnessUpdate,
                    self._lastSkyQualityUpdate, self._lastTemperatureUpdate, self._lastWindDirectionUpdate, 
                    self._lastWindGustUpdate, self._lastWindSpeedUpdate)
        self._lock.release()
        return res

    @property
    def lastCloudCoverUpdate(self) -> float:
        self._lock.acquire()
        res =  self._lastCloudCoverUpdate
        self._lock.release()
        return res

    @property
    def lastDewPointUpdate(self) -> float:
        self._lock.acquire()
        res =  self._lastDewPointUpdate
        self._lock.release()
        return res

    @property
    def lastHumidityUpdate(self) -> float:
        self._lock.acquire()
        res =  self._lastHumidityUpdate
        self._lock.release()
        return res

    @property
    def lastPressureUpdate(self) -> float:
        self._lock.acquire()
        res =  self._lastPressureUpdate
        self._lock.release()
        return res

    @property
    def lastRainRateUpdate(self) -> float:
        self._lock.acquire()
        res =  self._lastRainRateUpdate
        self._lock.release()
        return res

    @property
    def lastSkyBrightnessUpdate(self) -> float:
        self._lock.acquire()
        res =  self._lastSkyBrightnessUpdate
        self._lock.release()
        return res

    @property
    def lastSkyQualityUpdate(self) -> float:
        self._lock.acquire()
        res =  self._lastSkyQualityUpdate
        self._lock.release()
        return res

    @property
    def lastTemperatureUpdate(self) -> float:
        self._lock.acquire()
        res =  self._lastTemperatureUpdate
        self._lock.release()
        return res

    @property
    def lastWindDirectionUpdate(self) -> float:
        self._lock.acquire()
        res =  self._lastWindDirectionUpdate
        self._lock.release()
        return res

    @property
    def lastWindGustUpdate(self) -> float:
        self._lock.acquire()
        res =  self._lastWindDirectionUpdate
        self._lock.release()
        return res

    @property
    def lastWindSpeedUpdate(self) -> float:
        self._lock.acquire()
        res =  self._lastWindSpeedUpdate
        self._lock.release()
        return res    

    @property
    def cloudCover(self) -> float:
        self._lock.acquire()
        res =  self._cloudCover
        self._lock.release()
        return res

    @property
    def dewPoint(self) -> float:
        self._lock.acquire()
        res =  self._dewPoint
        self._lock.release()
        return res

    @property
    def humidity(self) -> float:
        self._lock.acquire()
        res =  self._humidity
        self._lock.release()
        return res 
        
    @property
    def pressure(self) -> float:
        self._lock.acquire()
        res =  self._pressure
        self._lock.release()
        return res    

    @property
    def rainRate(self) -> float:
        self._lock.acquire()
        res =  self._rainRate
        self._lock.release()
        return res        

    @property
    def skyBrightness(self) -> float:
        self._lock.acquire()
        res =  self._skyBrightness
        self._lock.release()
        return res   
    
    @property
    def skyQuality(self) -> float:
        self._lock.acquire()
        res =  self._skyQuality
        self._lock.release()
        return res      

    @property
    def temperature(self) -> float:
        self._lock.acquire()
        res =  self._temperature
        self._lock.release()
        return res       

    @property
    def windDirection(self) -> float:
        self._lock.acquire()
        if self._windSpeed != 0:
            res =  self._windDirection
        else:
            res = 0
        self._lock.release()
        return res          

    @property
    def windGust(self) -> float:
        self._lock.acquire()
        res =  self._windGust
        self._lock.release()
        return res       

    @property
    def windSpeed(self) -> float:
        self._lock.acquire()
        res =  self._windSpeed
        self._lock.release()
        return res     
    
# callbacks    
def on_connect(client, userdata, flags, rc):
    userdata.logger.info(f"[mqtt] connected rc = {rc}, flags={flags}")

def on_disconnect(client, userdata, rc):
    userdata.logger.info(f"[mqtt] disconnected, rc={rc}")
    
def on_message_cloud_cover(client, userdata, msg):
    userdata._lock.acquire()
    userdata._cloudCover = float(msg.payload.decode('utf-8'))
    userdata._lastCloudCoverUpdate = time.time()
    userdata.logger.info(f"[cloud cover] value {userdata._cloudCover} time {userdata._lastCloudCoverUpdate}")  
    userdata._lock.release()

def on_message_dew_point(client, userdata, msg):
    userdata._lock.acquire()
    userdata._dewPoint = float(msg.payload.decode('utf-8'))
    userdata._lastDewPointUpdate = time.time()    
    userdata.logger.info(f"[dew point] value {userdata._dewPoint} time {userdata._lastDewPointUpdate}")  
    userdata._lock.release()

def on_message_event_rain(client, userdata, msg):
    userdata._lock.acquire()
    userdata.last_rain_reading = userdata.current_rain_reading
    userdata.current_rain_reading = float(msg.payload.decode('utf-8'))
    userdata.last_rain_time = userdata.current_rain_time
    userdata.current_rain_time = time.time()
    userdata._lastRainRateUpdate = userdata.current_rain_time
    rate = (userdata.current_rain_reading - userdata.last_rain_reading) / (userdata.current_rain_time - userdata.last_rain_time)
    if rate < 0:
        rate = 0
    userdata._rainRate = rate * 3600  # convert mm/s to mm/hour
    userdata.logger.info(f"[rain rate] value {userdata._rainRate} time {userdata._lastRainRateUpdate}")  
    userdata._lock.release()

def on_message_hummidity(client, userdata, msg):
    userdata._lock.acquire()
    userdata._humidity = float(msg.payload.decode('utf-8'))
    userdata._lastHumidityUpdate = time.time()     
    userdata.logger.info(f"[humidity] value {userdata._humidity} time {userdata._lastHumidityUpdate}")  
    userdata._lock.release()

def on_message_pressure(client, userdata, msg):
    userdata._lock.acquire()
    userdata._pressure = float(msg.payload.decode('utf-8'))
    userdata._lastPressureUpdate = time.time()     
    userdata.logger.info(f"[pressure] value {userdata._pressure} time {userdata._lastPressureUpdate}")  
    userdata._lock.release()

def on_message_solar_radiation(client, userdata, msg):
    userdata._lock.acquire()
    userdata._skyBrightness = float(msg.payload.decode('utf-8')) * 126.7  # convert to lux
    userdata._lastSkyBrightnessUpdate = time.time()     
    userdata.logger.info(f"[sky brightness] value {userdata._skyBrightness} time {userdata._lastSkyBrightnessUpdate}")  
    userdata._lock.release()

def on_message_sqm(client, userdata, msg):
    userdata._lock.acquire()
    sqm = str(msg.payload.decode('utf-8'))
    if sqm == "daylight":
        sqm = 0
    userdata._skyQuality = float(sqm)
    userdata._lastSkyQualityUpdate = time.time()     
    userdata.logger.info(f"[sky quality] value {userdata._humidity} time {userdata._lastHumidityUpdate}")  
    userdata._lock.release()

def on_message_temperature(client, userdata, msg):
    userdata._lock.acquire()
    userdata._temperature = float(msg.payload.decode('utf-8'))
    userdata._lastTemperatureUpdate = time.time()     
    userdata.logger.info(f"[temperature] value {userdata._temperature} time {userdata._lastTemperatureUpdate}")  
    userdata._lock.release()

def on_message_wind_direction(client, userdata, msg):
    userdata._lock.acquire()
    userdata._windDirection = float(msg.payload.decode('utf-8'))
    userdata._lastWindDirectionUpdate = time.time()     
    userdata.logger.info(f"[wind direcion] value {userdata._windDirection} time {userdata._lastWindDirectionUpdate}")  
    userdata._lock.release()

def on_message_wind_gust(client, userdata, msg):
    userdata._lock.acquire()
    userdata._windGust = float(msg.payload.decode('utf-8')) * (1000.0/3600.0)  # convert from km/h to m/s
    userdata._lastWindGustUpdate = time.time()     
    userdata.logger.info(f"[wind gust] value {userdata._windGust} time {userdata._lastWindGustUpdate}")  
    userdata._lock.release()

def on_message_wind_speed(client, userdata, msg):
    userdata._lock.acquire()
    userdata._windSpeed = float(msg.payload.decode('utf-8')) * (1000.0/3600.0)  # convert from km/h to m/s
    userdata._lastWindSpeedUpdate = time.time()     
    userdata.logger.info(f"[wind speed] value {userdata._windSpeed} time {userdata._windSpeed}")  
    userdata._lock.release()    
