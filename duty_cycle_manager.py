import RPi.GPIO as IO

import time
IO.setwarnings(False)

power = 0

# GPIO Pins
clk = 17
dt = 18

dt_val = 0
clk_val = 0
fq = 100

INCREMENT = 5


FLOW_MAX = 1090.0
FLOW_LOW = 450.0
ON = True
OFF = False

class DutyCycleManager():
    current_output = 0
    high = FLOW_MAX
    low = FLOW_LOW
    cycle_time = 30
    flowrate = 0
    pwm_object = None
    status = OFF

    def __init__(self, high=FLOW_MAX, low=FLOW_LOW):
        high = high
        low = low
        IO.setmode(IO.BCM)

        IO.setup(12,IO.OUT)
        self.pwm_object = IO.PWM(12,fq)
        self.pwm_object.start(0)


    def get_cycle(self):
        return self.current_output

    def set_cycle(self, app, value):
        app.logger.error(f"Setting cval to {self.calc_power(value)}")
        if value < self.low:
            value = self.low
        elif value > self.high:
            value = self.high
        self.current_output = self.calc_power(value)
        app.logger.error(f"CVAL is {self.current_output}")

    def calc_power(self, flowrate):
        if flowrate < self.low:
            flowrate = self.low
            self.calc_cycle_power(flowrate)
        elif flowrate > self.high:
            flowrate = self.high
            self.current_output = (4.76e-5 * pow(flowrate, 2)) + (3.85e-2 * flowrate) + 1.14

        return self.current_output


    def on_cycle(self):
        return self.flowrate / self.low * self.cycle_time

    def off_cycle(self):
        return (1 - self.flowrate / self.low) * self.cycle_time
    def calc_cycle_power(self, flowrate):
        self.status = ON
        print(f"Starting cycle for flowrate: {flowrate}")
        print(f"Cycle is {'ON' if self.status == ON else 'OFF'}")
        to_stop = self.on_cycle() if self.status else self.off_cycle()
        print(f"Waitinf for  {to_stop}")
        power = self.calc_power(self.low) if self.status else 0
        self.pwm_object.ChangeDutyCycle(self.current_output)
        print(f"Setting duty cycle to {self.calc_power(self.current_output)}")
        time.sleep(to_stop)
        self.status = not self.status


    def loop(self):
        try:
            dc = 0
            while True:
                val = float(input("Flow Rate: "))
                if val <= FLOW_LOW:
                    calc_cycle_power(val)

            dc = self.calc_power(val)
            print(dc)
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        except KeyboardInterrupt:
            pass

    def cleanup(self):
        p.ChangeDutyCycle(0)
        p.stop()
        IO.cleanup()
