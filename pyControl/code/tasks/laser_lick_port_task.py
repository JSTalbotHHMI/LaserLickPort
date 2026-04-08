from pyControl.utility import *
from devices import Breakout_1_2, LaserLickPort


board = Breakout_1_2()
laser_lick_port = LaserLickPort(board.port_3)

states = ["monitor"]
events = ["poll", "sync_settings", "apply_settings"]
initial_state = "monitor"

opt_history = []
cap_history = []

v.custom_controls_dialog = "laser_lick_port_controls"
v.api_class = "LaserLickPort_API"

v.opt_threshold = 700
v.cap_threshold = 800
v.show_opt_channel = True
v.show_cap_channel = True
v.print_to_terminal = False
v.poll_interval_ms = 10
v.debug_uart = False
v.gui_plot_stride = 5
v.moving_average_points = 4

v.last_opt_raw = 0
v.last_cap_raw = 0
v.last_opt_lick = 0
v.last_cap_lick = 0
v.device_opt_threshold = 980
v.device_cap_threshold = 800


def run_start():
    global opt_history, cap_history
    opt_history = []
    cap_history = []
    laser_lick_port.clear()
    laser_lick_port.set_stream_mask(True, True)
    v.device_opt_threshold = v.opt_threshold
    v.device_cap_threshold = v.cap_threshold
    print_variables(
        ["opt_threshold", "cap_threshold", "device_opt_threshold", "device_cap_threshold", "moving_average_points"]
    )
    set_timer("poll", v.poll_interval_ms * ms, output_event=False)


def monitor(event):
    pass


def all_states(event):
    if event == "poll":
        poll_device()
        set_timer("poll", v.poll_interval_ms * ms, output_event=False)
    elif event == "sync_settings":
        v.device_opt_threshold = v.opt_threshold
        v.device_cap_threshold = v.cap_threshold
        print_variables(
            ["opt_threshold", "cap_threshold", "device_opt_threshold", "device_cap_threshold", "moving_average_points"]
        )
    elif event == "apply_settings":
        v.device_opt_threshold = v.opt_threshold
        v.device_cap_threshold = v.cap_threshold
        print_variables(
            [
                "opt_threshold",
                "cap_threshold",
                "device_opt_threshold",
                "device_cap_threshold",
                "moving_average_points",
                "show_opt_channel",
                "show_cap_channel",
                "print_to_terminal",
            ]
        )


def poll_device():
    global opt_history, cap_history
    latest_data = None

    while True:
        values = laser_lick_port.read_message()
        raw_line = laser_lick_port.get_last_raw_line()
        if v.debug_uart and raw_line:
            print("UART raw: " + raw_line)
            laser_lick_port.last_raw_line = None

        if values is None:
            break

        latest_data = values

    if latest_data is None:
        return

    avg_points = max(1, int(v.moving_average_points))
    if len(opt_history) > avg_points:
        opt_history = opt_history[-avg_points:]
    if len(cap_history) > avg_points:
        cap_history = cap_history[-avg_points:]

    if "optRaw" in latest_data:
        opt_history.append(latest_data["optRaw"])
        if len(opt_history) > avg_points:
            opt_history.pop(0)
        v.last_opt_raw = sum(opt_history) // len(opt_history)
    if "capRaw" in latest_data:
        cap_history.append(latest_data["capRaw"])
        if len(cap_history) > avg_points:
            cap_history.pop(0)
        v.last_cap_raw = sum(cap_history) // len(cap_history)
    v.last_opt_lick = int(v.last_opt_raw > v.opt_threshold)
    v.last_cap_lick = int(v.last_cap_raw > v.cap_threshold)
    print_variables(["last_opt_raw", "last_cap_raw", "last_opt_lick", "last_cap_lick"])

    if v.print_to_terminal:
        print(
            "LLP,optRaw="
            + str(v.last_opt_raw)
            + ",capRaw="
            + str(v.last_cap_raw)
            + ",optLick="
            + str(v.last_opt_lick)
            + ",capLick="
            + str(v.last_cap_lick)
        )
