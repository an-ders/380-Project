
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

    def forward(self, speed=1.0):
        return

    def backward(self, speed=1.0):
        return

    def stop(self):
        return


class TestServo:
    def __init__(self, pin):
        self.value = pin

    def min(self):
        return

    def max(self):
        return
