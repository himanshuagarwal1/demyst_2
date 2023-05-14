def get_account_statement(account_number, accounting_provider):
    SBI =  "sbi"
    MYOB = "myob"
    XERO = "xero"

    data1 = [
    {
        "year": 2020,
        "month": 12,
        "profitOrLoss": 250000,
        "assetsValue": 1234
    },
    {
        "year": 2020,
        "month": 11,
        "profitOrLoss": 1150,
        "assetsValue": 5789
    },
    {
        "year": 2020,
        "month": 10,
        "profitOrLoss": 2500,
        "assetsValue": 22345
    },
    {
        "year": 2020,
        "month": 9,
        "profitOrLoss": -187000,
        "assetsValue": 223452
    }
]
    data2 = [
    {
        "year": 2020,
        "month": 12,
        "profitOrLoss": 2500,
        "assetsValue": 123
    },
    {
        "year": 2020,
        "month": 11,
        "profitOrLoss": 11500,
        "assetsValue": 578
    },
    {
        "year": 2020,
        "month": 10,
        "profitOrLoss": 250,
        "assetsValue": 2245
    },
    {
        "year": 2020,
        "month": 9,
        "profitOrLoss": -1870000,
        "assetsValue": 23452
    }
]

    if accounting_provider == SBI:
        return data1 + data2
    elif accounting_provider == MYOB:
        return data1
    else:
        return data2
    
def get_preAssessment(sheet, loan_amount):
    profit  = 0
    assetsValue = 0
    for data in sheet[:12]:
        profit += data["profitOrLoss"]
        assetsValue +=data["assetsValue"]
    assetsValue = assetsValue/len(sheet)

    if profit > 0:
        preassessment = 60
    else:
        preassessment = 20 
    if assetsValue > loan_amount:
        preassessment = 100

    return (profit , preassessment)

def get_decision_engine(account, buisness, assest, preAssessment):
    
    if preAssessment > 50:
        return True
    else:
        return False