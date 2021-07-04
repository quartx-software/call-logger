# Third Party
import pytest

# Local
from calllogger.influx import Point


@pytest.fixture
def point():
    return Point("test_metric")


@pytest.mark.parametrize("precision,length", [
    (Point.NANOSECONDS, 19),
    (Point.MICROSECONDS, 16),
    (Point.MILLISECONDS, 13),
    (Point.SECONDS, 10),
])
def test_time(point, precision, length):
    assert point._time is None
    point.time(precision)
    assert isinstance(point._time, int)
    assert len(str(point._time)) == length


def test_time_invalid(point: Point):
    assert point._time is None
    with pytest.raises(ValueError):
        point.time("invalid")


def test_set_tag(point: Point):
    assert not point._tags
    point.tag("tag", "value")
    assert point._tags.get("tag") == "value"


def test_set_tags(point: Point):
    assert not point._tags
    point.tags(tag1="value1", tag2="value2")
    assert point._tags.get("tag1") == "value1"
    assert point._tags.get("tag2") == "value2"


def test_set_field(point: Point):
    assert not point._fields
    point.field("field", "value")
    assert point._fields.get("field") == "value"


def test_set_fields(point: Point):
    assert not point._fields
    point.fields(field1="value1", field2="value2")
    assert point._fields.get("field1") == "value1"
    assert point._fields.get("field2") == "value2"


def test_line_protocol(point: Point):
    point.tag("tag", "value")
    point.field("field", "value")
    line = point.to_line_protocol()
    assert line == 'test_metric,tag=value field="value"'


def test_line_protocol_no_field(point: Point):
    """That that a point with no field outputs an empty line."""
    point.tag("tag", "value")
    line = point.to_line_protocol()
    assert line == ''


def test_none_value(point: Point):
    """Test that tags & fields ignore value of type None."""
    point.tag("tag1", "value")
    point.tag("tag2", None)
    point.field("field1", "value")
    point.field("field2", None)
    line = point.to_line_protocol()
    assert line == 'test_metric,tag1=value field1="value"'


@pytest.mark.parametrize("value,expected_line", [
    (10.1, "test_metric field=10.1"),
    (10.0, "test_metric field=10"),
    (True, "test_metric field=true"),
    (False, "test_metric field=false"),
    (0, "test_metric field=0i"),
    (5, "test_metric field=5i"),
    ("value", 'test_metric field="value"'),
])
def test_field_value_types(point: Point, value, expected_line):
    point.field("field", value)
    line = point.to_line_protocol()
    assert line == expected_line


def test_invalid_field_type(point: Point):
    point.field("field", object())
    with pytest.raises(ValueError):
        point.to_line_protocol()
