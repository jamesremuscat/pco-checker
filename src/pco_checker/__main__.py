from colorama import init, Fore
from pco_checker.api import api


def run():
    init()
    service_types = api.endpoint('service_types').get()

    for service_type in service_types.data:
        print(service_type.attributes['name'])

        plans = api.endpoint('service_types/{}/plans'.format(service_type.id)).get(params={'filter': 'future'})

        for plan in plans.data:
            print(" ", plan.attributes['dates'])

            needed = api.endpoint(f"service_types/{service_type.id}/plans/{plan.id}/needed_positions").get()
            for position in needed.data:
                print(f"    {Fore.RED}NEEDED{Fore.RESET}: {position.attributes['team_position_name']} ({position.attributes['quantity']})")

            team_members = api.endpoint('service_types/{}/plans/{}/team_members'.format(service_type.id, plan.id)).get()
            for team_member in team_members.data:
                if team_member.attributes['status'] == 'U':
                    print(f"    {Fore.YELLOW}UNCONFIRMED{Fore.RESET} ({ team_member.attributes['team_position_name'] }): {team_member.attributes['name']}")


if __name__ == "__main__":
    run()
