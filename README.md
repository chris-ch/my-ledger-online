my-ledger-online
===========================

Online Bookkeeping

After the first start using
> docker-compose up

Run this command:
> docker-compose exec django python manage.py migrate

Removing volumes when shutting down:
> docker-compose down -v

Executing a script:
> docker-compose exec django python manage.py runscript -v2 ping --script-args hello

