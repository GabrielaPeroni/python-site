### Basic Django Unit Test with Test Client

Source: https://docs.djangoproject.com/en/6.0/topics/testing/tools

An example of a standard Python unit test using Django's `Client`. It shows how to initialize the client in `setUp`, make a GET request, and assert the status code and context data of the response.

```python
import unittest
from django.test import Client

class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get("/customer/details/")

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 5 customers.
        self.assertEqual(len(response.context["customers"]),
                         5)
```

--------------------------------

### Verify Python Installation

Source: https://docs.djangoproject.com/en/6.0/intro/install

This code block demonstrates how to verify if Python is installed by typing 'python' in the shell, which should display the Python version and environment details.

```shell
python
Python 3.x.y
[GCC 4.x] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>

```

--------------------------------

### Verify Django Installation

Source: https://docs.djangoproject.com/en/6.0/intro/install

This snippet shows how to verify the Django installation within a Python interpreter. It involves importing the Django library and then printing its version using `django.get_version()`.

```python
>>> import django
>>> print(django.get_version())
6.0

```

--------------------------------

### Install and Install Git Hooks with pre-commit

Source: https://docs.djangoproject.com/en/6.0/internals/contributing/writing-code/coding-style

Instructions for installing the pre-commit framework and its git hooks. This tool helps identify simple issues before committing code, reducing the need for CI runs and allowing reviewers to focus on code changes. It also automatically fixes some formatting issues.

```shell
$ python -m pip install pre-commit
$ pre-commit install

```

```shell
...\n> py -m pip install pre-commit
...\n> pre-commit install


```

--------------------------------

### Writing Django Middleware as a Class

Source: https://docs.djangoproject.com/en/6.0/topics/http/middleware

This example demonstrates creating a Django middleware component as a class. The `__init__` method handles initial setup, receiving the `get_response` callable. The `__call__` method contains the logic executed for each request before and after the view.

```python
class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

```

--------------------------------

### Configure uWSGI Server for Django (INI File)

Source: https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/uwsgi

Provides an example INI configuration file for starting a uWSGI server for a Django project. This method simplifies the command-line arguments by organizing them into a configuration file.

```ini
[uwsgi]
chdir=/path/to/your/project
module=mysite.wsgi:application
master=True
pidfile=/tmp/project-master.pid
vacuum=True
max-requests=5000
daemonize=/var/log/uwsgi/yourproject.log

```

--------------------------------

### Install GeoDjango prerequisites with Homebrew on macOS

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install

Installs essential GeoDjango prerequisites on macOS using the Homebrew package manager. This includes PostgreSQL, PostGIS, GDAL, and libGeoIP. Xcode is required as Homebrew builds from source.

```bash
$ brew install postgresql
$ brew install postgis
$ brew install gdal
$ brew install libgeoip
```

--------------------------------

### Django Sitemap Index URLconf Setup

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/sitemaps

This example configures Django's URL patterns to serve a sitemap index and individual sitemap files. It utilizes the `views.index` and `views.sitemap` functions from `django.contrib.sitemaps`.

```python
from django.contrib.sitemaps import views

urlpatterns = [
    path(
        "sitemap.xml",
        views.index,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.index",
    ),
    path(
        "sitemap-<section>.xml",
        views.sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
```

--------------------------------

### Install binutils on Debian/Ubuntu

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install

Installs the binutils package, which is required by GeoDjango's find_library function on GNU/Linux systems. This package provides the objdump utility.

```bash
$ sudo apt-get install binutils
```

--------------------------------

### Install binutils on Red Hat/CentOS

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install

Installs the binutils package, which is required by GeoDjango's find_library function on GNU/Linux systems. This package provides the objdump utility.

```bash
$ sudo yum install binutils
```

--------------------------------

### Django Admins Docs Setup

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/admin/admindocs

Configuration steps to enable Django's admindocs app. This involves adding the app to INSTALLED_APPS, including its URLs in the project's urlpatterns, and installing the docutils package. Optional middleware for bookmarklets is also mentioned.

```python
INSTALLED_APPS = [
    ...
    'django.contrib.admindocs',
    ...
]

urlpatterns = [
    ...
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    ...
]
```

--------------------------------

### Install Sphinx Documentation Generator (Unix/Linux)

Source: https://docs.djangoproject.com/en/6.0/intro/whatsnext

This command installs the Sphinx documentation generator using pip, a Python package installer. Sphinx is required to convert plain text documentation into HTML format.

```bash
$ python -m pip install Sphinx

```

--------------------------------

### Django App README and Installation Instructions

Source: https://docs.djangoproject.com/en/6.0/intro/reusable-apps

This is a sample README.rst file for a Django application, providing a brief overview, installation instructions, and usage steps. It includes how to add the app to `INSTALLED_APPS`, include its URLs, run migrations, and access the app's features.

```rst
============
django-polls
============

django-polls is a Django app to conduct web-based polls. For each
question, visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "django_polls",
    ]

2. Include the polls URLconf in your project urls.py like this::

    path("polls/", include("django_polls.urls")),

3. Run ``python manage.py migrate`` to create the models.

4. Start the development server and visit the admin to create a poll.

5. Visit the ``/polls/`` URL to participate in the poll.


```

--------------------------------

### Django CLI: Start Development Server

Source: https://docs.djangoproject.com/en/6.0/intro/tutorial02

Command-line instructions for starting the Django development server. This command launches a local web server to test your Django application, including the admin interface. Access the admin site by navigating to '/admin/' in your web browser.

```bash
$ python manage.py runserver

```

```powershell
...\> py manage.py runserver

```

--------------------------------

### Start uWSGI Server using INI File

Source: https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/uwsgi

Demonstrates how to start the uWSGI server using an INI configuration file. This is a convenient way to manage uWSGI settings.

```shell
uwsgi --ini uwsgi.ini

```

--------------------------------

### Download and Build SpatiaLite from Source

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install/spatialite

Steps to download the SpatiaLite library source bundle, extract it, configure the build, compile, and install it. This method is universally applicable when pre-compiled binaries or packages are not available.

```bash
$ wget https://www.gaia-gis.it/gaia-sins/libspatialite-sources/libspatialite-X.Y.Z.tar.gz
$ tar xaf libspatialite-X.Y.Z.tar.gz
$ cd libspatialite-X.Y.Z
$ ./configure
$ make
$ sudo make install

```

--------------------------------

### Install Django using pip

Source: https://docs.djangoproject.com/en/6.0/topics/install

These commands demonstrate the recommended method for installing Django using pip within a virtual environment. The first command is for Unix-like systems (Linux/macOS), and the second is for Windows.

```shell
$ python -m pip install Django

```

```shell
...> py -m pip install Django

```

--------------------------------

### Install GeoDjango prerequisites with MacPorts on macOS

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install

Installs GeoDjango prerequisites on macOS using the MacPorts package manager. This includes PostgreSQL, GEOS, PROJ, PostGIS, GDAL, and libGeoIP. Xcode is required as MacPorts builds from source.

```bash
$ sudo port install postgresql14-server
$ sudo port install geos
$ sudo port install proj6
$ sudo port install postgis3
$ sudo port install gdal
$ sudo port install libgeoip
```

--------------------------------

### Install Sphinx Documentation Generator (Windows)

Source: https://docs.djangoproject.com/en/6.0/intro/whatsnext

This command installs the Sphinx documentation generator using pip, a Python package installer. Sphinx is required to convert plain text documentation into HTML format on Windows.

```batch
...\> py -m pip install Sphinx

```

--------------------------------

### Python Test Docstring Example with Ticket Reference

Source: https://docs.djangoproject.com/en/6.0/internals/contributing/writing-code/coding-style

Example of a Python test docstring, including a ticket reference for obscure issues. Ticket numbers should be appended to sentences where additional context from the ticket is beneficial.

```python
def test_foo():
    """
    A test docstring looks like this (#123456).
    """
    ...

```

--------------------------------

### Install and Run isort for Import Sorting

Source: https://docs.djangoproject.com/en/6.0/internals/contributing/writing-code/coding-style

Installs the isort tool and runs it recursively on the current directory to automatically sort Python imports according to predefined guidelines. This tool helps maintain consistent import order and structure.

```shell
$ python -m pip install "isort >= 7.0.0"
$ isort .
```

```shell
...\> py -m pip install "isort >= 7.0.0"
...\> isort .
```

--------------------------------

### Test ReportLab Installation

Source: https://docs.djangoproject.com/en/6.0/howto/outputting-pdf

Verifies that the ReportLab library has been installed correctly by attempting to import it in the Python interactive interpreter. Successful import indicates the installation was successful.

```python
>>> import reportlab

```

--------------------------------

### Build and Install PROJ with CMake

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install/geolibs

Commands to build and install the PROJ library using CMake after configuration. This includes building the library and installing it to the system.

```bash
$ cmake --build .
$ sudo cmake --build . --target install
```

--------------------------------

### Install Daphne with pip

Source: https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/daphne

This command installs the Daphne ASGI server using pip. Ensure you have pip installed and accessible in your environment.

```shell
python -m pip install daphne
```

--------------------------------

### Configure System Library Path (GNU/Linux)

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install

This code demonstrates how to update the system's dynamic library path on GNU/Linux systems. It involves appending the library directory to the ld.so.conf file and then running ldconfig to update the system's library cache. This ensures that system-wide applications can find newly installed libraries.

```bash
$ sudo echo /usr/local/lib >> /etc/ld.so.conf
$ sudo ldconfig
```

--------------------------------

### Install Jinja2 for Django

Source: https://docs.djangoproject.com/en/6.0/topics/templates

Instructions for installing the Jinja2 templating engine using pip, required for configuring the Jinja2 backend in Django.

```shell
python -m pip install Jinja2
```

```shell
py -m pip install Jinja2
```

--------------------------------

### Django Settings Markup

Source: https://docs.djangoproject.com/en/6.0/internals/contributing/writing-documentation

Directive to document Django settings. Use `:setting:` to link to a documented setting. Example: `.. setting:: INSTALLED_APPS`.

```rst
.. setting:: INSTALLED_APPS
```

--------------------------------

### Instantiate and Use Django Test Client

Source: https://docs.djangoproject.com/en/6.0/intro/tutorial05

This snippet shows how to import and create an instance of Django's test Client. It then demonstrates making a GET request to a URL and checking the response status code and content. It also shows how to use `reverse` for URL lookups.

```python
>>> from django.test import Client
>>> from django.urls import reverse
>>> client = Client()
>>> response = client.get("/")
>>> response.status_code
404
>>> response = client.get(reverse("polls:index"))
>>> response.status_code
200
>>> response.content
b'\n    <ul>\n    \n        <li><a href="/polls/1/">What&#x27;s up?</a></li>\n    \n    </ul>\n\n'
>>> response.context["latest_question_list"]
<QuerySet [<Question: What's up?>]>
```

--------------------------------

### Start a New Django Project

Source: https://docs.djangoproject.com/en/6.0/intro/tutorial01

Command to create a new Django project named 'mysite' in a directory called 'djangotutorial'. This command bootstraps the necessary files and directory structure for a Django project.

```shell
$ django-admin startproject mysite djangotutorial

```

```shell
...\> django-admin startproject mysite djangotutorial

```

--------------------------------

### Modify PATH for Python on macOS

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install

Updates the PATH environment variable in the .profile file to use a newer Python version installed via framework installers on macOS. This ensures the 'python' command points to the desired installation.

```bash
export PATH=/Library/Frameworks/Python.framework/Versions/Current/bin:$PATH
```

--------------------------------

### Configure Django Setting for SpatiaLite Library Path

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install/spatialite

Example of how to set the `SPATIALITE_LIBRARY_PATH` in Django's settings to point to the location of the SpatiaLite library. This is crucial for GeoDjango to find and utilize the SpatiaLite extension.

```python
SPATIALITE_LIBRARY_PATH = "/opt/homebrew/lib/mod_spatialite.dylib"

```

--------------------------------

### Install Uvicorn using pip

Source: https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/uvicorn

This command installs the Uvicorn ASGI server using pip. Ensure you have pip installed and accessible in your environment.

```shell
python -m pip install uvicorn
```

--------------------------------

### Python Unpacking Generalizations Example

Source: https://docs.djangoproject.com/en/6.0/internals/contributing/writing-code/coding-style

Demonstrates the use of unpacking generalizations compliant with PEP 448, such as merging mappings and sequences. This practice is encouraged for improved performance, readability, and maintainability.

```python
# Where applicable, use unpacking generalizations compliant with **PEP 448**, such as merging mappings (`{**x, **y}`) or sequences (`[*a, *b]`). This improves performance, readability, and maintainability while reducing errors.

```

--------------------------------

### Install psycopg Python Module

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install

The psycopg module facilitates communication between Python applications and PostgreSQL databases. It can be installed using pip within a Python virtual environment. Ensure you are in your project's virtual environment before running the command.

```bash
...\> py -m pip install psycopg
```

--------------------------------

### Getting Runtime Help with django-admin

Source: https://docs.djangoproject.com/en/6.0/ref/django-admin

Shows how to retrieve help information for the `django-admin` command. This includes displaying general usage, listing all commands, or getting details about a specific command.

```shell
django-admin help
django-admin help --commands
django-admin help <command>
```

--------------------------------

### Run the Django development server

Source: https://docs.djangoproject.com/en/6.0/intro/tutorial01

These commands initiate the Django development server, which is used for testing and local development. Executing this command will start a server that listens for incoming HTTP requests on a specified port (default is 8000), allowing you to view your Django application in a web browser.

```bash
$ python manage.py runserver

```

```powershell
...> py manage.py runserver

```

--------------------------------

### Install Core Django Tables with Migrate

Source: https://docs.djangoproject.com/en/6.0/howto/legacy-databases

Run the `migrate` command after setting up models to install any additional necessary database records, such as admin permissions and content types.

```shell
python manage.py migrate
```

--------------------------------

### Django Get Signed Cookie Examples

Source: https://docs.djangoproject.com/en/6.0/ref/request-response

Illustrates the usage of Django's `get_signed_cookie` method for retrieving signed cookie values. Examples cover successful retrieval, handling non-existent cookies, using salts, and managing expired signatures.

```python
>>> request.get_signed_cookie("name")
'Tony'
>>> request.get_signed_cookie("name", salt="name-salt")
'Tony' # assuming cookie was set using the same salt
>>> request.get_signed_cookie("nonexistent-cookie")
KeyError: 'nonexistent-cookie'
>>> request.get_signed_cookie("nonexistent-cookie", False)
False
>>> request.get_signed_cookie("cookie-that-was-tampered-with")
BadSignature: ...
>>> request.get_signed_cookie("name", max_age=60)
SignatureExpired: Signature age 1677.3839159 > 60 seconds
>>> request.get_signed_cookie("name", False, max_age=60)
False

```

--------------------------------

### Example Django Import Grouping

Source: https://docs.djangoproject.com/en/6.0/internals/contributing/writing-code/coding-style

An example Python code snippet illustrating the recommended grouping and sorting of imports in Django projects. It shows the order: future, standard library, third-party, Django components, local Django components, and try/except blocks. Imports are sorted alphabetically within each group.

```python
# future
from __future__ import unicode_literals

# standard library
import json
from itertools import chain

# third-party
import bcrypt

# Django
from django.http import Http404
from django.http.response import (
    Http404,
    HttpResponse,
    HttpResponseNotAllowed,
    StreamingHttpResponse,
    cookie,
)

# local Django
from .models import LogEntry

# try/except
try:
    import yaml
except ImportError:
    yaml = None

CONSTANT = "foo"


class Example: ...

```

--------------------------------

### Django pre_save Signal Example

Source: https://docs.djangoproject.com/en/6.0/ref/signals

This example illustrates connecting a receiver to the `pre_save` signal, which is triggered at the start of a Django model's `save()` method. It shows how to access the sender, instance, raw flag, database alias, and update fields.

```python
from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save)
def pre_save_handler(sender, instance, raw, using, update_fields, **extra_kwargs):
    print(f"Pre-save signal received for {sender.__name__} instance {instance.pk}")
    print(f"Raw: {raw}")
    print(f"Using: {using}")
    print(f"Update fields: {update_fields}")
    # You can modify instance here before it's saved

# Example usage:
# class MyModel(models.Model):
#     # ... model definition

# When instance.save() is called, the pre_save_handler will be executed first.
```

--------------------------------

### Start Django Development Server

Source: https://docs.djangoproject.com/en/6.0/intro/tutorial01

This command starts the Django development server, allowing you to test your project locally. It's suitable for development but not for production environments. The server automatically reloads for Python code changes.

```bash
$ python manage.py runserver
```

```batch
...\> py manage.py runserver
```

--------------------------------

### Add Postgres.app to PATH on macOS

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install

Appends the path to the Postgres.app binaries to the PATH environment variable in the .bash_profile file on macOS. This allows running PostgreSQL commands from the terminal.

```bash
export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/X.Y/bin
```

--------------------------------

### Running collectstatic Management Command Help

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/staticfiles

These are command-line examples showing how to access the help documentation for the `collectstatic` management command in Django. The `--help` flag provides a detailed explanation of all available options and their usage. This is crucial for understanding and effectively utilizing the `collectstatic` command.

```bash
$ python manage.py collectstatic --help

```

```bash
...\> py manage.py collectstatic --help

```

--------------------------------

### Django Logging: Configuration Example

Source: https://docs.djangoproject.com/en/6.0/contents

Configure Django's logging system to manage application logs effectively. This includes setting up handlers, formatters, and log levels.

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
```

--------------------------------

### Django `Q` object for complex queries (startswith)

Source: https://docs.djangoproject.com/en/6.0/topics/db/queries

Shows how to use Django's `Q` objects to create complex queries, starting with a simple `startswith` example. `Q` objects allow for more advanced filtering logic than standard keyword arguments.

```python
from django.db.models import Q

Q(question__startswith="What")
```

--------------------------------

### Run Django Unit Tests (Linux/macOS)

Source: https://docs.djangoproject.com/en/6.0/internals/contributing/writing-code/unit-tests

This snippet shows the command-line steps to clone the Django repository, set up a virtual environment, install requirements, and run the unit tests using the `runtests.py` script on Unix-like systems.

```bash
$ git clone https://github.com/YourGitHubName/django.git django-repo
$ cd django-repo/tests
$ python -m pip install -e ..
$ python -m pip install -r requirements/py3.txt
$ ./runtests.py

```

--------------------------------

### Install Colorama for Colored Terminal Output

Source: https://docs.djangoproject.com/en/6.0/howto/windows

Installs the 'colorama' package, required for colored terminal output in older Windows versions or legacy terminals. This ensures syntax coloring works correctly within the command prompt.

```shell
...\> py -m pip install "colorama >= 0.4.6"
```

--------------------------------

### Apply Database Migrations with Django

Source: https://docs.djangoproject.com/en/6.0/intro/tutorial02

This command applies database migrations for the Django project. It reads the `INSTALLED_APPS` setting and creates necessary database tables based on `mysite/settings.py` and app migrations. Ensure your database is configured correctly in `settings.py`.

```bash
python manage.py migrate
```

```powershell
py manage.py migrate
```

--------------------------------

### Configure PATH for MacPorts on macOS

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install

Modifies the PATH environment variable in the .profile file to include MacPorts binaries and libraries on macOS. This makes MacPorts-installed programs accessible from the command line.

```bash
export PATH=/opt/local/bin:/opt/local/lib/postgresql14/bin
```

--------------------------------

### Example of Test Runner Output during Database Creation

Source: https://docs.djangoproject.com/en/6.0/topics/testing/overview

Illustrates the console output when the Django test runner initializes the test database. This includes messages about creating the database and setting up tables.

```shell
Creating test database...
Creating table myapp_animal
Creating table myapp_mineral
```

--------------------------------

### Django `Q` objects with multiple positional arguments

Source: https://docs.djangoproject.com/en/6.0/topics/db/queries

Explains how to pass multiple `Q` objects as positional arguments to lookup functions like `get()`. When multiple `Q` objects are used this way, they are ANDed together. This example demonstrates an AND combination of a `startswith` query with an OR condition on `pub_date`.

```python
from datetime import date

Poll.objects.get(
    Q(question__startswith="Who"),
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)),
)
```

--------------------------------

### Configure DYLD_FALLBACK_LIBRARY_PATH for MacPorts on macOS

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install

Sets the DYLD_FALLBACK_LIBRARY_PATH environment variable to include MacPorts library directories on macOS. This helps Python locate the necessary libraries.

```bash
export DYLD_FALLBACK_LIBRARY_PATH=/opt/local/lib:/opt/local/lib/postgresql14
```

--------------------------------

### Find Django Installation Path (Python)

Source: https://docs.djangoproject.com/en/6.0/intro/tutorial07

These snippets demonstrate how to find the installation path of the Django library on your system using Python. This is useful for locating default template files or other Django source code.

```python
$ python -c "import django; print(django.__path__)"
```

```python
> py -c "import django; print(django.__path__)"
```

--------------------------------

### Set LD_LIBRARY_PATH Environment Variable (Bash)

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install

This snippet demonstrates how to set the LD_LIBRARY_PATH environment variable in a bash profile. This is typically used to inform the operating system about the location of dynamically linked libraries, especially when they are installed from source in non-standard directories like /usr/local/lib.

```bash
export LD_LIBRARY_PATH=/usr/local/lib
```

--------------------------------

### Deploy Django ASGI application using Gunicorn with Uvicorn worker

Source: https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/uvicorn

This command starts Gunicorn using the Uvicorn worker class to serve a Django ASGI application. This setup is recommended for production environments. Replace 'myproject.asgi:application' with your project's ASGI application path.

```shell
python -m gunicorn myproject.asgi:application -k uvicorn_worker.UvicornWorker
```

--------------------------------

### Install Geospatial Libraries on Debian/Ubuntu

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install/geolibs

Installs essential geospatial libraries required by GeoDjango on Debian/Ubuntu systems. It uses apt-get to install binutils, libproj-dev, and gdal-bin, which also pull in their dependencies.

```bash
$ sudo apt-get install binutils libproj-dev gdal-bin

```

--------------------------------

### Async Support Check Example

Source: https://docs.djangoproject.com/en/6.0/ref/checks

An example of a specific system check related to asynchronous support, highlighting a security concern.

```APIDOC
## Core System Checks: Asynchronous Support

### Description
Verifies your setup for Asynchronous support.

### Check Example

*   **async.E001**: You should not set the `DJANGO_ALLOW_ASYNC_UNSAFE` environment variable in deployment. This disables async safety protection.
```

--------------------------------

### Install django-polls Package (User Install)

Source: https://docs.djangoproject.com/en/6.0/intro/reusable-apps

Installs the 'django-polls' package as a user library using pip. This method is useful for per-user installations, especially when administrator access is limited.

```bash
python -m pip install --user django-polls/dist/django_polls-0.1.tar.gz
```

--------------------------------

### Django: Basic Custom Field Example

Source: https://docs.djangoproject.com/en/6.0/howto/custom-model-fields

This is a minimal example of defining a custom Django model field. It shows the basic structure by subclassing `models.CharField` and adding a placeholder comment for custom logic. This serves as a starting point for more complex field implementations.

```python
class CustomCharField(models.CharField): ...
```

--------------------------------

### Install PostgreSQL CIText Extension using Django Migrations

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/postgres/operations

This operation is used to install the PostgreSQL 'citext' extension within a Django project's database migrations. As a specialized subclass of `CreateExtension`, it simplifies the process. The `hints` argument is available for integration with database routers, starting with Django version 6.0.

```python
from django.contrib.postgres.operations import CITextExtension


class Migration(migrations.Migration):
    ...

    operations = [CITextExtension(), ...]

```

--------------------------------

### Generate HTML Documentation (Unix/Linux)

Source: https://docs.djangoproject.com/en/6.0/intro/whatsnext

These commands navigate to the Django documentation directory and then use the 'make html' command to generate the HTML version of the documentation. This requires GNU Make to be installed.

```bash
$ cd path/to/django/docs
$ make html

```

--------------------------------

### Install Hypercorn using pip

Source: https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/hypercorn

This command installs the Hypercorn ASGI server using pip. Ensure pip is available and updated for the latest version. This is a prerequisite for running Django with Hypercorn.

```python
python -m pip install hypercorn
```

--------------------------------

### Install Python Build Tools

Source: https://docs.djangoproject.com/en/6.0/internals/howto-release-django

Installs essential Python packages for building and distributing Python packages. This includes `build` for creating distribution archives and `twine` for uploading them to package indexes.

```shell
python -m pip install build twine

```

--------------------------------

### Use Convenience Imports in Django

Source: https://docs.djangoproject.com/en/6.0/internals/contributing/writing-code/coding-style

Shows the preferred way to import classes or functions in Django using convenience imports when available. This example contrasts importing `View` directly from `django.views` versus importing it from its more specific submodule.

```python
from django.views import View
```

```python
from django.views.generic.base import View
```

--------------------------------

### Install Gunicorn using pip

Source: https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/gunicorn

Installs the Gunicorn package using Python's package installer, pip. Ensure Python and pip are installed and accessible in your environment.

```bash
python -m pip install gunicorn
```

--------------------------------

### Get GDALRaster Driver Name

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/gdal

Illustrates how to access the 'driver' attribute of a GDALRaster object to get the name of the GDAL driver used for handling the raster data. This includes examples for an in-memory raster and a GeoTIFF file.

```python
from django.contrib.gis.gdal import GDALRaster

# In-memory raster
print(GDALRaster({"width": 10, "height": 10, "srid": 4326}).driver.name)

# File-based GeoTiff raster
import tempfile
rstfile = tempfile.NamedTemporaryFile(suffix=".tif")
rst = GDALRaster({
    "driver": "GTiff",
    "name": rstfile.name,
    "srid": 4326,
    "width": 255,
    "height": 255,
    "nr_of_bands": 1,
})
print(rst.name)
print(rst.driver.name)
```

--------------------------------

### Create Django Project with `startproject`

Source: https://docs.djangoproject.com/en/6.0/ref/django-admin

Initializes a new Django project, creating the necessary directory structure and default files like `manage.py` and `settings.py`. It supports custom templates, file extensions for rendering, specific file inclusions, and directory exclusions.

```bash
django-admin startproject name [directory]
django-admin startproject myproject /Users/jezdez/Code/myproject_repo --template TEMPLATE --extension EXTENSIONS, -e EXTENSIONS --name FILES, -n FILES --exclude DIRECTORIES, -x DIRECTORIES
```

--------------------------------

### Django VERSION Tuple Examples

Source: https://docs.djangoproject.com/en/6.0/internals/howto-release-django

Illustrative examples of Django's VERSION tuple structure and how it translates to user-facing version strings. The tuple format is (major, minor, micro, status, series_number).

```python
# Example 1: Final release
VERSION = (4, 1, 1, "final", 0)  # Represents "4.1.1"

# Example 2: Pre-alpha release
VERSION = (4, 2, 0, "alpha", 0)  # Represents "4.2 pre-alpha"

# Example 3: Beta release
VERSION = (4, 2, 0, "beta", 1)   # Represents "4.2 beta 1"
```

--------------------------------

### Python f-string formatting examples

Source: https://docs.djangoproject.com/en/6.0/internals/contributing/writing-code/coding-style

Examples demonstrating allowed and disallowed usage of f-strings in Python for string variable interpolation. Complex expressions or function calls directly within f-strings are discouraged; instead, use local variable assignments for clarity. F-strings should not be used for translatable strings.

```python
# Allowed
f"hello {user}"
f"hello {user.name}"
f"hello {self.user.name}"

# Disallowed
f"hello {get_user()}"
f"you are {user.age * 365.25} days old"

# Allowed with local variable assignment
user = get_user()
f"hello {user}"
user_days_old = user.age * 365.25
f"you are {user_days_old} days old"

```

--------------------------------

### Build and Install GEOS from Source

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install/geolibs

Compiles and installs the GEOS C++ library from source. This process involves downloading the source, configuring the build with CMake, compiling, and then installing the library system-wide. This is necessary when GeoDjango cannot find the GEOS library.

```bash
$ wget https://download.osgeo.org/geos/geos-X.Y.Z.tar.bz2
$ tar xjf geos-X.Y.Z.tar.bz2
$ cd geos-X.Y.Z
$ mkdir build
$ cd build
$ cmake -DCMAKE_BUILD_TYPE=Release ..
$ cmake --build .
$ sudo cmake --build . --target install

```

--------------------------------

### Install Uvicorn and Gunicorn with pip

Source: https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/uvicorn

This command installs both Uvicorn and Gunicorn, along with the Uvicorn worker for Gunicorn. This is useful for production deployments where Gunicorn manages Uvicorn processes.

```shell
python -m pip install uvicorn uvicorn-worker gunicorn
```

--------------------------------

### Setting Proxy Environment Variables for Pip Install

Source: https://docs.djangoproject.com/en/6.0/howto/windows

This snippet shows how to set environment variables for HTTP and HTTPS proxies, which is necessary when installing Django using pip from behind a proxy server. These variables configure the proxy settings for the command prompt session.

```bash
set http_proxy=http://username:password@proxyserver:proxyport
set https_proxy=https://username:password@proxyserver:proxyport
```

--------------------------------

### Start uWSGI Server for Django (Command Line)

Source: https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/uwsgi

Starts a uWSGI server process for a Django project using command-line arguments. This configuration includes settings for project directory, WSGI module, environment variables, master process, socket, worker processes, user/group, request timeouts, and logging.

```shell
uwsgi --chdir=/path/to/your/project \
    --module=mysite.wsgi:application \
    --env DJANGO_SETTINGS_MODULE=mysite.settings \
    --master --pidfile=/tmp/project-master.pid \
    --socket=127.0.0.1:49152 \
    --processes=5 \
    --uid=1000 --gid=2000 \
    --harakiri=20 \
    --max-requests=5000 \
    --vacuum \
    --home=/path/to/virtual/env \
    --daemonize=/var/log/uwsgi/yourproject.log

```

--------------------------------

### Django Data Migration: Move Data from Old to New App

Source: https://docs.djangoproject.com/en/6.0/howto/writing-migrations

This Python script demonstrates a Django data migration to move data from a model in an 'old_app' to a model in a 'new_app'. It includes error handling for when the old app is not installed and specifies dependencies for the migration.

```python
from django.apps import apps as global_apps
from django.db import migrations


def forwards(apps, schema_editor):
    try:
        OldModel = apps.get_model("old_app", "OldModel")
    except LookupError:
        # The old app isn't installed.
        return

    NewModel = apps.get_model("new_app", "NewModel")
    NewModel.objects.bulk_create(
        NewModel(new_attribute=old_object.old_attribute)
        for old_object in OldModel.objects.all()
    )


class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
    dependencies = [
        ("myapp", "0123_the_previous_migration"),
        ("new_app", "0001_initial"),
    ]

    if global_apps.is_installed("old_app"):
        dependencies.append(("old_app", "0001_initial"))

```

--------------------------------

### Run Django Unit Tests (Windows)

Source: https://docs.djangoproject.com/en/6.0/internals/contributing/writing-code/unit-tests

This snippet outlines the command-line steps to clone the Django repository, set up a virtual environment, install requirements, and run the unit tests using the `runtests.py` script on Windows systems.

```batch
...\> git clone https://github.com/YourGitHubName/django.git django-repo
...\> cd django-repo\tests
...\> py -m pip install -e ..
...\> py -m pip install -r requirements\py3.txt
...\> runtests.py

```

--------------------------------

### Download PROJ Source and Data

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install/geolibs

Commands to download the PROJ source code archive and the necessary datum shifting files. These are prerequisites for building PROJ from source.

```bash
$ wget https://download.osgeo.org/proj/proj-X.Y.Z.tar.gz
$ wget https://download.osgeo.org/proj/proj-data-X.Y.tar.gz
```

--------------------------------

### Get Transaction Start Time with TransactionNow - Django

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/postgres/functions

The TransactionNow function returns the database server's date and time at the start of the current transaction, or the current statement's time if not in a transaction. It complements django.db.models.functions.Now. Usage involves filtering model instances based on this time.

```python
from django.contrib.postgres.functions import TransactionNow
Article.objects.filter(published__lte=TransactionNow())
```

--------------------------------

### Start Django Interactive Python Shell

Source: https://docs.djangoproject.com/en/6.0/intro/tutorial02

The `shell` command launches an interactive Python interpreter pre-configured with Django's settings and model imports. This is useful for testing the database API and performing ad-hoc operations. Use `exit()` to leave the shell.

```bash
python manage.py shell
```

```bash
py manage.py shell
```

--------------------------------

### Install Django using pip

Source: https://docs.djangoproject.com/en/6.0/howto/windows

Installs the latest version of Django using pip within an active virtual environment. This command should be executed after activating the virtual environment.

```shell
...\> py -m pip install Django
```

--------------------------------

### Run Django with Daphne command

Source: https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/daphne

This command starts the Daphne server to run your Django project. It requires the path to your project's ASGI application object.

```shell
daphne myproject.asgi:application
```

--------------------------------

### Install Python Build Package

Source: https://docs.djangoproject.com/en/6.0/intro/reusable-apps

Installs the 'build' package using pip, which is necessary for creating distributable Python packages. This command should be run within the Django project directory.

```bash
python -m pip install build
```

--------------------------------

### Define Custom File Storage with STORAGES Options

Source: https://docs.djangoproject.com/en/6.0/ref/settings

Sets up a custom file storage backend named 'example' with specific location and base URL options. This demonstrates how to configure custom storage solutions in Django.

```python
STORAGES = {
    # ...
    "example": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": "/example",
            "base_url": "/example/",
        },
    },
}
```

--------------------------------

### Configure and Build SQLite with R*Tree

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/install/spatialite

This section provides commands to configure, build, and install SQLite from source, ensuring the R*Tree module is enabled by setting the `CFLAGS` environment variable. This is necessary if your system's SQLite lacks R*Tree support.

```bash
$ CFLAGS="-DSQLITE_ENABLE_RTREE=1" ./configure
$ make
$ sudo make install
$ cd ..

```

--------------------------------

### Create Git Branch for Ticket (Shell)

Source: https://docs.djangoproject.com/en/6.0/intro/contributing

Creates a new Git branch for a specific ticket, allowing isolated development. This command assumes Git is installed and accessible in the system's PATH. The branch name 'ticket_99999' is an example.

```shell
$ git checkout -b ticket_99999
```

```shell
...\> git checkout -b ticket_99999
```

--------------------------------

### Testing Class-Based Views with RequestFactory in Django

Source: https://docs.djangoproject.com/en/6.0/topics/testing/advanced

Provides an example of testing Django class-based views outside the full request/response cycle. It shows how to instantiate a view, use RequestFactory to create a request, call the view's setup() method with the request, and then test methods like get_context_data().

```python
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "myapp/home.html"

    def get_context_data(self, **kwargs):
        kwargs["environment"] = "Production"
        return super().get_context_data(**kwargs)

```

```python
from django.test import RequestFactory, TestCase
from .views import HomeView


class HomePageTest(TestCase):
    def test_environment_set_in_context(self):
        request = RequestFactory().get("/")
        view = HomeView()
        view.setup(request)

        context = view.get_context_data()
        self.assertIn("environment", context)

```

--------------------------------

### Check Python Installation

Source: https://docs.djangoproject.com/en/6.0/howto/windows

Verifies if Python is installed and accessible via the 'py' command in the Windows command prompt. If 'py' is not found, users should use 'python' instead.

```shell
...\> py --version
```

--------------------------------

### Create Django Project with django-admin

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/gis/tutorial

Initializes a new Django project named 'geodjango' using the django-admin command-line tool. This is the first step in setting up a new Django application.

```shell
$ django-admin startproject geodjango

```

```shell
...\> django-admin startproject geodjango

```

--------------------------------

### Hybrid Middleware Function in Django

Source: https://docs.djangoproject.com/en/6.0/topics/http/middleware

This example shows a middleware function that supports both synchronous and asynchronous requests. It uses `asgiref.sync.iscoroutinefunction` to determine the nature of the `get_response` callable and adapts accordingly. The `@sync_and_async_middleware` decorator simplifies this setup.

```python
from asgiref.sync import iscoroutinefunction
from django.utils.decorators import sync_and_async_middleware


@sync_and_async_middleware
def simple_middleware(get_response):
    # One-time configuration and initialization goes here.
    if iscoroutinefunction(get_response):

        async def middleware(request):
            # Do something here!
            response = await get_response(request)
            return response

    else:

        def middleware(request):
            # Do something here!
            response = get_response(request)
            return response

    return middleware

```

--------------------------------

### Django Template: Correct `extends` Placement

Source: https://docs.djangoproject.com/en/6.0/internals/contributing/writing-code/coding-style

Illustrates the correct placement of the `{% extends %}` tag in Django templates. It must be the first non-comment line. Examples show valid placements with and without preceding comments.

```django
{% extends "base.html" %}

{% block content %}
  <h1 class="font-semibold text-xl">
    {{ pages.title }}
  </h1>
{% endblock content %}

```

```django
{# This is a comment #}
{% extends "base.html" %}

{% block content %}
  <h1 class="font-semibold text-xl">
    {{ pages.title }}
  </h1>
{% endblock content %}

```

--------------------------------

### Django Feed Class Configuration Example

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/syndication

This Python code demonstrates the structure and various optional and required attributes for creating a custom feed using Django's `Feed` class. It shows how to specify feed type, template names, language, title, link, feed URL, GUID, description, and author details. Dependencies include Django's `syndication.views.Feed` and `utils.feedgenerator`.

```python
from django.contrib.syndication.views import Feed
from django.utils import feedgenerator


class ExampleFeed(Feed):
    # FEED TYPE -- Optional. This should be a class that subclasses
    # django.utils.feedgenerator.SyndicationFeed. This designates
    # which type of feed this should be: RSS 2.0, Atom 1.0, etc. If
    # you don't specify feed_type, your feed will be RSS 2.0. This
    # should be a class, not an instance of the class.

    feed_type = feedgenerator.Rss201rev2Feed

    # TEMPLATE NAMES -- Optional. These should be strings
    # representing names of Django templates that the system should
    # use in rendering the title and description of your feed items.
    # Both are optional. If a template is not specified, the
    # item_title() or item_description() methods are used instead.

    title_template = None
    description_template = None

    # LANGUAGE -- Optional. This should be a string specifying a language
    # code. Defaults to django.utils.translation.get_language().

    language = "de"

    # TITLE -- One of the following three is required. The framework
    # looks for them in this order.

    def title(self, obj):
        """
        Takes the object returned by get_object() and returns the
        feed's title as a normal Python string.
        """

    def title(self):
        """
        Returns the feed's title as a normal Python string.
        """

    title = "foo"  # Hard-coded title.

    # LINK -- One of the following three is required. The framework
    # looks for them in this order.

    def link(self, obj):
        """
        # Takes the object returned by get_object() and returns the URL
        # of the HTML version of the feed as a normal Python string.
        """

    def link(self):
        """
        Returns the URL of the HTML version of the feed as a normal Python
        string.
        """

    link = "/blog/"  # Hard-coded URL.

    # FEED_URL -- One of the following three is optional. The framework
    # looks for them in this order.

    def feed_url(self, obj):
        """
        # Takes the object returned by get_object() and returns the feed's
        # own URL as a normal Python string.
        """

    def feed_url(self):
        """
        Returns the feed's own URL as a normal Python string.
        """

    feed_url = "/blog/rss/"  # Hard-coded URL.

    # GUID -- One of the following three is optional. The framework looks
    # for them in this order. This property is only used for Atom feeds
    # (where it is the feed-level ID element). If not provided, the feed
    # link is used as the ID.

    def feed_guid(self, obj):
        """
        Takes the object returned by get_object() and returns the globally
        unique ID for the feed as a normal Python string.
        """

    def feed_guid(self):
        """
        Returns the feed's globally unique ID as a normal Python string.
        """

    feed_guid = "/foo/bar/1234"  # Hard-coded guid.

    # DESCRIPTION -- One of the following three is required. The framework
    # looks for them in this order.

    def description(self, obj):
        """
        Takes the object returned by get_object() and returns the feed's
        description as a normal Python string.
        """

    def description(self):
        """
        Returns the feed's description as a normal Python string.
        """

    description = "Foo bar baz."  # Hard-coded description.

    # AUTHOR NAME --One of the following three is optional. The framework
    # looks for them in this order.

    def author_name(self, obj):
        """
        Takes the object returned by get_object() and returns the feed's
        author's name as a normal Python string.
        """

    def author_name(self):
        """
        Returns the feed's author's name as a normal Python string.
        """

    author_name = "Sally Smith"  # Hard-coded author name.

    # AUTHOR EMAIL --One of the following three is optional. The framework
    # looks for them in this order.

    def author_email(self, obj):
        """
        Takes the object returned by get_object() and returns the feed's
        author's email as a normal Python string.
        """

    def author_email(self):
        """
        Returns the feed's author's email as a normal Python string.
        """

    author_email = "test@example.com"  # Hard-coded author email.

    # AUTHOR LINK --One of the following three is optional. The framework
    # looks for them in this order. In each case, the URL should include
    # the scheme (such as "https://") and domain name.

    def author_link(self, obj):
        """
        Takes the object returned by get_object() and returns the feed's
        author's URL as a normal Python string.
        """

    def author_link(self):
        """

```

--------------------------------

### Check Django Version

Source: https://docs.djangoproject.com/en/6.0/intro/tutorial01

Command to verify if Django is installed and display its version. It can be run using 'python -m' or 'py -m' depending on the system's Python installation.

```shell
$ python -m django --version

```

```shell
...\> py -m django --version

```

--------------------------------

### Get Inline Instances in Django Admin

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/admin

The `get_inline_instances` method returns a list of `InlineModelAdmin` objects for the given model and request. It can be overridden to customize which inlines are displayed, for example, by bypassing default permission checks.

```python
class MyModelAdmin(admin.ModelAdmin):
    inlines = [MyInline]

    def get_inline_instances(self, request, obj=None):
        return [inline(self.model, self.admin_site) for inline in self.inlines]

```

--------------------------------

### Django post_init Signal Example

Source: https://docs.djangoproject.com/en/6.0/ref/signals

This example shows how to connect a receiver to the `post_init` signal, which is sent after a Django model's `__init__()` method has finished. It demonstrates accessing the sender and the newly created instance.

```python
from django.db.models.signals import post_init
from django.dispatch import receiver

@receiver(post_init)
def post_init_handler(sender, instance, **extra_kwargs):
    print(f"Post-init signal received for {sender.__name__}")
    print(f"Instance: {instance}")
    # Note: instance._state is not fully set at this point

# Example usage:
# class MyModel(models.Model):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # ... other initialization code

# When an instance of MyModel is created, the post_init_handler will be called after __init__ completes.
```

--------------------------------

### Django Cached Sitemap Index URLconf Setup

Source: https://docs.djangoproject.com/en/6.0/ref/contrib/sitemaps

This example shows how to configure Django's URL patterns for a sitemap index with caching enabled. It uses `cache_page` decorator and specifies `sitemap_url_name` for the index view.

```python
from django.contrib.sitemaps import views as sitemaps_views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path(
        "sitemap.xml",
        cache_page(86400)(sitemaps_views.index),
        {"sitemaps": sitemaps, "sitemap_url_name": "sitemaps"},
    ),
    path(
        "sitemap-<section>.xml",
        cache_page(86400)(sitemaps_views.sitemap),
        {"sitemaps": sitemaps},
        name="sitemaps",
    ),
]
```
