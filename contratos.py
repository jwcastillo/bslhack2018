from boa.builtins import concat
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Runtime import CheckWitness, Notify
from boa.interop.Neo.Storage import *

TOKEN_NAME = 'TOC COIN'

TOKEN_SYMBOL = 'TOCC'

TOKEN_DECIMALS = 8

# This is the script hash of the address for the owner of the token
# This can be found in ``neo-python`` with the wallet open, use ``wallet`` command


TOKEN_CIRC_KEY = b'in_circulation'

# 10m total supply * 10^8 ( decimals)
TOKEN_TOTAL_SUPPLY = 10000000 * 100000000

TOKEN_INITIAL_AMOUNT = 2500000 * 100000000  # 2.5m to owners * 10^8

# for now assume 1 dollar per token, and one neo = 40 dollars * 10^8
TOKENS_PER_NEO = 40 * 100000000

# for now assume 1 dollar per token, and one gas = 20 dollars * 10^8
TOKENS_PER_GAS = 20 * 100000000

# maximum amount you can mint in the limited round ( 500 neo/person * 40 Tokens/NEO * 10^8 )
MAX_EXCHANGE_LIMITED_ROUND = 500 * 40 * 100000000

# when to start the crowdsale
BLOCK_SALE_START = 755000

# when to end the initial limited round
LIMITED_ROUND_END = 755000 + 10000

KYC_KEY = b'kyc_ok'

LIMITED_ROUND_KEY = b'r1'

CLAUSULAS = ['clausula 1', 'clausula 2']
GARANTIA = 5000
GANANCIAGARANTIA = 500
MONTOARRIENDO = 2500
MULTA = 100

RANKARRENDADOR = 100
RANKARRENDATARIO = 100
FEED = 0.01


def Main(operation, args):
    nargs = len(args)

    if nargs == 0:
        print("Sin direccion de arrendatario")
        return 0

    if operation == 'consulta':
        arrendatario_wallet_address = args[0]
        return ConsultaArrendatario(arrendatario_wallet_address)

    elif operation == 'registrar':
        if nargs < 2:
            print(
                "parametros requeridos: [arrendatario_wallet_address] [arrendador_wallet_address]")
            return 0
        arrendatario_wallet_address = args[0]
        arrendador_wallet_address = args[1]
        return RegistrarArrendatario(arrendatario_wallet_address, arrendador_wallet_address)

    else:
        return 'unknown operation'


def ConsultaArrendatario(arrendatario_wallet_address):
    msg = concat("consulta arrendatario: ", arrendatario_wallet_address)

    Notify(msg)

    context = GetContext()
    arrendador_wallet_address = Get(context, arrendatario_wallet_address)
    if not arrendador_wallet_address:
        Notify("El arrendatario no se encuentra registrado")
        return False

    Notify(arrendador_wallet_address)
    return arrendador_wallet_address


def RegistrarArrendatario(arrendatario_wallet_address, arrendador_wallet_address):
    msg = concat("RegistrarArrendatario: ", arrendatario_wallet_address)

    Notify(msg)

    if not CheckWitness(arrendador_wallet_address):
        Notify("Usted no esta autorizado para Registrar arrendatario")
        return False

    context = GetContext()
    exists = Get(context, arrendatario_wallet_address)
    if exists:
        msg = concat("Arrendatario: ", exists)
        Notify(msg)
        return False

    Put(context, arrendatario_wallet_address, arrendador_wallet_address)
    return True
