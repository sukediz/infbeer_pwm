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
OFf = False

class DutyCycleManager():
    current_output = 0
    high = FLOW_MAX
    low = FLOW_LOW
    cycle_time = 30
    flowrate = 0
    pwm_object = None

    def __init__(self, high=FLOW_MAX, low=FLOW_LOW):
        high = high
        low = low
        IO.setmode(IO.BCM)

        IO.setup(12,IO.OUT)
        self.pwm_object = IO.PWM(12,fq)
        self.pwm_object.start(0)


    def get_cycle(self):
        return self.current_output

    def set_cycle(self, value):
        if value < self.low:
            value = self.low
        elif value > self.high:
            value = self.high
            self.current_output = value

    def calc_power(self, flowrate):
        if flowrate < self.low:
            flowrate = self.low
            if flowrate > self.high:
                flowrate = self.high

        self.duty_cycle = (4.76e-5 * pow(flowrate, 2)) + (3.85e-2 * flowrate) + 1.14
        return self.duty_cycle

    def calc_cycle_power(self, flowrate):
        self.status = ON
        print(f"Starting cycle for flowrate: {flowrate}")

        def on_cycle(self):
            return self.flowrate / self.low * self.cycle_time

        def off_cycle(self):
            return (1 - self.flowrate / self.low) * self.cycle_time
        print(f"Cycle is {on}")
        to_stop = on_cycle() if on else off_cycle()
        print(f"Waitinf for  {to_stop}")
        pwm_object.ChangeDutyCycle(calc_power(FLOW_LOW) if on else 0)
        print(f"Setting duty cycle to {calc_power(FLOW_LOW)}")
        time.sleep(to_stop)
        on = not on


    def loop(self):
        try:
            dc = 0
            while True:
                val = float(input("Flow Rate: "))
                if val <= FLOW_LOW:
                    calc_cycle_power(p, val)

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
