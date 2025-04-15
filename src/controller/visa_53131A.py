# from asyncio import timeout
from time import sleep
import pyvisa


class Visa53131A:
    def __init__(self, port):
        self.port = port
        self.resource_manager = None
        self.dev = None
        self.serial_number = ''
        self.channel = '1'


    def initialize(self):
        rm = pyvisa.ResourceManager()
        self.dev = rm.open_resource(self.port)
        sleep(.5)


    def finalize(self):
        self.dev.close()


    def query(self, message):
        if self.dev is None:
            raise Exception('You must first initialize the device with initialize()')

        message = message + "\n"
        message = message.encode()
        self.dev.write(message)
        # sleep(0.1) # be polite to all the data be sent back
        return self.dev.read().decode('ascii').strip()


    def idn(self):
        self.serial_number = self.dev.query("*IDN?")

    def rst(self):
        message = f'*RST'
        self.dev.write(message)


    def MEASure_FREQuency(self):
        message = f'MEAS:FREQ? (@{self.channel})'
        print(message)
        return self.dev.query(message)


    def ARM_STAR_SOUR(self):
        message = f'FREQ:ARM:STAR:SOUR IMM'
        self.dev.write(message)


    def ARM_STOP_SOUR(self):
        message = f'FREQ:ARM:STOP:SOUR TIM'
        self.dev.write(message)


    def ARM_STOP_TIM(self, time):
        message = f'FREQ:ARM:STOP:TIM {time}'
        self.dev.write(message)

    def ARM_STOP_TIM_query(self):
        message = f'FREQ:ARM:STOP:TIM?'
        return self.dev.query(message)


    def CONFigure_FREQ(self):
        message = f'CONF:FREQ (@{self.channel})'
        self.dev.write(message)

    def CONFigure_FREQ_query(self):
        message = f'CONF?'
        return self.dev.query(message)

    def INITiate(self):
        message = f'INITiate'
        self.dev.write(message)

    def READ(self):
        message = f'READ:FREQ?'
        try:
            response = self.dev.query(message)
        except Exception:
            print("Error: No valid frequency data. Is the input connected?")
            response = 0

        return response

    def FORMat_TINFormation(self, state):
        message =  f'FORM:TINF {state}'
        self.dev.write(message)

    def SYSTem_ERRor_query(self):
        message =  f'SYSTem:ERRor?'
        return self.dev.query(message)

    def DISplay_ENABle(self, state):
        message =  f'DIS:ENAB {state}'
        self.dev.write(message)





if __name__ == "__main__":
    dev = Visa53131A("GPIB0::2::INSTR") # need to change address here accordingly

    dev.initialize()
    dev.idn()
    print(dev.serial_number)
    dev.rst()

    dev.DISplay_ENABle('OFF')

    dev.CONFigure_FREQ()
    dev.ARM_STAR_SOUR()
    dev.ARM_STOP_SOUR()
    dev.ARM_STOP_TIM(1)
    dev.ARM_STOP_TIM_query()

    for i in range(5):
        freq = dev.READ()
        print(freq)
        print(dev.ARM_STOP_TIM_query())
        # print(f'{float(freq):.13}')

    dev.finalize()
