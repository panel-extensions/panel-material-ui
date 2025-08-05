import logging

import param
import pytest

from panel_material_ui.base import MaterialComponent

logger = logging.getLogger(__name__)

NO_REFENCE_GUIDE_NEEDED = [
    "DatetimeInput",
    "DictInput",
    "ListInput",
    "NumberInput",
    "NotificationArea",
    "TupleInput",
    "Column",
    "Row",
    "Divider",
    "Alert"
]

## Find child classes of MaterialComponent
def find_child_classes(cls, skip_class: list[str]=NO_REFENCE_GUIDE_NEEDED):
    """
    Recursively find all child classes of MaterialComponent.
    """
    child_classes = []
    for subclass_name, subclass in param.concrete_descendents(cls).items():
        if not subclass_name.startswith('_') and not subclass_name in NO_REFENCE_GUIDE_NEEDED:
            child_classes.append(subclass)
    return child_classes

# find all reference guides in examples/reference_guides
def find_reference_guides():
    """
    Find all reference guides in examples/reference_guides.
    """
    import os
    import glob

    reference_guides = []
    for root, _, files in os.walk("examples/reference"):
        for file in files:
            if file.endswith(".ipynb") and not file.endswith("-checkpoint.ipynb"):
                reference_guides.append(os.path.join(root, file))

    return reference_guides

child_classes = find_child_classes(MaterialComponent)
reference_guides = find_reference_guides()

@pytest.mark.parametrize("child_class", child_classes)
def test_reference_guide_exists(child_class):
    """
    Test to ensure that each MaterialComponent subclass has a corresponding reference guide.
    """
    class_name = child_class.__name__
    module_name = child_class.__module__.split('.')[-1]

    # Check if the reference guide exists
    guide_exists = any(f"{class_name}.ipynb" in guide for guide in reference_guides)

    if not guide_exists:
        message = f"No reference guide found for {class_name} in {module_name}."
        raise AssertionError(message)
    else:
        logger.info(f"Reference guide found for {class_name} in {module_name}.")
