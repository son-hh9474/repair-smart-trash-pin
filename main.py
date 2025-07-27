from smart_trash_bin import SmartTrashBin

if __name__ == "__main__":
    trash_bin = SmartTrashBin(trigger_distance=2.0, hold_time=5)

    trash_bin.run()
