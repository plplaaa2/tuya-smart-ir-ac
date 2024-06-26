from tuya_connector import TuyaOpenAPI
from .const import VALID_MODES
from homeassistant.core import HomeAssistant

import logging
from pprint import pformat

_LOGGER = logging.getLogger("tuya_hack")


class TuyaAPI:
    def __init__(
        self,
        hass: HomeAssistant,
        access_id,
        access_secret,
        thermostat_device_id,
        ir_remote_device_id,
    ):
        self.access_id = access_id
        self.access_secret = access_secret
        self.thermostat_device_id = thermostat_device_id
        self.ir_remote_device_id = ir_remote_device_id
        self.hass = hass

        openapi = TuyaOpenAPI("https://openapi.tuyaus.com", access_id, access_secret)
        openapi.connect()
        self.openapi = openapi

        self._temperature = "0"
        self._mode = "0"
        self._power = "0"
        self._wind = "0"

    async def async_init(self):
        await self.update()

    async def async_update(self):
        status = await self.get_status()
        if status:
            self._temperature = status.get("temp")
            self._mode = status.get("mode")
            self._power = status.get("power")
            self._wind = status.get("wind")
        _LOGGER.info(pformat("ASYNC_UPDATE " + str(status)))

    async def async_set_fan_speed(self, fan_speed):
        _LOGGER.info(fan_speed)
        await self.send_command("wind", str(fan_speed))

    async def async_set_temperature(self, temperature):
        await self.send_command("temp", str(temperature))

    async def async_turn_on(self):
        await self.send_command("power", "1")

    async def async_turn_off(self):
        await self.send_command("power", "0")

    async def async_set_hvac_mode(self, hvac_mode):
        _LOGGER.info(hvac_mode)
        for mode, mode_name in VALID_MODES.items():
            if hvac_mode == mode_name:
                _LOGGER.info(mode)
                await self.send_command("mode", mode)
                break

    async def get_status(self):
        url = f"/v2.0/infrareds/{self.ir_remote_device_id}/remotes/{self.thermostat_device_id}/ac/status"
        _LOGGER.info(url)
        try:
            data = await self.hass.async_add_executor_job(self.openapi.get, url)
            if data.get("success"):
                _LOGGER.info(pformat("GET_STATUS " + str(data.get("result"))))
                return data.get("result")
        except Exception as e:
            _LOGGER.error(f"Error fetching status: {e}")
        return None

    async def send_command(self, code, value):
        url = f"/v2.0/infrareds/{self.ir_remote_device_id}/air-conditioners/{self.thermostat_device_id}/command"
        _LOGGER.info(url)
        try:
            _LOGGER.info(pformat("SEND_COMMAND_CODE_THEN_VAL " + code + " " + value))
            data = await self.hass.async_add_executor_job(
                self.openapi.post,
                url,
                {
                    "code": code,
                    "value": value,
                },
            )
            _LOGGER.info(pformat("SEND_COMMAND_END " + str(data)))
            return data
        except Exception as e:
            _LOGGER.error(f"Error sending command: {e}")
            return False
