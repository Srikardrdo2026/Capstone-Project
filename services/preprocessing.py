def extract_features(log):
    """
    Convert raw log data into behavioral features.
    """

    # 1. Login hour
    login_time = log.get("login_time", "00:00")
    login_hour = int(login_time.split(":")[0])

    # 2. Command count
    commands = log.get("commands", [])
    command_count = len(commands)

    # 3. Privileged command usage
    privileged_commands = {"sudo", "su", "chmod", "chown"}
    uses_privileged_cmd = int(any(cmd in privileged_commands for cmd in commands))

    # 4. Session duration
    session_duration = int(log.get("session_duration", 0))

    # 5. Protocol encoding
    protocol_map = {
        "SSH": 1,
        "HTTP": 2,
        "HTTPS": 3,
        "FTP": 4
    }
    protocol_encoded = protocol_map.get(log.get("protocol", "UNKNOWN"), 0)

    return {
        "login_hour": login_hour,
        "command_count": command_count,
        "uses_privileged_cmd": uses_privileged_cmd,
        "session_duration": session_duration,
        "protocol_encoded": protocol_encoded
    }
