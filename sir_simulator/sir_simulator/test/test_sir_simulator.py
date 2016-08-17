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

def test_default_values_of_fields():
    test_xblock = make_block()
        
    assert_equals(test_xblock.population, 50)
