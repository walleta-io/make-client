import sys
import argparse
import json
import logging

from . import Make


def main():
    parser = argparse.ArgumentParser(prog='make')
    parser.add_argument('--api-key')
    parser.add_argument('--team-id', type=int)
    parser.add_argument('--log-level', default='WARNING')
    parser.add_argument('command', choices=['list_scenarios', 'scenario_logs'])
    parser.add_argument('--scenario-id', type=int)
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level.upper())

    m = Make(api_key=args.api_key, team_id=args.team_id)

    match args.command:
        case 'list_scenarios':
            results = m.list_scenarios()

        case 'scenario_logs':
            if not args.scenario_id:
                parser.error('scenario_logs requires --scenario-id')
            results = m.get_scenario_logs(args.scenario_id)

        case _:
            exit('Invalid command')

    json.dump(results, sys.stdout, indent=2)


if __name__ == '__main__':
    main()
