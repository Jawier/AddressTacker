import os
import sys
from datetime import datetime
import pandas as pd
import requests


# Get current UTXO balance of an address.
def get_utxo_balance(address):
    url = f"https://ocean.defichain.com/v0/mainnet/address/{address}/balance"
    r = requests.get(url)
    return float(r.json()['data'])


# List all tokens balance belonging to an address.
def get_all_tokens_balance(address):
    url = f"https://ocean.defichain.com/v0/mainnet/address/{address}/tokens"
    r = requests.get(url).json()
    balance = {}
    for token in r['data']:
        balance[token['displaySymbol']] = token['amount']

    return balance


# List all vaults belonging to an address [Loans].
def get_loan_info(address):
    url = f"https://ocean.defichain.com/v0/mainnet/address/{address}/vaults"
    r = requests.get(url).json()
    return {'collateral_amount_DFI': r['data'][0]['collateralAmounts'][0]['amount'],
            'collateral_value_USD': r['data'][0]['collateralValue'],
            'loan_dUSD': r['data'][0]['loanAmounts'][0]['amount'],
            'loan_dARKK': r['data'][0]['loanAmounts'][1]['amount'],
            'loan_value_USD': r['data'][0]['loanValue'],
            'informativeRatio': r['data'][0]['informativeRatio'],
            'UTC': datetime.now().replace(microsecond=0).isoformat(' ')}


def save_into_csv_file(filepath, dataframe):
    # if file does not exist write header
    if not os.path.isfile(filepath):
        dataframe.to_csv(filepath, index=False, header=True)
    else:  # else it exists so append without writing the header
        dataframe.to_csv(filepath, mode='a', index=False, header=False)


def generate_summary(_utxo, _tokens_balance, _loan_details):
    df1 = pd.DataFrame([{'UTXO': _utxo}])
    df2 = pd.DataFrame([_tokens_balance])
    df3 = pd.DataFrame([_loan_details])

    return pd.concat([df1, df2, df3], axis=1)


if __name__ == '__main__':
    my_address = sys.argv[1]
    utxo = get_utxo_balance(my_address)
    tokens_balance = get_all_tokens_balance(my_address)
    loan_details = get_loan_info(my_address)
    summary = generate_summary(utxo, tokens_balance, loan_details)
    addressInfoFilePath = f"./address_{my_address}.csv"
    save_into_csv_file(addressInfoFilePath, summary)
