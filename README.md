Online Ledger
==

Server interaction
--

Start the app using:
> docker-compose up

For running shell commands within the running app, prefix them with `docker-compose exec django`

For example database migrations are performed with the following command:
> docker-compose exec django python manage.py migrate

Or for executing a script:
> docker-compose exec django python manage.py runscript -v2 ping --script-args hello

Removing volumes when shutting down:
> docker-compose down -v

For building a new Django docker image after an update:
> docker-compose build

The command above takes several minutes to complete because the image includes Pandas and Matplotlib.

Database
--
PostgreSQL terminal (non-interactive), show all tables:
> docker-compose exec django-db psql -d oas -U oas -c \\dt

