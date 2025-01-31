from src.controller.visa_53131A import Visa53131A


class model53131A:
    def __init__(self, port):
        self.port = port
        self.driver = Visa53131A(self.port)
        self.driver.initialize()
        self.driver.idn()


    def conf_freq(self):
        self.driver.CONFigure_FREQ()

    def read_freq(self):
        return self.driver.READ()

    def meas_time(self, time):
        self.driver.ACQuisition_APERture(time)

    def meas_time_query(self):
        return self.driver.ACQuisition_APERture_query()

    def normalise_freq(self, freq):
        return (freq - 10E6) / 10E6

    def finalize(self):
        self.driver.finalize()

    def __str__(self):
        return f"Model53131A, visa: {self.driver.serial_number}, on port: {self.port}"


if __name__ == "__main__":
    model_53131A = model53131A("USB0::0x0699::0x3003::599442::INSTR")
    print(model_53131A)

    model_53131A.conf_freq()
    model_53131A.meas_time(1)

    print(model_53131A.meas_time_query())

    freq = float(model_53131A.read_freq())
    print(f'Measured freq: {freq}')
    print(f'Normalised freq: {model_53131A.normalise_freq(freq)}')

    print(model_53131A.meas_time_query())
    model_53131A.finalize()

