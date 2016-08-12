"""This XBlock allows users to play with an epidemic model by changing parameters 
and asks them to submit the parameters for the worst epidemic they can generate."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, Float, String
from xblock.fragment import Fragment
from xblockutils.studio_editable import StudioEditableXBlockMixin

class SIRSimulatorXBlock(StudioEditableXBlockMixin, XBlock):
    """
    Allows students to select parameters for an SIR model and describe the
    resulting simulation.
    """

    ############################################################################
    # Fields
    ############################################################################

    display_name = 'SIR Simulation'
    editable_fields = ('preamble', 'directions')

    # Learner-generated fields
    ##########################

    # This number is a common metric for how debilitating an epidemic is
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
    reproduction_num = Float( # this is R0, in the SIR model
        default=1.2, scope=Scope.user_state,
        help="The basic reproduction number of the virus.",
    )

    # Description of simulation written by learner
    simulation_description = String(
        default='', scope=Scope.user_state,
        help="A description of this outbreak simulation.",
    )

    # Instructor-configurable fields
    ################################

    preamble = String(# TODO: broaden this to include equations. Possibly expose
        # more technical details to instructor in studio view only.

        help="An explanation of what the SIR model is and directions for "\
        "interacting with the simulation. We've included the limitations of "\
        "the model here, but you may add to or reword the description.",

        default="The SIR (Susceptible, Infected, Recovered) model is a "\
        "simple dynamic system used to simulate an epidemic. In this "\
        "simulation, a single person becomes infected with a virus. The "\
        "infection lasts for one time step of the model, during which they "\
        "may infect others in the population. Once infected and recovered, "\
        "an individual is immune. The plague lasts until it dies out or all "\
        "individuals in the population are immune. However, at any point in "\
        "the plague, if over 10% of the population is incapacitated by the "\
        "infection, basic civic infrastructure may begin to suffer.",

        scope=Scope.content,
        display_name='Activity preamble',
        multiline_editor=True
    )

    directions = String(

        help="An explanation of what the learner should describe in their "\
        "submission.",

        default='Pick the parameters which you think represent the "worst '\
        'case scenario". Then explain the features of the simulation which '\
        'you think justify this.', 

        scope=Scope.content,
        display_name='Directions',
        multiline_editor=True
    )

    ############################################################################
    # Views
    ############################################################################

    # studio_view inherited from StudioEditableXBlockMixin

    # Displays a form for entering simulation parameters and runs the simulation
    def student_view(self, context=None):
        """
        The primary view of the SIRSimulatorXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/sir_simulator.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/sir_simulator.css"))
        frag.add_javascript(self.resource_string(
            "static/js/src/sir_simulator.js"
        ))
        frag.add_javascript(self.resource_string(
            "static/js/lib/highcharts-custombar-4.2.6.min.js"
        ))
        frag.initialize_js('SIRSimulatorXBlock')
        return frag

    ############################################################################
    # Endpoints
    ############################################################################

    @XBlock.json_handler
    def simulation_description(self, data, suffix=''):
        """
        Save the learner's simulation parameters and description
        Check if the max infected percentage is a new record
        """
        response = {'status': 'ok'}
        new_record_message = "Congratulations! That's the worst outbreak "\
                             "in this class!"
        current_record_message = "The worst outbreak in the class so far had "\
            "a peak of %d%% infected! See if you can make your outbreak even "\
            "worse." % self.max_percent_infected

        self.population = data['population']
        self.reproduction_num = data['reproduction_num']
        self.description = data['simulation_description']

        # examine max_percent_infected
        # if it's bigger than what we currently have, overwrite
        if int(data['max_percent_infected']) > self.max_percent_infected:
            self.max_percent_infected = data['max_percent_infected']
            response['max_percent_message'] = new_record_message
        else:
            response['max_percent_message'] = current_record_message
        # either way, return message with final max_percent_infected so we
        # can tell learner about it
        return response

    ############################################################################
    # Helpers and bookkeeping
    ############################################################################

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TODO: consult Product on intended behavior of multiple xblocks on a page.
    # then pay for all the technical decisions that assume only 1.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("simulation",
             """<sir_simulator name='sir_simulator'/>
             """)
        ]
