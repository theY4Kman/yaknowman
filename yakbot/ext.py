CMDNAME_ATTR = '__cmdname__'
ALIASES_ATTR = '__aliases__'


def command(name=None, aliases=()):
    """ Decorator to register a command handler in a Plugin. """
    fn = None
    if callable(name):
        fn = name
        name = None

    def _command(fn):
        setattr(fn, CMDNAME_ATTR, fn.__name__ if name is None else name)
        setattr(fn, ALIASES_ATTR, aliases)
        return fn

    if fn:
        return _command(fn)

    return _command


class PluginMeta(type):
    def __new__(cls, name, bases, attrs):
        plugin = type.__new__(cls, name, bases, attrs)
        if bases == (object,):
            # Skip metaclass magic for Plugin base class
            return plugin

        if plugin.name is None:
            setattr(plugin, 'name', name)

        commands = []
        for name, value in attrs.iteritems():
            if callable(value) and hasattr(value, CMDNAME_ATTR):
                cmdname = getattr(value, CMDNAME_ATTR)
                aliases = getattr(value, ALIASES_ATTR, ())
                commands.append((cmdname, value, aliases))
        plugin._commands = commands

        return plugin


class Plugin(object):
    __metaclass__ = PluginMeta

    name = None         # Populated with the class name if None
    private = False     # Whether the plug-in should be hidden in !list

    _commands = None

    def __init__(self, yakbot, irc):
        self.yakbot = yakbot
        self.irc = irc

    def __hash__(self):
        return hash(self.name)

    def on_unload(self):
        pass
