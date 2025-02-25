class EnergyRecord:
    def __init__(self, engine: str, regex_complexity: str, run: int, time: float, energy: float):
        """
        Stores energy consumption data for a given regex engine and regex complexity.

        :param engine: Name of the regex engine/library used.
        :param regex_complexity: Description or level of regex complexity.
        :param run: Iteration of experiment.
        :param time: Time in seconds (s) of the measurement.
        :param energy: Measured energy consumption in Joules (J)
        """
        self.engine = engine
        self.regex_complexity = regex_complexity
        self.run = run
        self.time = time
        self.energy = energy