from enum import Enum


class Industry(str, Enum):
    Technology = 'Technology',
    Finance = 'Finance',
    Healthcare = 'Healthcare',
    Retail = 'Retail',
    Manufacturing = 'Manufacturing'
