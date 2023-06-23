============
Todo project
============

Example project using htmx


Local development
=================


Setup
-----

Check out the repository into a new dir:

.. code-block:: bash

    mkdir todo
    cd todo
    git clone ... repo
    cd repo
    cp docker-compose.dev.yml.default docker-compose.dev.yml


This, along with the commands below, would normally be put in a shortcut file somewhere.
I use `workdir <https://pypi.org/project/workenv/>`_, others use Makefile, Taskfile,
local fabric commands etc.


Running - tl;dr
---------------

In different terminals:

.. code-block:: bash

    docker compose -f docker-compose.dev.yml up postgres
    docker compose -f docker-compose.dev.yml up backend
    docker compose -f docker-compose.dev.yml exec backend /bin/bash


Running - details
-----------------

**Start postgres in docker:**

.. code-block:: bash

    docker compose -f docker-compose.dev.yml up postgres


Then there are three options to run Python:


1.  **Either run Python outside docker:**

    Often easiest if you have no OS dependencies and you trust the code - easiest to use
    with IDEs.

    .. code-block:: bash

        python -m venv ../venv
        . ../venv/bin/activate
        pip install -r requirements.txt

        ./manage.py migrate
        ./manage.py runserver 0:8000

    If you start adding env vars without defaults, you'll also need an env file.


2.  **Or use docker to ``runserver``**

    Best for a reasonably stable project where you don't need to keep stopping and
    starting the server and you want an environment consistent with prod and other devs.

    .. code-block:: bash

        docker compose -f docker-compose.dev.yml up backend

    You can then connect to the running container to run additional commands:

    .. code-block:: bash

        docker compose -f docker-compose.dev.yml exec backend /bin/bash

        ./manage.py createsuperuser


3.  **Or use docker as a virtual machine:**

    Same as 2, but slightly less delay each time you stop and restart the server.

    #. Start the container::

          docker compose -f docker-compose.dev.yml run --service-ports --entrypoint=/bin/bash backend

    #. Start Django as you would normally::

          ./manage.py migrate
          ./manage.py runserver 0:8000

    #. In another shell, connect to the running container to run additional commands::

          docker compose -f docker-compose.dev.yml exec backend /bin/bash

          ./manage.py createsuperuser

The site is then available at http://localhost:8000/. I use a wildcard localhost DNS
entry, eg http://todo.local.uzeweb.com:8000/. I can then have additional logins at
http://todo-anon.local.uzeweb.com:8000/, http://todo-admin.local.uzeweb.com:8000/
etc without needing to shuffle browser profiles or cookies.


Working with the database
-------------------------

To dump from the database:

.. code-block:: bash

    docker-compose -f docker-compose.dev.yml exec postgres /project/docker/postgres/dump.sh

The dumped file is in ``../docker-store/backup``

To load the database from a dump (default ``database.dump``):

.. code-block:: bash

    docker-compose -f docker-compose.dev.yml exec postgres /project/docker/postgres/restore.sh



Changing requirements
---------------------

This project uses ``pip-tools``:

#. Modify ``requirements.in``
#. Run ``pip-compile``
#. Run ``pip-sync``


Linting
-------

Install pre-commit::

    pip install pipx
    pipx install pre-commit
    pre-commit install

Run manually::

    pre-commit run --all-files

Skip checks during commit::

    git commit --no-verify


Testing
=======

Use ``mypy`` to type check:

.. code-block:: bash

  mypy


Use ``pytest`` to run the tests on your current installation:

.. code-block:: bash

  pytest
