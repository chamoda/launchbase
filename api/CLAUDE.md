## Python Development

- We are using uv in the project. So every command you run related to python start them with `uv run`

### Development guidelines

- Use `uv run alembic revision --autogenerate` create migration file. Only manual edit you are supposed to do is adding server_default to handle nullable situation. If you need some fancy data migration do it in seperate `uv run manage.py` custom command
- Don't need to add tests in MVP iterations, move fast

### API Development Best Practices

- When you make any changes to APIs make sure to update requests.org file (it's emacs verb plugin file written in org mode)
- Use MUST use common REST API design guidelines
- Never session.commit() in services, only session.flush() in service and let router layer commit



