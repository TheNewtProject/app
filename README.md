# IMPORTANT {#important}

#### **The Newt Plugin API is deprecated! Please use build overrides and buildsets instead.**


# Newt {#}

Newt is a lightweight community-made text editor made in Python.

Features Include:

- Theme Support
- Build Overrides
- Buildsets


## Theme Example {#theme}

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


## Build Override Example {#override}

1. First, move to the root directory of your installation of Newt.

2. Create a new file using `snake_case`, and give it a name with the `.py` extension.

3. Inside this file, write the following boilerplate code to start a new build override:

```py
from framework import newt as fw

class OverrideName(fw.Newt):
    def override_name(self):
        ...
```

4. Your build override is ready!

Using build overrides, you can change the entire functionality and look of Newt, without disturbing your `main.py` file or the actual application itself!

Build overrides also modify the application directly, instead of running in the background. This means that build overrides have more flexibility and capibilities than a plugin does.

However, build overrides do nothing on their own. You will need to create a buildset and import and run your overrides.



## Buildset Example {#buildset}

Buildsets are a compilation of build overrides that are run alongside each other.

1. First, move to the root directory of your installation of Newt.

2. Create a new file using `snake_case`, and give it a name with the `.py` extension.

3. Inside this file, write the following boilerplate code to start a new build override:

```py
from framework import newt as fw
from override1 import Override1
from override2 import Override2

class BuildsetName(Override1, Override2):
    def run(self):
        self.override_1()
        self.override_2()
        self.root.mainloop()

if __name__ == '__main__':
    BuildsetName().run()
```

There you go! You may need to make some modifications, but your buildset is ready!

4. Run the file you created using the following command:

`py buildset_name.py`

Note that buildsets do not merge overrides. 

If anything is shared between the overrides in the buildset, the lowest in the list will take priority, and the priority gets lower the higher you go in the list of overrides.