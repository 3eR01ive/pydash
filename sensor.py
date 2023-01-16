class Sensor:
    def __init__(self, name, channel, voltages, values):

        assert len(voltages) >= 2
        assert len(values) >= 2
        assert len(voltages) == len(values)

        self.__name = name
        self.__channel = channel
        self.__voltages = voltages
        self.__values = values
        self.__current_voltage = 0

    def set_voltage(self, voltage):
        self.__current_voltage = voltage

    def get_value(self):
        return self.__convert_voltage_to_value(self.__current_voltage)

    def __linear_interpolate(self, value, _from, _to):
        assert _from < _to
        assert 0 <= _from <= len(self.__voltages)
        assert 0 <= _to <= len(self.__voltages)

        voltage_from = self.__voltages[_from]
        voltage_to = self.__voltages[_to]

        assert value >= voltage_from
        assert value <= voltage_to
        assert voltage_to - voltage_from > 0

        multiplier = (value - voltage_from) / (voltage_to - voltage_from)

        value_from = self.__values[_from]
        value_to = self.__values[_to]

        interpolated_value = value_from + ((value_to - value_from) * multiplier)

        return interpolated_value

    def __convert_voltage_to_value(self, voltage_value):
        _from = 0
        _to = len(self.__voltages) - 1

        for i, voltage in enumerate(self.__voltages):
            if voltage_value >= voltage:
                _from = i
                break

        for i, voltage in reversed(list(enumerate(self.__voltages))):
            if voltage_value <= voltage:
                _to = i
                break

        return self.__linear_interpolate(voltage_value, _from, _to)
