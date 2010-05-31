# Brief Video Introduction #

[![](http://garlicsim.org/images/video_thumbnail.jpg)](http://garlicsim.org/brief_introduction.html)


# Documentation #

[Main documentation site](http://docs.garlicsim.org)

[Installation](http://docs.garlicsim.org/intro/installation/python-2.x.html)

[FAQ](http://docs.garlicsim.org/misc/faq.html)

[Mailing lists](http://docs.garlicsim.org/misc/mailing-lists.html)

If you wish, it's possible to just run the gui and play with it without installing anything. To do so, download the repo and run the `run_gui.py` file in the root folder.


# What is GarlicSim? #

GarlicSim is an ambitious open-source project in the field of scientific computing, specifically computer simulations. It attempts to redefine the way that people think about computer simulations, making a new standard for how simulations are created and used.

GarlicSim is a platform for writing, running and analyzing simulations. It is general enough to handle any kind of simulation: Physics, game theory, epidemic spread, electronics, etc.

When you're writing a simulation, about 90% of the code you write is boilerplate; Code that isn't directly related to the phenomenon you're simulating, but is necessary for your simulation to work. The aim of GarlicSim is to write that 90% of the code once and for all, and to do it well, so you could concentrate on the important 10%.

GarlicSim defines a new format for simulations. It's called a **simulation package**, and often abbreviated as **simpack**. For example, say you are interested in simulating the interaction of hurricane storms. It is up to you to write a simpack for this type of simulation. The simpack is simply a Python package which defines a few special functions according to the GarlicSim simpack API, the most important function being the **step function**.

The beauty is that since so many simulation types can fit into this mold of a simpack, the tools that GarlicSim provides can be used across all of these different domains. Once you plug your own simpack into GarlicSim, you're ready to roll. All the tools that GarlicSim provides will work with your simulation.

Additionally, GarlicSim will eventually be shipped with a standard library of simpacks for common simulations, that the user may find useful to use as-is, or with his own modifications.

For a more thorough introduction to how GarlicSim works, check out the [documentation](http://docs.garlicsim.org).

GarlicSim itself is written in pure Python. The speed of simulations is mostly dependent on the simpack's performance - So it is possible to use C code in a simpack to make things faster.

-------

Current screenshot, showing the [Game of Life](http://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) simulation package shipped with the program:

![](http://garlicsim.org/images/screenshot.png)


# Mailing lists #

The main mailing list is **[garlicsim@librelist.org](mailto:garlicsim@librelist.org)**.

The development mailing list is **[garlicsim.dev@librelist.org](mailto:garlicsim.dev@librelist.org)**.

To subscribe just send an email. These lists are hosted by [librelist](http://librelist.org), which is currently slightly experimental.


# Core and GUI #

This repository contains three packages: `garlicsim`, which is the core logic, `garlicsim_lib`, which is a collection of simpacks, and `garlicsim_wx`, which is the wxPython-based GUI. 

The `garlicsim` package is the important one, and its code is well-organized and very readable.

The `garlicsim` and `garlicsim_lib` packages are distributed under the **LGPL2.1 license**. 

`garlicsim_wx` is in a less mature state than `garlicsim`. Also, it is not licensed as open source. (Though the source code is available and not obfuscated.) I have not yet decided if the gui will be developed as an open source project or as commercial software, so in the meantime it is officially closed source.

If you require an official license, [contact me](mailto:cool-rr@cool-rr.com) and I'll probably give you one.

Both packages are copyright 2009-2010 Ram Rachum. 


# Python versions #
 
GarlicSim supports Python versions 2.5 and up, not including Python 3.x.

There is a [separate fork of GarlicSim](http://github.com/cool-RR/GarlicSim-for-Python-3.x) that supports Python 3.x. Take note though that it does not contain a GUI, because wxPython does not support Python 3.x.


# Current state #

Garlicsim is at version 0.5, which is an alpha release. It is still very experimental, and there are probably many bugs. If you run into any trouble, let us know immediately in the [mailing list](mailto:garlicsim@librelist.org).

At this experimental stage of the project, backward compatibility will _not_ be maintained. However, I will be available to assist in issues related to backward compatibility.
