import hashlib
import os


class SpeedFormat(object):

    @staticmethod
    def format(speed):
        unit_index = 0
        while speed > 1024:
            unit_index += 1
            speed = speed * 1.0 / 1024

        if unit_index == 0:
            unit = "B/s"
        elif unit_index == 1:
            unit = "KB/s"
        elif unit_index == 2:
            unit = "MB/s"
        elif unit_index == 3:
            unit = "GB/s"
        elif unit_index == 4:
            unit = "TB/s"
        else:
            unit = "PB"
        return "%s %s" % (speed, unit)


class Sha1Manager(object):

    @staticmethod
    def get_file_sha1(file_path, block_size=2 ** 20):
        if not os.path.exists(file_path):
            return None

        sha1obj = hashlib.sha1()
        with open(file_path, 'rb') as file_to_check:
            while True:
                data = file_to_check.read(block_size)
                if not data:
                    break
                sha1obj.update(data)
            return sha1obj.hexdigest()
