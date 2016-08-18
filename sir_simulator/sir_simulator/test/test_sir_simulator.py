# test assertion articulation tools
from xblock.test.tools import (
    assert_equals, assert_true,
    assert_not_equals, assert_false
)

# Code not under test that we will nonetheless exercise
from workbench.runtime import WorkbenchRuntime
from xblock.fields import ScopeIds
from xblock.runtime import KvsFieldData, DictKeyValueStore

# Code under test
from sir_simulator.sir_simulator import SIRSimulatorXBlock

def make_block():
    # TODO: figure out if there are applications where I can exercise the
    # class without a runtime, or if a little stubbing would get me there
    key_store = DictKeyValueStore()
    field_data = KvsFieldData(key_store)
    return SIRSimulatorXBlock(None, field_data, None)
    

def make_block_with_runtime():
    """ Instantiate a SIRSimulatorXBlock inside a WorkbenchRuntime """
    block_type = ''
    key_store = DictKeyValueStore()
    field_data = KvsFieldData(key_store)
    runtime = WorkbenchRuntime()
    def_id = runtime.id_generator.create_definition(block_type)
    usage_id = runtime.id_generator.create_usage(def_id)
    scope_ids = ScopeIds('user', block_type, def_id, usage_id)
    return SIRSimulatorXBlock(runtime, field_data, scope_ids=scope_ids)

def test_default_values_of_model_parameters():
    test_xblock = make_block_with_runtime()

    assert_equals(test_xblock.population, 50)
    assert_equals(test_xblock.reproduction_num, 1.2)
    assert_equals(test_xblock.max_percent_infected, 0)
    # TODO: Figure out why this field isn't there.
    # Maybe because this is the String default?
    #assert_equals(test_xblock.simulation_description, '')

def test_instructor_editable_fields():
    test_xblock = make_block_with_runtime()

    expected_editable_fields = ('preamble', 'directions')
    assert_equals(test_xblock.editable_fields, expected_editable_fields)

    for field in expected_editable_fields:
        # field defaults should be more than some trivial length
        assert(len(getattr(test_xblock, field)) > 5)

        # field help text is required by StudioEditableXBlockMixin
        assert(len(test_xblock.fields[field].help) > 5)
