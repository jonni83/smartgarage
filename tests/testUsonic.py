from SmartGarage.smartgarage import USonic

class TestUSonic:
    def setup(self):
        self.usonic = USonic(TRIGGER=10, ECHO=9)

    def teardown(self):
        self.usonic.cleanup()

    def test_get_distance(self):
        self.usonic.get_distance()
