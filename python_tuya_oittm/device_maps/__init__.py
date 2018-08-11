def create_reverse_device_map(device_map):
    reverse_device_map = {}
    for k, v in device_map.items():
        reverse_device_map[v] = k

    return reverse_device_map
