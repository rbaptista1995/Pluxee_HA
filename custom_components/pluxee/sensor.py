"""Platform for sensor integration."""
from __future__ import annotations
from typing import Any
import aiohttp
import logging

from datetime import datetime, timedelta
from typing import Any, Callable, Dict

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api.myedenred import MY_EDENRED
from .api.card import Card
from .const import (
    DOMAIN,
    DEFAULT_ICON,
    UNIT_OF_MEASUREMENT,
    ATTRIBUTION
)

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

# Time between updating data from API
SCAN_INTERVAL = timedelta(minutes=60)

async def async_setup_entry(hass: HomeAssistant, 
                            config_entry: ConfigEntry, 
                            async_add_entities: Callable):
    """Setup sensor platform."""
    session = async_get_clientsession(hass, True)
    api = MY_EDENRED(session)

    config = config_entry.data
    token = await api.login(config["username"], config["password"])

    if (token):
        cards = await api.getCards(token)
        sensors = [MyEdenredSensor(card, api, config) for card in cards]
        async_add_entities(sensors, update_before_add=True)


def _parse_tx_date(date_str: str) -> datetime:
    """Parse transaction dates while tolerating unexpected formats."""
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d.%m.%Y", "%d.%m"):
        
        try:
            parsed = datetime.strptime(date_str, fmt)
            if fmt == "%d.%m":
                parsed = parsed.replace(year=datetime.now().year)
            return parsed
        except (ValueError, TypeError):
            continue

    _LOGGER.debug("Unknown date format from Pluxee transaction: %s", date_str)
    return datetime.min


class MyEdenredSensor(SensorEntity):
    """Representation of a MyPluxee Card (Sensor)."""

    def __init__(self, card: Card, api: MY_EDENRED, config: Any):
        super().__init__()
        self._card = card
        self._api = api
        self._config = config
        self._transactions = None

        self._icon = DEFAULT_ICON
        self._unit_of_measurement = UNIT_OF_MEASUREMENT
        self._device_class = SensorDeviceClass.MONETARY
        self._state_class = SensorStateClass.TOTAL
        self._state = None
        self._available = True
        
    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return f"Pluxee Card {self._card.number}"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return f"{DOMAIN}-{self._card.id}".lower()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def state(self) -> float:
        return self._state

    @property
    def device_class(self):
        return self._device_class

    @property
    def state_class(self):
        return self._state_class

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit_of_measurement

    @property
    def icon(self):
        return self._icon

    @property
    def attribution(self):
        return ATTRIBUTION

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        return {
            "ownerName": self._card.ownerName,
            "cardStatus": self._card.status,
            "cardNumber": self._card.number,
            "transactions": self._transactions
        }

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.
           This is the only method that should fetch new data for Home Assistant.
        """
        api = self._api
        card = self._card
        
        try:            
            token = await api.login(self._config["username"], self._config["password"])
            if (token):
                account = await api.getAccountDetails(card.id, token)
                self._state = account.availableBalance
                movement_list = sorted(
                    account.movementList,
                    key=lambda tx: _parse_tx_date(tx.date),
                    reverse=True,
                )
                self._transactions = [
                    {
                        "date": t.date,
                        "name": t.name,
                        "amount": t.amount,
                    }
                    for t in movement_list[:10]
                ]

        except aiohttp.ClientError as err:
            self._available = False
            _LOGGER.exception("Error updating data from Pluxee API. %s", err)            
