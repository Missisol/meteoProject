- Run app ``flask run --host=0.0.0.0``
- Command for working with the database entities without having to import them ``flask shell``
- Setting up a scheduled job with cron 
    - ``crontab -e``
    - ``* * * * * cd <path_to_project_directory> && .venv/bin/flask <command_name>``

