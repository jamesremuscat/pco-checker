from datetime import datetime
from pco_checker.api import api

PRODUCTION_TEAM_IDS = ['1452268', '1452274', '1452280', '4218978', '4246891', '4269029', '4489725', '4657247']
ISO_DATE_STRING = '%Y-%m-%dT%H:%M:%SZ'


def calculate_time_duration(t):

    start_time = datetime.strptime(t.attributes['starts_at'], ISO_DATE_STRING)
    end_time = datetime.strptime(t.attributes['ends_at'], ISO_DATE_STRING)
    return (end_time - start_time).total_seconds()


def run():
    service_types = api.endpoint('service_types').get()
    overall_hours = 0

    for service_type in service_types.data:

        # https://api.planningcenteronline.com/services/v2/service_types/387688/plans?include=plan_times&filter=after,before&per_page=250&after=2021-09-01&before=2022-09-01

        plans = api.endpoint(
            'service_types/{}/plans'.format(service_type.id)
        ).get(
            params={
                'filter': 'after,before',
                'per_page': 100,
                'after': '2021-08-31',
                'before': '2022-09-01',
                'include': 'plan_times'
            }
        )

        service_times = list(
            filter(
                lambda p: p.type == 'PlanTime' and p.attributes['time_type'] == 'service',
                plans.content.included
            )
        )

        plan_time_durations = {t.id: calculate_time_duration(t) for t in filter(lambda p: p.type == 'PlanTime', plans.content.included)}

        num_services = len(service_times)

        cumulative_time_seconds = 0

        for plan in plans.data:
            team_members = api.endpoint(f'service_types/{service_type.id}/plans/{plan.id}/team_members').get()

            production_team_members = list(
                filter(
                    lambda t: t.relationships['team'].data.id in PRODUCTION_TEAM_IDS and t.attributes['status'] == 'C',
                    team_members.data
                )
            )

            for person in production_team_members:
                durations = list(
                    map(
                        lambda t: plan_time_durations[t.id],
                        person.relationships['times'].data
                    )
                )
                cumulative_time_seconds += sum(durations)

        total_hours = cumulative_time_seconds / 3600
        overall_hours += total_hours

        print(f'{service_type.attributes["name"]} => {len(plans.data)} plans, {num_services} services, {total_hours} volunteer hours')

    print(f'Total hours: {overall_hours}')


if __name__ == "__main__":
    run()
