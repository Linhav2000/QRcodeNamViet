from CommonAssit import CommonAssit

header = "@"
fixed_for_light = "00"
end_cmd = "\r\n"
turn_off = "L0"
turn_on = "L1"
change_value = "F"
change_mode = "S"

def turn_off_cmd(channel=None):
    cmd = ""
    if channel == 1:
        cmd = header + "00" + turn_off
    elif channel == 2:
        cmd = header + "01" + turn_off
    elif channel == 3:
        cmd = header + "02" + turn_off
    else:
        cmd = header + "FF" + turn_off
    cmd += fixed_for_light
    cmd = cmd + CommonAssit.check_sum(cmd) + end_cmd
    return cmd

def turn_on_cmd(channel=None):
    cmd = ""
    if channel == 1:
        cmd = header + "00" + turn_on
    elif channel == 2:
        cmd = header + "01" + turn_on
    elif channel == 3:
        cmd = header + "02" + turn_on
    else:
        cmd = header + "FF" + turn_on
    cmd += fixed_for_light
    cmd = cmd + CommonAssit.check_sum(cmd) + end_cmd
    return cmd

def change_value_cmd(value=100, channel=None):
    str_value = str(value)
    if len(str_value)==1:
        str_value = "00" + str_value
    elif len(str_value)==2:
        str_value = "0" + str_value

    if channel == 1:
        cmd = header + "00" + change_value + str_value + fixed_for_light
    elif channel == 2:
        cmd = header + "01" + change_value + str_value + fixed_for_light
    elif channel == 3:
        cmd = header + "02" + change_value + str_value + fixed_for_light
    else:
        cmd = header + "FF" + change_value + str_value + fixed_for_light
    cmd = cmd + CommonAssit.check_sum(cmd) + end_cmd
    return cmd

def change_mode_cmd(mode="01", channel=None):
    if channel == 1:
        cmd = header + "00" + change_mode + mode + fixed_for_light
    elif channel == 2:
        cmd = header + "01" + change_mode + mode + fixed_for_light
    elif channel == 3:
        cmd = header + "02" + change_mode + mode + fixed_for_light
    else:
        cmd = header + "FF" + change_mode + mode + fixed_for_light
    cmd = cmd + CommonAssit.check_sum(cmd) + end_cmd
    return cmd