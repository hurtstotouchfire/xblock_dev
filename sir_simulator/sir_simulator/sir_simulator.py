"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, Float, String
from xblock.fragment import Fragment


class SIRSimulatorXBlock(XBlock):
    """
    Allows students to select parameters for an SIR model and describe the
    resulting simulation.
    """

    # Learners are shown the max infected percent in each of their simulation
    # runs. This number is a common metric for how debilitating an epidemic is
    # so the student whose simulation produced the max_percent_infected would
    # have created the "worst" epidemic.
    max_percent_infected = Integer(
        help="The largest infected percentage in all learner simulations.",
        default=0, scope=Scope.user_state_summary
    )

    # SIR model parameters, can be chosen by learner
    population = Integer( # this is S, in the SIR model
        default=50, scope=Scope.user_state,
        help="The initial susceptible population.",
    )
    reproduction_num = Float( # this is R0, in the SIR model, https://en.wikipedia.org/wiki/Basic_reproduction_number
        default=1.4, scope=Scope.user_state,
        help="The basic reproduction number of the virus.",
    )

    # Description of simulation written by learner
    simulation_description = String(
        default='', scope=Scope.user_state,
        help="A description of this outbreak simulation.",
    )

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the SIRSimulatorXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/sir_simulator.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/sir_simulator.css"))
        frag.add_javascript(self.resource_string("static/js/src/sir_simulator.js"))
        frag.initialize_js('SIRSimulatorXBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def submit_description(self, data, suffix=''):
        """
        Save the learner's simulation parameters and description
        """
        # save population
        # save reproductive rate
        # save description
        
        # examine max_percent_infected (still need to calculate and return this)
        # if it's bigger than what we currently have, overwrite
        # either way, return final max_percent_infected so we can tell learner about it
        return {}

    # TODO: consult Product on intended behavior of multiple xblocks on a page.
    # then pay for all the technical decisions that assume only 1.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("SIRSimulatorXBlock",
             """<sir_simulator/>
             """),
            ("Multiple SIRSimulatorXBlock",
             """<vertical_demo>
                <sir_simulator/>
                <sir_simulator/>
                <sir_simulator/>
                </vertical_demo>
             """),
        ]
