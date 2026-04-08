from pyqtgraph.Qt import QtCore, QtWidgets


class Custom_controls_dialog(QtWidgets.QDialog):
    def __init__(self, parent_tab, board):
        super(QtWidgets.QDialog, self).__init__(parent_tab)
        self.board = board
        self.setWindowTitle("LaserLickPort Controls")
        self.setModal(False)

        self.opt_threshold = QtWidgets.QSpinBox()
        self.opt_threshold.setRange(0, 1023)

        self.cap_threshold = QtWidgets.QSpinBox()
        self.cap_threshold.setRange(0, 4095)

        self.moving_average_points = QtWidgets.QSpinBox()
        self.moving_average_points.setRange(1, 200)

        self.enable_opt_channel = QtWidgets.QCheckBox("Show optical channel")
        self.enable_cap_channel = QtWidgets.QCheckBox("Show capacitive channel")
        self.refresh_button = QtWidgets.QPushButton("Refresh")
        self.apply_button = QtWidgets.QPushButton("Apply")
        self.close_button = QtWidgets.QPushButton("Close")

        form = QtWidgets.QFormLayout()
        form.addRow("Opt threshold", self.opt_threshold)
        form.addRow("Cap threshold", self.cap_threshold)
        form.addRow("Average points", self.moving_average_points)
        form.addRow("", self.enable_opt_channel)
        form.addRow("", self.enable_cap_channel)

        buttons = QtWidgets.QHBoxLayout()
        buttons.addWidget(self.refresh_button)
        buttons.addWidget(self.apply_button)
        buttons.addWidget(self.close_button)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(form)
        layout.addLayout(buttons)

        self.refresh_button.clicked.connect(self.refresh)
        self.apply_button.clicked.connect(self.apply)
        self.close_button.clicked.connect(self.close)

        self.refresh()

    def exec(self):
        self.show()
        self.raise_()
        self.activateWindow()
        return 0

    def refresh(self):
        if self.board.framework_running:
            self.board.trigger_event("sync_settings")
            QtCore.QTimer.singleShot(250, self._load_from_board_cache)
            return
        self._load_from_board_cache()

    def _load_from_board_cache(self):
        self.opt_threshold.setValue(int(self._get_value("opt_threshold")))
        self.cap_threshold.setValue(int(self._get_value("cap_threshold")))
        self.moving_average_points.setValue(int(self._get_value("moving_average_points")))
        self.enable_opt_channel.setChecked(bool(self._get_value("show_opt_channel")))
        self.enable_cap_channel.setChecked(bool(self._get_value("show_cap_channel")))

    def _get_value(self, name):
        if self.board.framework_running:
            return self.board.sm_info.variables[name]
        return self.board.get_variable(name)

    def apply(self):
        self.board.set_variable("opt_threshold", int(self.opt_threshold.value()))
        self.board.set_variable("cap_threshold", int(self.cap_threshold.value()))
        self.board.set_variable("moving_average_points", int(self.moving_average_points.value()))
        self.board.set_variable("show_opt_channel", self.enable_opt_channel.isChecked())
        self.board.set_variable("show_cap_channel", self.enable_cap_channel.isChecked())
        if self.board.framework_running:
            QtCore.QTimer.singleShot(200, lambda: self.board.trigger_event("apply_settings"))
            QtCore.QTimer.singleShot(350, self._load_from_board_cache)
        else:
            self.board.set_variable("device_opt_threshold", int(self.opt_threshold.value()))
            self.board.set_variable("device_cap_threshold", int(self.cap_threshold.value()))
            self._load_from_board_cache()
