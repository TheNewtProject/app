## Plugin Example

### Synchronous

1. First, move to the root directory of your installation of Newt, which will contain the `main.py` file that comes with the standard installation of Newt.

2. Create a new file using `snake_case`, and give it a name with the `.py` extension.

3. Inside your plugin file (we will call this `plugin.py` in this example for convenience), write the following boilerplate code to start a new plugin:

```py
from framework.plugins import Plugin

class MyPlugin(Plugin):
    def run(self, app):
        ...
```

4. Replace the `...` with your plugin code.

5. Move into your `main.py` file, and add the following code:

```py
from framework import newt as fw
from framework import plugins
import importlib

app = fw.Newt()

plugin = importlib.import_module("your_plugin_file_name_here_without_extension")

plugins.Plugin.run_all(app)
app.run()
```

6. Run your `main.py` file, and your plugin will automagically attach itself to the application!

### Asynchronous

1. First, move to the root directory of your installation of Newt, which will contain the `main.py` file that comes with the standard installation of Newt.

2. Create a new file using `snake_case`, and give it a name with the `.py` extension.

3. Inside your plugin file (we will call this `aioplugin.py` in this example for convenience), write the following boilerplate code to start a new asynchronous plugin:

```py
from framework.plugins import AsyncPlugin

class MyAsyncPlugin(AsyncPlugin):
    async def run(self, app):
        ...
```

4. Replace the `...` with your plugin code.

5. Move into your `aiomain.py` file, and add the following code:

```py
import asyncio
import importlib
from framework import newt as fw
from framework import plugins


async def main():
    app = fw.Newt()
    plugin = importlib.import_module("aioplugin")
    await plugins.AsyncPlugin.run_all(app)
    await app.run_async()

asyncio.run(main())
```

6. Run your `aiomain.py` file, and your plugin will automagically attach itself to the application!