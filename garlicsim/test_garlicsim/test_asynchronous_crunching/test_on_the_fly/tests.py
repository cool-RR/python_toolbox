# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.


from __future__ import division
from __future__ import with_statement

import re
import os
import types
import time
import itertools
import cPickle, pickle

import nose

from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import math_tools
from garlicsim.general_misc import path_tools
from garlicsim.general_misc import address_tools
from garlicsim.general_misc import import_tools
from garlicsim.general_misc.infinity import infinity

import garlicsim

import test_garlicsim

from ..shared import MustachedThreadCruncher


def test():
    '''Test changing things while crunching.'''
    from . import simpacks as simpacks_package
    
    # Collecting all the test simpacks:
    simpacks = import_tools.import_all(simpacks_package).values()
    
    # Making sure that we didn't miss any simpack by counting the number of
    # sub-folders in the `simpacks` folder:
    simpacks_dir = \
        os.path.dirname(simpacks_package.__file__)
    assert len(path_tools.list_sub_folders(simpacks_dir)) == \
           len(simpacks)
    
    for simpack in simpacks:
        
        test_garlicsim.verify_simpack_settings(simpack)
        
        cruncher_types = \
            garlicsim.misc.SimpackGrokker(simpack).available_cruncher_types
        
        for cruncher_type in cruncher_types:
            yield check, simpack, cruncher_type

        
def check(simpack, cruncher_type):
    
    
    my_simpack_grokker = garlicsim.misc.SimpackGrokker(simpack)
    
    assert my_simpack_grokker is garlicsim.misc.SimpackGrokker(simpack)
    # Ensuring caching works.
    
    assert garlicsim.misc.simpack_grokker.step_type.StepType.get_step_type(
        my_simpack_grokker.default_step_function
    ) == simpack._test_settings.DEFAULT_STEP_FUNCTION_TYPE
    
    step_profile = my_simpack_grokker.build_step_profile()
    deterministic = \
        my_simpack_grokker.settings.DETERMINISM_FUNCTION(step_profile)
    
    state = simpack.State.create_root()
    
    
    project = garlicsim.Project(simpack)
        
    project.crunching_manager.cruncher_type = cruncher_type
    
    assert project.tree.lock._ReadWriteLock__writer is None
    
    root = project.root_this_state(state)

    def run_sync_crunchers_until_we_get_at_least_one_node():
        while not project.sync_crunchers():
            time.sleep(0.1)

    ### Test changing clock target on the fly: ################################
    #                                                                         #

    huge_number = 10 ** 20
    different_huge_number = huge_number + 1
    assert different_huge_number - huge_number == 1
    
    job = project.begin_crunching(root, huge_number)    
    run_sync_crunchers_until_we_get_at_least_one_node()
    (cruncher,) = project.crunching_manager.crunchers.values()
    
    ## An interlude to test `__repr__` methods: ###############################
    
    step_profile_description = repr(job.crunching_profile.step_profile)
    assert step_profile_description == \
        'StepProfile(%s)' % simpack._test_settings.DEFAULT_STEP_FUNCTION
    
    short_step_profile_description = \
            job.crunching_profile.step_profile.__repr__(short_form=True)
    assert short_step_profile_description == \
        '%s(<state>)' % address_tools.describe(
            simpack._test_settings.DEFAULT_STEP_FUNCTION,
            shorten=True,
            root=simpack,
        )
    
    crunching_profile_description = repr(job.crunching_profile)
    assert crunching_profile_description == \
           'CrunchingProfile(clock_target=%d, step_profile=%s)' % \
           (huge_number, short_step_profile_description)
    
    job_description = repr(job)
    assert job_description == 'Job(node=%s, crunching_profile=%s)' % \
           (repr(job.node), crunching_profile_description)
    
    crunching_manager_description = repr(project.crunching_manager)
    assert re.match(
        ('^<.*?CrunchingManager currently employing 1 crunchers to '
         'handle 1 jobs at .*?>$'),
        crunching_manager_description
    )
    
    project_description = repr(project)
    assert re.match(
        '<.*?Project containing .*? nodes and employing 1 crunchers at .*?>',
        project_description
    )
    
    # Assert the job cruncher is not unequal to itself:
    assert not job.crunching_profile.__ne__(job.crunching_profile)
    
    ## Finished interlude to test `__repr__` methods. #########################
        
    job.crunching_profile.raise_clock_target(different_huge_number)
    # Letting our crunching manager update our cruncher about the new clock
    # target:
    project.sync_crunchers()
    assert not job.is_done()
    (same_cruncher,) = project.crunching_manager.crunchers.values()
    # todo: On slow machines cruncher doesn't get created fast enough for the
    # above assert to work. Probably make some function that waits for it.
    assert same_cruncher is cruncher
    
    # Deleting jobs so the cruncher will stop:
    del project.crunching_manager.jobs[:]
    project.sync_crunchers()
    assert not project.crunching_manager.jobs
    assert not project.crunching_manager.crunchers
    
    #                                                                         #
    ### Finish testing changing clock target on the fly. ######################
    
    ### Test changing step profile on the fly: ################################
    #                                                                         #
    
    # For simpacks providing more than one step function, we'll test changing
    # between them. This will exercise the crunching manager's policy of
    # switching crunchers immediately when the step profile for a job gets
    # changed.
    if simpack._test_settings.N_STEP_FUNCTIONS >= 2:        
        default_step_function, alternate_step_function = \
            my_simpack_grokker.all_step_functions[:2]
        job = project.begin_crunching(root, infinity)
        assert job.crunching_profile.step_profile.step_function == \
               default_step_function
        run_sync_crunchers_until_we_get_at_least_one_node()
        (cruncher,) = project.crunching_manager.crunchers.values()
        alternate_step_profile = \
            garlicsim.misc.StepProfile(alternate_step_function)
        job.crunching_profile.step_profile = alternate_step_profile
        # Letting our crunching manager get a new cruncher for our new step
        # profile:
        project.sync_crunchers()
        (new_cruncher,) = project.crunching_manager.crunchers.values()
        assert new_cruncher is not cruncher
        last_node_with_default_step_profile = job.node
        assert not last_node_with_default_step_profile.children # It's a leaf
        assert last_node_with_default_step_profile.\
               step_profile.step_function == default_step_function
        # Another `sync_crunchers`:
        run_sync_crunchers_until_we_get_at_least_one_node()
        # And now we have some new nodes with the alternate step profile.
        (first_node_with_alternate_step_profile,) = \
            last_node_with_default_step_profile.children
        path = last_node_with_default_step_profile.make_containing_path()
 
        nodes_with_alternate_step_profile = list(
            path.__iter__(head=first_node_with_alternate_step_profile)
        )
        for node in nodes_with_alternate_step_profile:
            assert node.step_profile == alternate_step_profile
        
        # Deleting jobs so the cruncher will stop:
        del project.crunching_manager.jobs[:]
        project.sync_crunchers()
        assert not project.crunching_manager.jobs
        assert not project.crunching_manager.crunchers
        
    #                                                                         #
    ### Finished testing changing step profile on the fly. ####################
    
    ### Testing cruncher type switching: ######################################
    #                                                                         #
    
    job_1 = project.begin_crunching(root, clock_buffer=infinity)
    job_2 = project.begin_crunching(root, clock_buffer=infinity)
    
    assert len(project.crunching_manager.crunchers) == 0
    assert project.sync_crunchers() == 0
    assert len(project.crunching_manager.crunchers) == 2
    (cruncher_1, cruncher_2) = project.crunching_manager.crunchers.values()
    assert type(cruncher_1) is cruncher_type
    assert type(cruncher_2) is cruncher_type
    
    time.sleep(0.2) # Letting the crunchers start working
    
    project.crunching_manager.cruncher_type = MustachedThreadCruncher
    project.sync_crunchers()
    assert len(project.crunching_manager.crunchers) == 2
    (cruncher_1, cruncher_2) = project.crunching_manager.crunchers.values()
    assert type(cruncher_1) is MustachedThreadCruncher
    assert type(cruncher_2) is MustachedThreadCruncher
    
    project.crunching_manager.cruncher_type = cruncher_type
    project.sync_crunchers()
    assert len(project.crunching_manager.crunchers) == 2
    (cruncher_1, cruncher_2) = project.crunching_manager.crunchers.values()
    assert type(cruncher_1) is cruncher_type
    assert type(cruncher_2) is cruncher_type
    
    # Deleting jobs so the crunchers will stop:
    del project.crunching_manager.jobs[:]
    project.sync_crunchers()
    assert not project.crunching_manager.jobs
    assert not project.crunching_manager.crunchers
    
    #                                                                         #
    ### Finished testing cruncher type switching. #############################
    
    
    