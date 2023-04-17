# IMPORTANT

#### **The Newt Plugin API is deprecated! Please use build overrides and buildsets instead.**


# Newt

Newt is a lightweight community-made text editor made in Python.

Features Include:

- Theme Support
- Build Overrides
- Buildsets


## Theme Example

```ini
[root]
background = black
foreground = white

[text]
background = black
foreground = white
insert-background = white
font-family = Consolas
font-size = 12
wrap = word

[menu-bar]
background = black
foreground = white
active-background = #202020
active-foreground = white

[file-menu]
background = black
foreground = white
active-background = #202020
active-foreground = white

[edit-menu]
background = black
foreground = white
active-background = #202020
active-foreground = white

[run-menu]
background = black
foreground = white
active-background = #202020
active-foreground = white

[toolbar]
background = black

[tools]
background = black
foreground = white
active-background = #202020
active-foreground = white
```

This is a theme that can be used to customize the appearance of Newt. This theme is called AMOLED, and is bundled with the Newt standard installation.


## Build Override Example

1. First, move to the root directory of your installation of Newt.

2. Create a new file using `snake_case`, and give it a name with the `.py` extension.

3. Inside this file, write the following boilerplate code to start a new build override:

```py
from framework import newt as fw

class AwesomeOverride(fw.Newt):
    def awesome_override(self):
        ...

    def run(self):
        self.awesome_override()
        self.root.mainloop()

if __name__ == "__main__":
    AwesomeOverride().run()
```

4. Instead of running `newt.py`, `main.py`, or `aiomain.py`, instead run your build override file.

5. Your build override is ready!

Using build overrides, you can change the entire functionality and look of Newt, without disturbing your `main.py` file or the actual application itself!

Build overrides also modify the application directly, instead of running in the background. This means that build overrides have more flexibility and capibilities than a plugin does.


## Buildset Example

Buildsets are a compilation of build overrides that are run alongside each other.

However, build overrides require slightly more configuration to work, and if you want to use multiple build overrides, you may need to edit the overrides first.

1. First, move to the root directory of your installation of Newt.

2. Create a new file using `snake_case`, and give it a name with the `.py` extension.

3. Inside this file, write the following boilerplate code to start a new build override, but DO NOT override the `run` function unless it is required, except for inside your buildset:

```py
from framework import newt as fw
from override1 import AwesomeOverride
from override2 import CoolOverride

class MyBuildset(AwesomeOverride, CoolOverride):
    def run(self):
        self.awesome_override()
        self.cool_override()
        self.root.mainloop()

if __name__ == '__main__':
    MyBuildset().run()
```

There you go! You may need to make some modifications, but your buildset is ready!

4. Run the file you created using the following command:

`py YOUR_BUILDSET_FILE.py`

Note that the buildset does not merge overrides. 

If anything is shared between the overrides in the buildset, the lowest in the list will take priority, and the priority gets lower the higher you go in the list of overrides.