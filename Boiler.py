__author__ = 'John.Edenfield'


def radiation_loss(QN,m_fuel):
    Crad =0.211

    return Crad * QN**0.7 *10E6 * 0.0009486 * 3600/m_fuel