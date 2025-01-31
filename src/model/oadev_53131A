import datetime
import time
from pathlib import Path
from threading import Thread
import threading
import numpy as np
import yaml
from time import perf_counter
from time import sleep


from src.model.model_53131A import model53131A
# from src.model.dummy_53131A import Dummy53131A


class Experiment:
    def __init__(self):
        self.config = {}
        self.counter = None

        self.times = np.zeros((1,))
        self.measured_freqs = np.zeros((1,))


    def load_config(self, filename):
        with open(filename, 'r') as f:
            self.config = yaml.load(f, yaml.FullLoader)

    def load_counter(self):
        if self.config['53131A']['model'] == "Real":
            self.counter = model53131A(self.config['53131A']['port'])
        # elif self.config['53131A']['model'] == "Dummy":
        #     self.counter = Dummy53131A(self.config['53131A']['port'])
        else:
            raise Exception("Device Not supported")


    def measurement_shot(self):

        self.times = np.zeros((1,))
        self.measured_freqs = np.zeros((1,))

        t0 = time.time()
        t0_save = time.time()
        while (self.config['Counter_Measurement']['meas_duration'] > self.times[-1] ):

            timestamp = time.time()
            self.freq_last_value = float(self.counter.read_freq())

            self.measured_freqs = np.append(self.measured_freqs, float(self.freq_last_value))
            self.times = np.append(self.times, float(timestamp - t0))


            if ((timestamp - t0_save) > 600):
                # print('Save')
                self.save_data(exp.config['Counter_Measurement']['filename'])
                t0_save = time.time()

        time.sleep(0.5)
        print(self.times)
        print(self.measured_freqs)


    def save_data(self, filename):
        folder_date = f'{datetime.date.today()}'
        base_folder = Path(self.config['Counter_Measurement']['folder'])

        save_dir = base_folder / folder_date

        save_dir.mkdir(parents=True, exist_ok=True)

        filename = Path(filename)
        i = 1
        new_filename = f'{filename.stem}_{i}{filename.suffix}'
        print(new_filename)
        full_path = save_dir / new_filename
        # while full_path.exists():
        #     i += 1
        #     new_filename = f'{filename.stem}_{i}{filename.suffix}'
        #     full_path = save_dir / new_filename

        data = np.vstack((self.times[1:], self.measured_freqs[1:]))
        data = np.transpose(data)
        np.savetxt(full_path, data, delimiter=',')

        metadata_filename = Path(self.config['Counter_Measurement']['metadata_filename'])
        metadata_filename = f'{metadata_filename.stem}_{i}{metadata_filename.suffix}'
        self.save_metadata(save_dir/metadata_filename)

    def save_metadata(self, file_path):
        with open(file_path, 'w') as f:
            yaml.dump(self.config, f)


    def finalize(self):
        self.counter.finalize()


if __name__ == "__main__":
    exp = Experiment()
    exp.load_config('../config.yml')
    print(exp.config)
    print('')

    exp.load_counter()
    print(exp.counter)
    print("")

    exp.counter.conf_freq()
    exp.counter.meas_time(1)
    # print(exp.counter.read_freq())

    exp.measurement_shot()
    # exp.save_data(exp.config['Counter_Measurement']['filename'])


    exp.finalize()
