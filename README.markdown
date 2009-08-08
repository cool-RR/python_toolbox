Run `rundemo.py` in the src folder to see the demonstration. Then, File -> New. Choose one of the simulation packages, press Ok. A dialog will pop up, press Ok. Double click the seek bar to toggle playing.

Tested on [Python 2.6](http://www.python.org/download/releases/2.6.2/). Requires [wxPython](http://www.wxpython.org/). Optional: [Python for Windows Extensions](http://sourceforge.net/projects/pywin32/).


-----------

GarlicSim is a platform for writing, running and analyzing simulations. It can handle any kind of simulation: Physics, game theory, epidemic spread, electronics, etc.

The program is written in Python.


When you're writing a simulation, about 90% of the code you write is boilerplate; Code that isn't directly related to the phenomenon you're simulating, but is necessary for your simulation to work.
The aim of GarlicSim is to write that 90% of the code once and for all, and to do it well, so you could concentrate on the important 10%.

Additionally, we intend to ship GarlicSim with a standard library of common simulations, that the user may find useful to use as-is, or with his/her own modifications.

*__Serious Python coders are needed.
If you are interested, [contact me](mailto:cool-rr@cool-rr.com).__*

-------

Mockup:

![](http://garlicsim.com/images/mockup_thumb.gif)

-------

**Frequently Asked Question:**

_What kind of simulations will I be able to do with GarlicSim?_

People often ask this; probably because they do not fully believe it when they read GarlicSim's description saying that it can handle any kind of simulation. Well, it can. It is very general.

Then people ask, if it is so general, how is it useful? There are two answers to that:

1.  It is very useful. There are many many features that are common to all kinds of simulations, and which you really don't want to spend time writing. A few examples of such features: Saving the simulation to file. Browsing the timeline of a simulation like a movie clip while it is still crunching in the background. The option to make manual changes to the simulation world, observe their effects on how the simulation unfolds, and then to be able to revert to the timeline in which the changes were not applied. The option to change the "step" function of a simulation on the fly. Etcetera. And, of course, having a great GUI that was built specifically for running simulations.

2.  If you are interested in only a specific subset of simulations -- say, simulations of solid bodies in Physics -- Then it will be the wisest to write a framework for that within the framework of GarlicSim. Indeed, part of the work on GarlicSim will include writing these kind of sub-frameworks for the common categories of simulations (e.g., a framework for physics, a framework for game theory, etcetera.)


-------

This project is licensed under the MIT license.