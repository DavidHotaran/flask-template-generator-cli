# Python CLI that helps scaffold a Flask app.

### Removes the tedious setup and boilerplate when setting up a Flask app.

- Clones down sample app with routes, schema, model and blueprints already setup.
- CLI command to create route, schema and model.

```bash
usage: template-generator.py [-h] {scaffold,create} ...

options:
  -h, --help         show this help message and exit

scaffold commands:
  {scaffold,create}
    scaffold         create a project template
    create           create a route, model, schema or all of the above files
```