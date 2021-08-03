from datetime import datetime


from tabulate import tabulate


class Metrics:
    def __init__(self):
        self.coverage_before_annotation = dict()
        self.coverage_after_annotation = dict()
        self.max_spectra = 0
        self.finished = 0

        self.time_100_back = None
        self.time_100_now = datetime.now()
        self.eta = 0

    def update_progress(self):
        self.finished += 1
        if self.finished % 100 == 0:
            self.time_100_back = self.time_100_now
            self.time_100_now = datetime.now()
            diff = (self.time_100_now - self.time_100_back).total_seconds()
            self.eta = int(((self.max_spectra - self.finished)/100)*diff/60)
        print(f'Progress {self.finished}/{self.max_spectra}, {(self.finished/self.max_spectra)*100:.2f}%, '
              f'ETA {self.eta}m', end='\r')

    def set_params(self, target_attributes, length):
        """
        Set all parameters needed to compute metrics.

        :param target_attributes: target attributes to be obtained during annotation
        :param length: number of spectra data
        """
        self.coverage_before_annotation = {key: 0 for key in target_attributes}
        self.coverage_after_annotation = {key: 0 for key in target_attributes}
        self.max_spectra = length

    def update_before_annotation(self, metadata_keys):
        """
        Increase counts of already present attributes.

        :param metadata_keys: present attributes
        """
        for key in self.coverage_before_annotation:
            if key in metadata_keys:
                self.coverage_before_annotation[key] += 1

    def update_after_annotation(self, metadata_keys):
        """
        Increase counts of annotated attributes

        :param metadata_keys: discovered attributes
        """
        for key in self.coverage_after_annotation:
            if key in metadata_keys:
                self.coverage_after_annotation[key] += 1

    def __str__(self):
        table = tabulate([[key,
                           f'{(self.coverage_before_annotation[key]/self.max_spectra)*100:.2f}%',
                           f'{(self.coverage_after_annotation[key]/self.max_spectra)*100:.2f}%']
                          for key in self.coverage_before_annotation],
                         headers=['Target\nattribute', 'Coverage\nbefore', 'Coverage\nafter'])

        return f'Attribute discovery rates:\n\n{table}\n' + '='*50 + '\n'
