import sys
from typing import Sized

sys.path.append("../")
from chartify.layouts.insert_window import InsertWindow
from chartify.processors.data_adapter import DataAdapter
from chartify import config

if __name__ == "__main__":
    adapter = DataAdapter()
    app = InsertWindow(
        adapter,
        _key="text_box_value",
        title="Insert Window",
        size=(300, 200),
        _type="row",
    )
    app.start()
    print(adapter.get("text_box_value"))
