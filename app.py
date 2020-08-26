import requests
import settings
import sys

from time import sleep
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def is_ready():
    return settings.TC_URL and settings.TC_USER and settings.TC_PASS


def query_tc_for_agents(connected=True, authorized=True):
    agentdb = []
    uri = 'app/rest/agents?locator=connected:{},authorized:{}'.format(
        str(connected).lower(),
        str(authorized).lower(),
    )
    endpoint = urljoin(settings.TC_URL, uri)
    r = requests.get(endpoint, auth=(settings.TC_USER, settings.TC_PASS))
    if not r.ok:
        print('Unable to connect. Received status code {}'.format(r.status_code))
        print(r.content)
        sys.exit(1)

    r_parsed = BeautifulSoup(r.content, 'lxml-xml')
    agents = r_parsed.findAll('agent')
    for agent in agents:
        agentdb.append({
            'name': agent.get('name'),
            'id': agent.get('id'),
            'uri': agent.get('href'),
        })
    return agentdb


def authorize_unauthorize_agent(agent_id, authorize=True):
    endpoint = urljoin(
        settings.TC_URL,
        'app/rest/agents/id:{}/authorized'.format(agent_id)
    )
    r = requests.put(
        endpoint,
        data='{}'.format(authorize).lower(),
        auth=(settings.TC_USER, settings.TC_PASS)
    )

    if not r.ok:
        print('Failed to authorize/unauthorize node {}. Received status code {}'.format(
            agent_id,
            r.status_code
        ))
        sys.exit(1)
    return True


def delete_agent(agent_id):
    endpoint = urljoin(
        settings.TC_URL,
        'app/rest/agents/id:{}'.format(agent_id)
    )
    r = requests.delete(
        endpoint,
        auth=(settings.TC_USER, settings.TC_PASS)
    )

    if not r.ok:
        print('Failed to delete node {}. Received status code {}'.format(
            agent_id,
            r.status_code
        ))
        sys.exit(1)
    return True


def delete_inactive_agents():
    inactive_agents = []

    for agent in query_tc_for_agents(connected=False, authorized=False):
        inactive_agents.append(agent)

    for agent in query_tc_for_agents(connected=False, authorized=True):
        inactive_agents.append(agent)

    for agent in inactive_agents:
        print('Deleting agent {}...'.format(agent['name']))
        delete_agent(agent['id'])


def main():
    if not is_ready():
        print('Unable to start due to missing environment variables.')
        sys.exit(1)
    else:
        print('All set. Starting up.')

    while True:
        delete_inactive_agents()

        enabled_agents = query_tc_for_agents(
            connected=True,
            authorized=True,
        )

        unauthorized_agents = query_tc_for_agents(
            connected=True,
            authorized=False,
        )

        if len(enabled_agents) < settings.TC_MAX_AGENTS and len(unauthorized_agents) > 0:
            for agent in unauthorized_agents:
                if settings.AGENT_WHITELIST_STRING and not settings.AGENT_WHITELIST_STRING.lower() in agent['name'].lower():
                        break
                print('Authorizing new build agent {}...'.format(agent['name']))
                authorize_unauthorize_agent(agent['id'], authorize=True)
        else:
            print('Nothing to do. Going to sleep.')

        sleep(60)


if __name__ == "__main__":
    main()
