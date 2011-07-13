# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Simpack for simulating a queue.

`Queueing Theory`_ is the mathematical study of clients waiting in a queue.
These can be shoppers waiting in line for a cashier in a supermarket, or
product components waiting in a complex queue to be processed by different
machines in a factory. Queueing Theory has applications in diverse fields,
including telecommunications, traffic engineering, computing and the design of
factories, offices and hospitals.

In this simple simpack, clients from an infinite population arrive at a
facility and wait to be serviced by a bunch of servers. They wait in a single
queue. Sometimes the queue grows large when the servers take a long time to
service the clients.

The clients arrive according to a `Poisson distribution`_ and servers finish
servicing them according to a Poisson distribution.

.. _Queueing Theory: http://en.wikipedia.org/wiki/Queueing_theory
.. _Poisson distribution: http://en.wikipedia.org/wiki/Poisson_distribution

'''

from .state import State

name = 'Queueing Theory'

tags = ('queueing-theory', 'poisson-distribution')