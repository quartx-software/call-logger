# Standard lib
import pkgutil

# Package
from call_logger import config, plugins

# Import all plugin's so they can be registered
prefix = plugins.__name__ + "."
for _, modname, _ in pkgutil.iter_modules(plugins.__path__, prefix):
    __import__(modname)


def main(plugin_name):
    plugin_settings = config.get(plugin_name)
    timeout_settings = {
        "timeout": config["settings"]["timeout"],
        "max_timeout": config["settings"]["max_timeout"],
        "decay": config["settings"]["decay"]
    }

    # Select phone system plugin that is used to fetch call logs
    plugin = plugins.get_plugin(plugin_name)

    # Start the plugin and monitor for call logs
    plugin_ins = plugin(**plugin_settings, **timeout_settings)
    plugin_ins.run()


# Start the call monitoring software
if __name__ == "__main__":
    name = config["settings"]["phone_system"]
    main(name)
