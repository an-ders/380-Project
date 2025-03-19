
class TestDevice:
    def __init__(self, pin):
        self.value = pin

    def on(self):
        return

    def off(self):
        return


class TestEncoder:
    def __init__(self, pin, temp):
        self.value = pin
        self.steps = 0


class TestMotor:
    def __init__(self, pin, temp):
        self.value = pin
        self.steps = temp
    
    def forward(self):
        return
    
    def backward(self):
        return
    
    def stop(self):
        return
