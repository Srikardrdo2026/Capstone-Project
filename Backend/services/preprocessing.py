def extract_features(log):
    """
    Convert raw log data into behavioral features.
    Handles both JSON (HH:MM) and CSV (integer hour) inputs.
    """

    login_time = log.get("login_time", 0)

    if isinstance(login_time, str):
        try:
            login_hour = int(login_time.split(":")[0])
        except:
            login_hour = 0
    elif isinstance(login_time, (int, float)):
        login_hour = int(login_time)
    else:
        login_hour = 0

    session_duration = int(log.get("session_duration", 0))

    commands = log.get("commands", [])
    commands_count = len(commands)

    failed_logins = int(log.get("failed_logins", 0))

    protocol = log.get("protocol", "UNKNOWN")

    typing_speed = float(log.get("typing_speed", 0))

    return {
        "login_hour": login_hour,
        "session_duration": session_duration,
        "commands_count": commands_count,
        "failed_logins": failed_logins,
        "protocol": protocol,
        "typing_speed": typing_speed
    }
