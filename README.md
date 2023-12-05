# CFF Export Plugin
This is an export plugin for [RDMO](https://github.com/rdmorganiser/rdmo), creating a CITATION.cff file for a software described in an RDMO software management plan (SMP) with the MPDL catalog "[Software Management Plan](https://github.com/rdmorganiser/rdmo-catalog/blob/master/rdmorganiser/questions/SMP-Questions.xml)"

The RDMO attributes are mapped to the [cff standard version 1.2.0](https://citation-file-format.github.io/).

## Setup

Install the plugin in your RDMO virtual environment using pip (directly from GitHub):
```bash
pip install git+https://github.com/rdmorganiser/rdmo-plugins-cff.git
```
Add the `rdmo_plugins_cff` app to your `INSTALLED_APPS` in `config/settings/local.py``:
```py
from . import INSTALLED_APPS
INSTALLED_APPS = ['rdmo_plugins_cff'] + INSTALLED_APPS
```

Add the export plugins to the PROJECT_EXPORTS in config/settings/local.py:
```py
from django.utils.translation import gettext_lazy as _
from . import PROJECT_EXPORTS

PROJECT_EXPORTS += [
    ('cff-file', _('as CITATION.cff file'), 'rdmo_plugins_cff.exports.cff.cff.CffExport')
]
```

Please visit the [RDMO documentation](https://rdmo.readthedocs.io/en/latest/plugins/index.html#project-export-plugins) for detailed information.
