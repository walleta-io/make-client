"""
Minimal make.com API v2 client.

Only covers the endpoints needed for usage PULL:
  - GET /scenarios          — list all scenarios
  - GET /scenarios/{id}/logs — paginated execution logs
"""
import json
import logging
import os
import urllib.error
import urllib.parse
import urllib.request

from datetime import date, datetime, timezone
from typing import Any, Optional


LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

TEAM_ID_NAME = 'MAKE_TEAM_ID'
API_KEY_NAME = 'MAKE_API_KEY'


def get_team_id(team_id: Optional[int] = None) -> int:
    if team_id is not None:
        return team_id
    if TEAM_ID_NAME in os.environ:
        return int(os.environ[TEAM_ID_NAME])
    raise ValueError('Cannot find Team id')


def get_api_key(api_key: Optional[str] = None) -> str:
    if api_key is not None:
        return api_key
    if API_KEY_NAME in os.environ:
        return os.environ[API_KEY_NAME]
    raise ValueError('Cannot find API key!')


def strip_slash(s: str, start: bool = True, end: bool = True) -> str:
    while start and s.startswith('/'):
        s = s.lstrip('/')
    while end and s.endswith('/'):
        s = s.rstrip('/')
    return s


class Make:
    def __init__(self,
                 api_key: Optional[str] = None,
                 team_id: Optional[int] = None,
                 base_url: str = 'https://us2.make.com/api/v2',
                 ):
        api_key = get_api_key(api_key)
        self.team_id = get_team_id(team_id)
        self.base_url = strip_slash(base_url)
        self._headers = {
            'Authorization': f'Token {api_key}',
            'User-Agent': 'make-client/1.0',
        }

    def get_url(self, path: str, params: Optional[dict] = None) -> str:
        path = strip_slash(path)
        url = f'{self.base_url}/{path}'
        if params:
            url = f'{url}?{urllib.parse.urlencode(params)}'
        return url

    def do_get(self, path: str, params: Optional[dict] = None) -> dict:
        params = {**(params or {}), 'teamId': self.team_id}
        url = self.get_url(path, params=params)
        req = urllib.request.Request(url, headers=self._headers)
        LOGGER.debug('GET %s', url)
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='replace')
            LOGGER.error('HTTP %s %s: %s', e.code, e.reason, body)
            raise

    def list_scenarios(self, **params: Any) -> list[dict]:
        return self.do_get('scenarios', params=params).get('scenarios', [])

    def _get_scenario_logs_page(self, scenario_id: int, **params: Any) -> tuple:
        data = self.do_get(f'scenarios/{scenario_id}/logs', params=params)
        return (
            data.get('pg', {}).get('last'),
            data.get('scenarioLogs', []),
        )

    def get_scenario_logs(
        self,
        scenario_id: int,
        **params: Any,
    ) -> list[dict]:
        """Fetch all execution log entries for a scenario, handling pagination."""
        _from = params.get('from')
        if isinstance(_from, date):
            params['from'] = datetime(
                _from.year, _from.month, _from.day, tzinfo=timezone.utc).isoformat()
        _to = params.get('to')
        if isinstance(_to, date):
            params['to'] = datetime(
                _to.year, _to.month, _to.day, 23, 59, 59, tzinfo=timezone.utc).isoformat()

        logs = []
        while True:
            page, results = self._get_scenario_logs_page(scenario_id, **params)
            if not results:
                break
            logs.extend(results)
            if not page:
                break
            # Advance cursor; drop from/to after first request to avoid conflicts.
            params.pop('from', None)
            params.pop('to', None)
            params['pg[last]'] = page

        return logs
