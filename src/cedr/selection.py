

class Selector():
    def __init__(self, cfg) -> None:
        self.cfg = cfg
        self.methods = {
            "truncation": self.truncation
        }

    def truncation(self, individuals):
        n_breeders = int(len(individuals)*self.cfg["survival_rate"])

        # We always want an even number of breeding individuals
        if n_breeders % 2 != 0:
            n_breeders += 1

        return individuals[:n_breeders]
