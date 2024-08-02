SamplingTime = 1 

class PID:
    def __init__(self):
        self.setpoint = 0.80
        self.kp = -3.81
        self.ki = 4.47
        self.kd= 1.04
        self.sumerr=0
        self.preverr = 0
        self.derr=0

    def calculate_control_input(self, measured_value):
        error = self.setpoint - measured_value
        self.sumerr += SamplingTime * error
        self.derr = (error - self.preverr) / SamplingTime
        self.preverr = error
        u = self.kp * error+ self.sumerr*self.ki + self.kd*self.derr
       
        if u < 1:
            return 0

        return u


#print(controller(0.6))
