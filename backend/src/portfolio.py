#! python3


def has_sufficient_coins(records, selling):
    owned = 0
    for record in records:
        if record['type'] == 'purchase':
            owned += record['quantity']
        else:
            owned -= record['quantity']
    return owned >= selling
