"""API to PLUXEE consumer portal."""
import logging
import re
from datetime import datetime
from urllib.parse import unquote

import aiohttp

from .account import Account
from .card import Card
from .consts import API_DASHBOARD_URL, API_LOGIN_URL

_LOGGER = logging.getLogger(__name__)


class MY_EDENRED:
    """Interfaces to https://consumidores.pluxee.pt/."""

    def __init__(self, websession):
        self.websession = websession

    async def login(self, username, password):
        """Authenticate against the new Pluxee consumer login."""
        params = {
            "callback": "ha_callback",
            "nif": username,
            "pass": password,
            "reg": "true",
            "_": str(int(datetime.utcnow().timestamp() * 1000)),
        }

        async with self.websession.get(API_LOGIN_URL, params=params) as res:
            body = await res.text()
            if res.status != 200 or "false" in body.lower():
                raise Exception("Could not authenticate user")

            # jsonp response, we only need the authenticated cookies in session
            _LOGGER.debug("Authenticated with Pluxee portal")
            return "session"

    async def _get_dashboard_html(self):
        async with self.websession.get(API_DASHBOARD_URL) as res:
            html = await res.text()
            if res.status != 200:
                raise Exception("Could not load Pluxee dashboard")
            return html

    async def getCards(self, token) -> Card:
        """Extract card info from dashboard HTML."""
        html = await self._get_dashboard_html()
        card_number = self._extract(html, r"Cartão Nº:\s*([^<]+)<")
        card_id = self._extract(html, r'id="card_id">\s*([0-9]+)\s*<')
        data_cardid = self._extract(html, r'data-cardid="([0-9]+)"')

        card = {
            "id": data_cardid or card_id or "pluxee",
            "number": (card_number or "").strip(),
            "ownerName": "Pluxee",
            "status": "ACTIVE",
            "_html": html,
        }
        return [Card(card)]

    async def getAccountDetails(self, cardId, token) -> Account:
        """Extract balance and movements from dashboard HTML."""
        html = await self._get_dashboard_html()

        balance_raw = self._extract(html, r'card-heading[^>]*>\s*([0-9\.,]+)') or "0"
        balance = float(balance_raw.replace(".", "").replace(",", "."))

        movement_patterns = [
            re.compile(
                r'<div[^>]*class="[^"]*date_mov[^"]*"[^>]*>\s*([0-9]{2}\.[0-9]{2}(?:\.[0-9]{4})?)\s*</div>.*?'
                r'<div[^>]*class="[^"]*description_mov[^"]*"[^>]*>\s*([^<]+?)\s*</div>.*?'
                r'<div[^>]*class="[^"]*value_mov[^"]*"[^>]*>\s*([+-]?[0-9\.,]+)',
                re.S,
            ),
            re.compile(
                r'<span[^>]*class="[^"]*date_mov[^"]*"[^>]*>\s*([0-9]{2}\.[0-9]{2}(?:\.[0-9]{4})?)\s*</span>.*?'
                r'<span[^>]*class="[^"]*description_mov[^"]*"[^>]*>\s*([^<]+?)\s*</span>.*?'
                r'<span[^>]*class="[^"]*value_mov[^"]*"[^>]*>\s*([+-]?[0-9\.,]+)',
                re.S,
            ),
        ]

        movements = []
        for pattern in movement_patterns:
            for m in pattern.finditer(html):
                date, name, amount = m.groups()
                amount = amount.replace(".", "").replace(",", ".")
                movements.append({
                    "transactionDate": date,
                    "transactionName": unquote(name).strip(),
                    "amount": amount,
                })
            if movements:
                break

        _LOGGER.debug("Extracted %s transactions from Pluxee dashboard", len(movements))

        return Account({
            "iban": "",
            "cardNumber": cardId,
            "availableBalance": balance,
            "cardHolderFirstName": "",
            "cardHolderLastName": "",
            "cardActivated": True,
        }, movements)

    @staticmethod
    def _extract(content: str, pattern: str):
        m = re.search(pattern, content, re.S)
        return m.group(1) if m else None
