from SmartGarage.smartgarage import Relay

class TestRelay:
    def setup(self):
        self.relay = Relay()

    def teardown(self):
        self.relay.cleanup()

    def test_red(self):
        self.relay.turn_on_only(self.relay.red)

    def test_yellow(self):
        self.relay.turn_on_only(self.relay.yellow)
    
    def test_green(self):
        self.relay.turn_on_only(self.relay.green)
