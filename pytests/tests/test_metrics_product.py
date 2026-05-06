from pathlib import Path

from tenrek.parser import CppParser
from tenrek.metrics.for_classes import god_class


SAMPLES = Path(__file__).parent / "cpp_samples"


def test_god_class_returns_single_integer_for_one_class():
    parser = CppParser(str(SAMPLES / "god_class.cpp"))
    parser.parse()

    classes = parser.get_classes()

    assert len(classes) == 1
    assert god_class.calculate(classes[0]) == 8  # 3 fields + 5 methods
    assert isinstance(god_class.calculate(classes[0]), int)
