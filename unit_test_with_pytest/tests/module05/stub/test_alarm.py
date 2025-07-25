from unittest.mock import Mock

from src.module05.stub.alarm import Alarm
from src.module05.stub.sensor import Sensor


def test_alarm_isOff_by_default():
    alarm = Alarm()
    assert not alarm.is_alarm_on


class StubSensor:
    def sample_pressure(self):
        return 17.0


def test_alarm_is_on_at_lower_threshold():
    alarm = Alarm(StubSensor())
    alarm.check()
    assert alarm.is_alarm_on

def test_alarm_is_on_at_higher_threshold():
    stub = Mock(Sensor)
    stub.sample_pressure.return_value = 21.0
    alarm = Alarm(stub)
    alarm.check()
    assert alarm.is_alarm_on
