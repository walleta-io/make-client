# make-client

A minimal Python client library for the [make.com](https://make.com) API v2.

## Installation

```bash
pip install make-client
```

Or directly from GitHub:

```bash
pip install git+https://github.com/walleta-io/make-client.git
```

## Configuration

Set your API key and team ID via environment variables:

```bash
export MAKE_API_KEY=your_api_key
export MAKE_TEAM_ID=your_team_id
```

Or pass them directly when instantiating the client.

Your team ID can be found in the make.com URL when viewing your scenarios:
`https://us2.make.com/{teamId}/scenarios`

## Library Usage

```python
from make import Make

client = Make(api_key='...', team_id=12345)

# List all scenarios
scenarios = client.list_scenarios()

# Get execution logs for a scenario
logs = client.get_scenario_logs(scenario_id=3928327)

# With a date range
from datetime import date
logs = client.get_scenario_logs(
    scenario_id=3928327,
    **{'from': date(2026, 1, 1), 'to': date(2026, 1, 31)},
)
```

## CLI Usage

```bash
# List scenarios
make-client list_scenarios

# Get scenario logs
make-client scenario_logs --scenario-id 3928327

# Override credentials
make-client --api-key ... --team-id 12345 list_scenarios

# Adjust log verbosity
make-client --log-level DEBUG list_scenarios
```

Output is JSON, so you can pipe to `jq`:

```bash
make-client list_scenarios | jq '[.[].id]'
```
