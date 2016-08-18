from mock import Mock

from xblock.runtime import Runtime
from xblock.test.tools import (
    assert_equals, assert_raises, assert_raises_regexp,
    assert_not_equals, assert_false,
    WarningTestMixin, TestRuntime,
)
from xblock.fields import Dict, Float, Integer, List, Set, Field, Scope, ScopeIds
from xblock.field_data import FieldData, DictFieldData


from workbench.runtime import WorkbenchRuntime
from xblock.fields import ScopeIds
from xblock.runtime import KvsFieldData, DictKeyValueStore
from sir_simulator.sir_simulator import SIRSimulatorXBlock

def make_block():
    """ Instantiate a DragAndDropBlock XBlock inside a WorkbenchRuntime """
    block_type = 'drag_and_drop_v2'
    key_store = DictKeyValueStore()
    field_data = KvsFieldData(key_store)
    runtime = WorkbenchRuntime()
    def_id = runtime.id_generator.create_definition(block_type)
    usage_id = runtime.id_generator.create_usage(def_id)
    scope_ids = ScopeIds('user', block_type, def_id, usage_id)
    return SIRSimulatorXBlock(runtime, field_data, scope_ids=scope_ids)

def test_default_values_of_model_parameters():
    test_xblock = make_block()

    assert_equals(test_xblock.population, 50)
    assert_equals(test_xblock.reproduction_num, 1.2)
    assert_equals(test_xblock.max_percent_infected, 0)
    # TODO: Figure out why this field isn't there.
    # Maybe because this is the String default?
    #assert_equals(test_xblock.simulation_description, '')

def test_instructor_editable_fields():
    test_xblock = make_block()

    expected_editable_fields = ('preamble', 'directions')
    assert_equals(test_xblock.editable_fields, expected_editable_fields)

    for field in expected_editable_fields:
        # field defaults should be more than some trivial length
        assert(len(getattr(test_xblock, field)) > 5)

        # field help text is required by StudioEditableXBlockMixin
        assert(len(test_xblock.fields[field].help) > 5)
