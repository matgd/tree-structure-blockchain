import csv
import time


class MeasureTime:
    clear_file = True
    operations_counter = {}

    def __init__(self, operation: str, file_path: str = 'exec_time.csv'):
        self.file = open(file_path, mode='a', encoding='utf-8')
        if MeasureTime.clear_file:
            self.file.truncate(0)
            MeasureTime.clear_file = False
        self.writer = csv.writer(self.file)
        self.operation = operation

    def __enter__(self):
        self.start = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.perf_counter()
        self.writer.writerow([
            self.operation,
            MeasureTime.operations_counter.setdefault(self.operation, 1),
            '{0:.7f}'.format(self.end - self.start)
        ])
        MeasureTime.operations_counter[self.operation] += 1

    def __del__(self):
        self.file.close()
