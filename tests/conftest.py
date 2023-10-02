import os
import shutil
from pathlib import Path
from time import sleep

import pytest
from requests.exceptions import ConnectionError

from tests.hoass_client import HoassApi

AD_APPS_INTEGRATION_TEST_FILE = 'tests/apps-test.yaml'
AD_APPS_PRODUCTION_FILE = 'apps/apps.yaml'

BACKUP_FILE_FORMAT = '%s.bak'


def is_responsive(hoass_service):
    try:
        response = hoass_service.status()
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@pytest.fixture(scope="session")
def project_dir(pytestconfig) -> Path:
    return Path(str(pytestconfig.rootpath)).parent


@pytest.fixture(scope="session")
def docker_compose_file(project_dir) -> str:
    return str(project_dir.joinpath("docker-compose.yaml").absolute())


@pytest.fixture(scope="session")
def hoass_api(docker_ip, docker_services, configure_home_assistant):
    """Ensure that HTTP service is up and responsive."""

    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("homeassistant", 8123)
    hoass_service = HoassApi(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=120.0, pause=1, check=lambda: is_responsive(hoass_service)
    )
    sleep(15)
    return hoass_service


@pytest.fixture(scope="session", autouse=False)
def configure_home_assistant(request, project_dir):
    print('\nconfigure_HA()')
    print('\nconfigure apps.yaml')
    shutil.copy2(str(project_dir.joinpath(AD_APPS_PRODUCTION_FILE)),
                 str(project_dir.joinpath(BACKUP_FILE_FORMAT % AD_APPS_PRODUCTION_FILE)))
    shutil.copy2(str(project_dir.joinpath(AD_APPS_INTEGRATION_TEST_FILE)),
                 str(project_dir.joinpath('%s' % AD_APPS_PRODUCTION_FILE)))

    def fin():
        print('\nconfigure_HA() teardown')
        print('\nconfigure apps.yaml teardown')
        shutil.copy2(str(project_dir.joinpath(BACKUP_FILE_FORMAT % AD_APPS_PRODUCTION_FILE)),
                     str(project_dir.joinpath(AD_APPS_PRODUCTION_FILE)))
        os.remove(str(project_dir.joinpath(BACKUP_FILE_FORMAT % AD_APPS_PRODUCTION_FILE)))

    request.addfinalizer(fin)
