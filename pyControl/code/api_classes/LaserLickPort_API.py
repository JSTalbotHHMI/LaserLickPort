from collections import deque
import json

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets

from source.gui.api import Api
from source.communication.pycboard import MsgType


class LaserLickPort_API(Api):
    def __init__(self):
        super().__init__()
        self.window = None
        self.max_points = 1000
        self.colors = {
            "optRaw": "#e74c3c",
            "capRaw": "#2980b9",
            "optLick": "#e74c3c",
            "capLick": "#2980b9",
        }
        self.threshold_colors = {
            "optRaw": "#8b2d20",
            "capRaw": "#17486a",
        }
        self.enabled = {
            "optRaw": True,
            "capRaw": True,
            "optLick": True,
            "capLick": True,
        }
        self.series = {}
        self.thresholds = {"optRaw": 0, "capRaw": 0}
        self.plot_stride = 5
        self._plot_counters = {"optRaw": 0, "capRaw": 0, "optLick": 0, "capLick": 0}

    def interface(self, board, print_to_log):
        super().interface(board, print_to_log)
        self.enabled["optRaw"] = bool(board.sm_info.variables.get("show_opt_channel", True))
        self.enabled["capRaw"] = bool(board.sm_info.variables.get("show_cap_channel", True))
        self.enabled["optLick"] = self.enabled["optRaw"]
        self.enabled["capLick"] = self.enabled["capRaw"]
        self.thresholds["optRaw"] = int(board.sm_info.variables.get("opt_threshold", 0))
        self.thresholds["capRaw"] = int(board.sm_info.variables.get("cap_threshold", 0))
        self.plot_stride = max(1, int(board.sm_info.variables.get("gui_plot_stride", 5)))

    def run_start(self):
        self._ensure_window()
        self._reset_data()
        self.window.threshold_lines["optRaw"].setValue(self.thresholds["optRaw"])
        self.window.threshold_lines["capRaw"].setValue(self.thresholds["capRaw"])
        self._plot_counters = {"optRaw": 0, "capRaw": 0, "optLick": 0, "capLick": 0}
        self.window.show()

    def run_stop(self):
        if self.window:
            self.window.close()
            self.window.deleteLater()
            self.window = None

    def process_data_user(self, data):
        for var_change in data["vars"]:
            if var_change.name == "show_opt_channel":
                self.enabled["optRaw"] = bool(var_change.value)
                self.enabled["optLick"] = self.enabled["optRaw"]
            elif var_change.name == "show_cap_channel":
                self.enabled["capRaw"] = bool(var_change.value)
                self.enabled["capLick"] = self.enabled["capRaw"]
            elif var_change.name == "opt_threshold":
                self.thresholds["optRaw"] = int(var_change.value)
            elif var_change.name == "cap_threshold":
                self.thresholds["capRaw"] = int(var_change.value)
            elif var_change.name == "gui_plot_stride":
                self.plot_stride = max(1, int(var_change.value))
            elif var_change.name == "last_opt_raw":
                self._append_plot_point("optRaw", var_change.time / 1000.0, int(var_change.value))
            elif var_change.name == "last_cap_raw":
                self._append_plot_point("capRaw", var_change.time / 1000.0, int(var_change.value))
            elif var_change.name == "last_opt_lick":
                self._append_plot_point("optLick", var_change.time / 1000.0, int(var_change.value))
            elif var_change.name == "last_cap_lick":
                self._append_plot_point("capLick", var_change.time / 1000.0, int(var_change.value))

    def process_data(self, new_data):
        data = {"states": [], "events": [], "prints": [], "vars": [], "analog": []}

        for nd in new_data:
            if nd.type == MsgType.PRINT:
                data["prints"].append(self.print_tup(nd.content, nd.time))
            elif nd.type == MsgType.VARBL:
                for name, value in json.loads(nd.content).items():
                    data["vars"].append(self.var_tup(name, value, nd.time))
            elif nd.type == MsgType.STATE:
                data["states"].append(self.state_tup(self.ID2name[nd.content], nd.time))
            elif nd.type == MsgType.EVENT:
                data["events"].append(self.event_tup(self.ID2name[nd.content], nd.time))
            elif nd.type == MsgType.ANLOG:
                data["analog"].append(self.analog_tup(self.ID2analog[nd.content[0]], nd.content[1], nd.time))

        self.process_data_user(data)

    def plot_update(self):
        if not self.window:
            return
        for key in ("optRaw", "capRaw"):
            self.window.raw_curves[key].setVisible(self.enabled[key])
            self.window.raw_curves[key].setData(self.series[key]["x"], self.series[key]["y"])
            self.window.threshold_lines[key].setValue(self.thresholds[key])
        for key in ("optLick", "capLick"):
            self.window.flag_curves[key].setVisible(self.enabled[key])
            self.window.flag_curves[key].setData(self.series[key]["x"], self.series[key]["y"])

    def _parse_sample(self, line, timestamp):
        sample = {"time": timestamp}
        for field in line.split(",")[1:]:
            if "=" not in field:
                continue
            name, value = field.split("=", 1)
            try:
                sample[name] = int(value)
            except ValueError:
                return None
        return sample

    def _reset_data(self):
        self.series = {
            "optRaw": {"x": deque(maxlen=self.max_points), "y": deque(maxlen=self.max_points)},
            "capRaw": {"x": deque(maxlen=self.max_points), "y": deque(maxlen=self.max_points)},
            "optLick": {"x": deque(maxlen=self.max_points), "y": deque(maxlen=self.max_points)},
            "capLick": {"x": deque(maxlen=self.max_points), "y": deque(maxlen=self.max_points)},
        }
        self._plot_counters = {"optRaw": 0, "capRaw": 0, "optLick": 0, "capLick": 0}

    def _append_plot_point(self, key, timestamp, value):
        self._plot_counters[key] += 1
        if (self._plot_counters[key] % self.plot_stride) != 0:
            return
        self.series[key]["x"].append(timestamp)
        self.series[key]["y"].append(value)

    def _ensure_window(self):
        if self.window:
            return
        self.window = _LaserLickPortWindow(self.colors, self.threshold_colors)
        self.window.setWindowTitle("LaserLickPort Live Data")


class _LaserLickPortWindow(QtWidgets.QWidget):
    def __init__(self, colors, threshold_colors):
        super().__init__()
        self.resize(900, 600)

        self.raw_plot = pg.PlotWidget(title="Raw Sensor Output")
        self.raw_plot.showGrid(x=True, y=True, alpha=0.3)
        self.raw_plot.setLabel("left", "Raw")
        self.raw_plot.setLabel("bottom", "Time (s)")
        self.raw_plot.addLegend()

        self.flag_plot = pg.PlotWidget(title="Licks")
        self.flag_plot.showGrid(x=True, y=True, alpha=0.3)
        self.flag_plot.setLabel("left", "Flag")
        self.flag_plot.setLabel("bottom", "Time (s)")
        self.flag_plot.setYRange(-0.1, 1.1)
        self.flag_plot.addLegend()
        self.flag_plot.setXLink(self.raw_plot)

        legend = QtWidgets.QLabel(
            '<span style="color:{0};">optRaw</span> | '
            '<span style="color:{1};">capRaw</span> | '
            '<span style="color:{2};">optLick</span> | '
            '<span style="color:{3};">capLick</span>'.format(
                colors["optRaw"], colors["capRaw"], colors["optLick"], colors["capLick"]
            )
        )
        legend.setTextFormat(QtCore.Qt.TextFormat.RichText)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(legend)
        layout.addWidget(self.raw_plot)
        layout.addWidget(self.flag_plot)

        self.raw_curves = {
            "optRaw": self.raw_plot.plot(name="optRaw", pen=pg.mkPen(colors["optRaw"], width=2)),
            "capRaw": self.raw_plot.plot(name="capRaw", pen=pg.mkPen(colors["capRaw"], width=2)),
        }
        self.threshold_lines = {
            "optRaw": pg.InfiniteLine(
                angle=0, movable=False, pen=pg.mkPen(threshold_colors["optRaw"], width=2, style=QtCore.Qt.PenStyle.DashLine)
            ),
            "capRaw": pg.InfiniteLine(
                angle=0, movable=False, pen=pg.mkPen(threshold_colors["capRaw"], width=2, style=QtCore.Qt.PenStyle.DashLine)
            ),
        }
        self.raw_plot.addItem(self.threshold_lines["optRaw"])
        self.raw_plot.addItem(self.threshold_lines["capRaw"])
        self.flag_curves = {
            "optLick": self.flag_plot.plot(name="optLick", pen=pg.mkPen(colors["optLick"], width=2)),
            "capLick": self.flag_plot.plot(name="capLick", pen=pg.mkPen(colors["capLick"], width=2)),
        }
