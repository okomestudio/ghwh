from jinja2 import Environment
from jinja2 import PackageLoader


env = Environment(loader=PackageLoader(__name__, 'payloads'))


def render(template, context=None):
    tmpl = env.get_template(template + '.j2')
    return tmpl.render(**(context or {}))
