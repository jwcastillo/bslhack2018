from boa.builtins import concat
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Runtime import CheckWitness, Notify
from boa.interop.Neo.Storage import *

TOKEN_NAME = 'TOC COIN'

TOKEN_SYMBOL = 'TOCC'

TOKEN_DECIMALS = 8

# This is the script hash of the address for the owner of the token
# This can be found in ``neo-python`` with the wallet open, use ``wallet`` command
TOKEN_OWNER = b'S\xefB\xc8\xdf!^\xbeZ|z\xe8\x01\xcb\xc3\xac/\xacI)'

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
PLATAFORMA_WALLET = b'031a6c6fbbdf02ca351745fa86b9ba5a9452d785ac4f7fc2b7548ca2a46c4fcf4a'

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
        return RegistrarArrendatario(arrendatario_wallet_address, arrendador_wallet_address, PLATAFORMA_WALLET)

    elif operation == 'transferir':
        if nargs < 2:
            print(
                "parametros requeridos: [arrendatario_wallet_address] [to_address]")
            return 0
        arrendatario_wallet_address = args[0]
        to_address = args[1]
        return TransferirContrato(arrendatario_wallet_address, to_address)

    elif operation == 'agregar_pago':
        if nargs < 2:
            print(
                "parametros requeridos: [arrendatario_wallet_address] [arrendador_wallet_address]")
            return 0
        arrendatario_wallet_address = args[0]
        propiedad_id = args[1]
        return AgregarPago(arrendatario_wallet_address, arrendador_wallet_address, MONTOARRIENDO)

    elif operation == 'agregar_pago_retrasado':
        if nargs < 2:
            print(
                "parametros requeridos: [arrendatario_wallet_address] [arrendador_wallet_address]")
        return 0
        arrendatario_wallet_address = args[0]
        propiedad_id = args[1]

        return AgregarPagoRetrasado(arrendatario_wallet_address, arrendador_wallet_address, PLATAFORMA_WALLET, MONTOARRIENDO + MULTA)

    else:
        return 'unknown operation'


def FiniquitoContrato(arrendatario_wallet_address, arrendador_wallet_address, id_propiedad, monto_reparacion):

    msg = concat("Finiquito del Contrato: ", arrendatario_wallet_address)


Notify(msg)

context = GetContext()
arrendador_wallet_address = Get(context, arrendatario_wallet_address)
if not arrendador_wallet_address:
    Notify("El arrendatario no se encuentra registrado")
return False

Notify(arrendador_wallet_address)
return arrendador_wallet_address


def AgregarClausulas(clausula, arrendatario_wallet_address):

    msg = concat("Se registro una nueva clausula arrendatario: " +
                 clausula, arrendatario_wallet_address)


Notify(msg)

context = GetContext()
Put(context, "Clausula", clausula)
return clausula


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


def LogPagosAtrasados(arrendatario_wallet_address, info):
    context = GetContext()
    Put(context, arrendatario_wallet_address, info)
    return True


def TransferirContrato(arrendatario_wallet_address, to_address):
    msg = concat("Transferir Contrato: ", arrendatario_wallet_address)
    Notify(msg)
    context = GetContext()
    arrendador_wallet_address = Get(context, arrendatario_wallet_address)
    if not arrendador_wallet_address:
        Notify("El arrendador no se encuentra registrado")
        return False

    if not CheckWitness(arrendador_wallet_address):
        Notify("El arrendador no tiene cartera")
    return False

    if not len(to_address) != 34:
        Notify(
            "Direccion de Cartera invalida. debe poseer 34 letras")
    return False

    Put(context, arrendatario_wallet_address, to_address)
    return True


def BorrarArrendatario(arrendatario_wallet_address):
    msg = concat("Borrar Arrendatario: ", arrendatario_wallet_address)
    Notify(msg)
    context = GetContext()
    arrendador_wallet_address = Get(context, arrendatario_wallet_address)
    if not arrendador_wallet_address:
        Notify("Domain is not yet registered")
    return False

    if not CheckWitness(arrendador_wallet_address):
        Notify("No tiene permiso para realizar esta operacion, No se puede Transferir")
    return False

    Delete(context, arrendatario_wallet_address)
    return True


# TOKEN
def crowdsale_available_amount(ctx):
    """
    :return: int The amount of tokens left for sale in the crowdsale
    """

    in_circ = Get(ctx, TOKEN_CIRC_KEY)

    available = TOKEN_TOTAL_SUPPLY - in_circ

    return available


def add_to_circulation(ctx, amount):
    """
    Adds an amount of token to circlulation
    :param amount: int the amount to add to circulation
    """

    current_supply = Get(ctx, TOKEN_CIRC_KEY)

    current_supply += amount
    Put(ctx, TOKEN_CIRC_KEY, current_supply)
    return True


def get_circulation(ctx):
    """
    Get the total amount of tokens in circulation
    :return:
        int: Total amount in circulation
    """
    return Get(ctx, TOKEN_CIRC_KEY)


OnTransfer = RegisterAction('transfer', 'addr_from', 'addr_to', 'amount')
OnApprove = RegisterAction('approve', 'addr_from', 'addr_to', 'amount')


def handle_nep51(ctx, operation, args):

    if operation == 'name':
        return TOKEN_NAME

    elif operation == 'decimals':
        return TOKEN_DECIMALS

    elif operation == 'symbol':
        return TOKEN_SYMBOL

    elif operation == 'totalSupply':
        return Get(ctx, TOKEN_CIRC_KEY)

    elif operation == 'balanceOf':
        if len(args) == 1:
            return Get(ctx, args[0])

    elif operation == 'transfer':
        if len(args) == 3:
            return do_transfer(ctx, args[0], args[1], args[2])

    elif operation == 'transferFrom':
        if len(args) == 3:
            return do_transfer_from(ctx, args[0], args[1], args[2])

    elif operation == 'approve':
        if len(args) == 3:
            return do_approve(ctx, args[0], args[1], args[2])

    elif operation == 'allowance':
        if len(args) == 2:
            return do_allowance(ctx, args[0], args[1])

    return False


def do_transfer(ctx, t_from, t_to, amount):

    if amount <= 0:
        return False

    if len(t_to) != 20:
        return False

    if CheckWitness(t_from):

        if t_from == t_to:
            print("transfer to self!")
            return True

        from_val = Get(ctx, t_from)

        if from_val < amount:
            print("insufficient funds")
            return False

        if from_val == amount:
            Delete(ctx, t_from)

        else:
            difference = from_val - amount
            Put(ctx, t_from, difference)

        to_value = Get(ctx, t_to)

        to_total = to_value + amount

        Put(ctx, t_to, to_total)

        OnTransfer(t_from, t_to, amount)

        return True
    else:
        print("from address is not the tx sender")

    return False


def do_transfer_from(ctx, t_from, t_to, amount):

    if amount <= 0:
        return False

    available_key = concat(t_from, t_to)

    if len(available_key) != 40:
        return False

    available_to_to_addr = Get(ctx, available_key)

    if available_to_to_addr < amount:
        print("Insufficient funds approved")
        return False

    from_balance = Get(ctx, t_from)

    if from_balance < amount:
        print("Insufficient tokens in from balance")
        return False

    to_balance = Get(ctx, t_to)

    new_from_balance = from_balance - amount

    new_to_balance = to_balance + amount

    Put(ctx, t_to, new_to_balance)
    Put(ctx, t_from, new_from_balance)

    print("transfer complete")

    new_allowance = available_to_to_addr - amount

    if new_allowance == 0:
        print("removing all balance")
        Delete(ctx, available_key)
    else:
        print("updating allowance to new allowance")
        Put(ctx, available_key, new_allowance)

    OnTransfer(t_from, t_to, amount)

    return True


def do_approve(ctx, t_owner, t_spender, amount):

    if not CheckWitness(t_owner):
        return False

    if amount < 0:
        return False

    # cannot approve an amount that is
    # currently greater than the from balance
    if Get(ctx, t_owner) >= amount:

        approval_key = concat(t_owner, t_spender)

        if amount == 0:
            Delete(ctx, approval_key)
        else:
            Put(ctx, approval_key, amount)

        OnApprove(t_owner, t_spender, amount)

        return True

    return False


def do_allowance(ctx, t_owner, t_spender):

    return Get(ctx, concat(t_owner, t_spender))
