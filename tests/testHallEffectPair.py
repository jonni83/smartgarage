from SmartGarage.smartgarage import HallEffectPair

class TestHallEffectPair:
    def setup(self):
        self.halleffectpair = HallEffectPair()

    def teardown(self):
        self.halleffectpair.cleanup()
