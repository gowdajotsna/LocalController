prev_error=0
integral_error=0
SamplingInterval=1
def pid_controller(error, integral_error, prev_error, Kp, Ki, Kd, dt):
    integral = integral_error + error * dt
    derivative = (error - prev_error) / dt
    adjust = Kp * error + Ki * integral + Kd * derivative
    return adjust, integral

def controller(avg_cpu_usage):
   kp=-3
   ki=4
   kd=1.2
   global integral_error
   global prev_error
   reference_point=0.8
   error= reference_point-avg_cpu_usage
   u,integral_error=pid_controller(error, integral_error, prev_error,kp, ki, kd, SamplingInterval)
   prev_error=error
   print(u)
   if(u<1):
       return 0
   return u



#print(controller(0.6))
