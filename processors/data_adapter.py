class DataAdapter:
    """Used for exchanging data between different objects and windows."""

    def __init__(self):
        self._dict = {}

    def insert(self, _key, _value):
        self._dict[_key] = _value

    def get(self, _key):
        if _key not in self._dict:
            raise KeyError(f"{_key} not found")
        return self._dict[_key]

    def delete(self, _key):
        if _key not in self._dict:
            raise KeyError(f"{_key} not found")
        del self._dict[_key]

    def keys(self):
        return tuple(self._dict.keys())

    def values(self):
        return tuple(self._dict.values())

    def adapter_length(self):
        return len(self.keys())

    def ispresent(self, _key):
        return _key in self._dict

    def __str__(self) -> str:
        _str = "{\n"
        keys = self.keys()
        values = self.values()
        adapter_len = self.adapter_length()
        for i in range(adapter_len):
            _str += f"{keys[i]:<30}:\t{values[i]}, \n"
        _str += "}"
        return _str
