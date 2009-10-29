# How to run #

Run `run_gui.py` in the root folder to launch the GUI. Then, File -> New. Choose one of the simulation packages, press Ok. A dialog will pop up, press Ok. Double click the seek bar to toggle playing.

Tested on [Python 2.6](http://www.python.org/download/releases/2.6.4/). Requires [wxPython](http://www.wxpython.org/). Optional: [Psyco](http://psyco.org), on Windows: [Python for Windows Extensions](http://sourceforge.net/projects/pywin32/).

# What is GarlicSim? #

GarlicSim is an ambitious open-source project in the field of scientific computing, specifically computer simulations. It attempts to redefine the way that people think about computer simulations, making a new standard for how simulations are created and used.

GarlicSim is a platform for writing, running and analyzing simulations. It is general enough to handle any kind of simulation: Physics, game theory, epidemic spread, electronics, etc.

When you're writing a simulation, about 90% of the code you write is boilerplate; Code that isn't directly related to the phenomenon you're simulating, but is necessary for your simulation to work. The aim of GarlicSim is to write that 90% of the code once and for all, and to do it well, so you could concentrate on the important 10%.

GarlicSim defines a new format for simulations. It's called a **simulation package**, and often abbreivated as **simpack**. For example, say you are interested in simulating the interaction of hurricane storms. It is up to you to write a simpack for this type of simulation. The simpack is simply a Python package which defines a few special functions according to the GarlicSim simpack API, the most important function being the **step function**.

The beauty is that since so many simulation types can fit into this mold of a simpack, the tools that GarlicSim provides can be used across all of these different domains. Once you plug your own simpack into GarlicSim, you're ready to roll. All the tools that GarlicSim provides will work with your simulation.

Additionally, GarlicSim will eventually be shipped with a standard library of simpacks for common simulations, that the user may find useful to use as-is, or with his own modifications.

For a more thorugh introduction to how GarlicSim works, check out the ** [Introduction to GarlicSim](http://dl.getdropbox.com/u/1927707/Introduction%20to%20GarlicSim.doc) ** - Though not yet complete, it goes deep into the principles of GarlicSim and how to work with it.

GarlicSim is written in Python.

-------

Current screenshot, showing the [Game of Life](http://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) simulation package shipped with the program:

![](http://garlicsim.org/images/screenshot.gif)

-------

Mockup:

![](http://garlicsim.org/images/mockup_thumb.gif)

# Frequently Asked Question: #

_What kind of simulations will I be able to do with GarlicSim?_

People often ask this; probably because they do not fully believe it when they read GarlicSim's description saying that it can handle any kind of simulation. Well, it can. It is very general.

Then people ask, if it is so general, how is it useful? There are two answers to that:

1.  It is very useful. There are many many features that are common to all kinds of simulations, and which you really don't want to spend time writing. A few examples of such features: Saving the simulation to file. Browsing the timeline of a simulation like a movie clip while it is still crunching in the background. The option to make manual changes to the simulation world, observe their effects on how the simulation unfolds, and then to be able to revert to the timeline in which the changes were not applied. Changing the arguments to the step function on the fly, etc.

2.  If you are interested in only a specific subset of simulations -- say, simulations of solid bodies in Physics -- Then it will be the wisest to write a framework for that within the framework of GarlicSim. Indeed, part of the work on GarlicSim will include writing these kind of sub-frameworks for the common categories of simulations (e.g., a framework for physics, a framework for game theory, etcetera.)

# Licensing #

GarlicSim is comprised of two packages, `garlicsim` which is the business logic, and `garlicsim_wx`, which is the wxPython-based GUI. Both packages are copyright 2009 Ram Rachum. The `garlicsim` package is distributed under the LGPL2.1 license. The `garlicsim_wx` package is not licensed for distribution.