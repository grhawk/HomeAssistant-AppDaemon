import os
import shutil

import pytest

AD_APPS_INTEGRATION_TEST_FILE = 'tests/apps-test.yaml'
AD_APPS_PRODUCTION_FILE = 'apps/apps.yaml'

BACKUP_FILE_FORMAT = '%s.bak'


@pytest.fixture(scope="session", autouse=True)
def configure_home_assistant(request):
    print('\nconfigure_HA()')
    print('\nconfigure apps.yaml')
    shutil.copy2(AD_APPS_PRODUCTION_FILE, BACKUP_FILE_FORMAT % AD_APPS_PRODUCTION_FILE)
    shutil.copy2(AD_APPS_INTEGRATION_TEST_FILE, '%s' % AD_APPS_PRODUCTION_FILE)

    def fin():
        print('\nconfigure_HA() teardown')
        print('\nconfigure apps.yaml teardown')
        shutil.copy2(BACKUP_FILE_FORMAT % AD_APPS_PRODUCTION_FILE, AD_APPS_PRODUCTION_FILE)
        os.remove(BACKUP_FILE_FORMAT % AD_APPS_PRODUCTION_FILE)

    request.addfinalizer(fin)
