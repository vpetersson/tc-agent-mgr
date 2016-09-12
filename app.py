import requests
import settings

from time import sleep
from urlparse import urljoin
from bs4 import BeautifulSoup


def is_ready():
    return settings.TC_URL and settings.TC_USER and settings.TC_PASS


def query_tc_for_agents(connected=True, authorized=True):
    agentdb = []
    uri = 'httpAuth/app/rest/agents?locator=connected:{},authorized:{}'.format(
        str(connected).lower(),
        str(authorized).lower(),
    )
    endpoint = urljoin(settings.TC_URL, uri)
    r = requests.get(
        endpoint, auth=(
            settings.TC_USER,
            settings.TC_PASS
        )
    )
    if not 200 <= r.status_code <= 299:
        print 'Received status code {}'.format(r.status_code)
        return False

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
        'httpAuth/app/rest/agents/id:{}/authorized'.format(agent_id)
    )
    r = requests.put(
        endpoint,
        data='{}'.format(authorize).lower(),
        auth=(
            settings.TC_USER,
            settings.TC_PASS
        )
    )

    if not 200 <= r.status_code <= 299:
        print 'Failed to authorize/unauthorize node {}. Received status code {}'.format(
            agent_id,
            r.status_code
        )
        return False
    return True


def delete_agent(agent_id):
    endpoint = urljoin(
        settings.TC_URL,
        'httpAuth/app/rest/agents/id:{}'.format(agent_id)
    )
    r = requests.delete(
        endpoint, auth=(
            settings.TC_USER,
            settings.TC_PASS
        )
    )

    if not 200 <= r.status_code <= 299:
        print 'Failed to delete node {}. Received status code {}'.format(
            agent_id,
            r.status_code
        )
        return False
    return True


def delete_inactive_agents():
    inactive_agents = query_tc_for_agents(connected=False, authorized=False)
    for agent in inactive_agents:
        delete_agent(agent['id'])


def main():
    if not is_ready():
        print 'Unable to start due to missing environment variables.'
    else:
        print 'All set. Starting up.'

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
                print 'Authorizing new build agent...'
                authorize_unauthorize_agent(agent['id'], authorize=True)
        else:
            print 'Nothing to do. Going to sleep.'

        sleep(60)


if __name__ == "__main__":
    main()
