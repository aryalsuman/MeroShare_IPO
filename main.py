import csv

import requests


class MeroShare:
    def __init__(self, dp, password, username, apply_kitta, crnno, transactionPIN, get_bankID_initial=0):
        self.dp = dp
        self.password = password
        self.username = username
        self.apply_kitta = apply_kitta
        self.crnno = crnno
        self.transactionPIN = transactionPIN
        self.get_bankID_initial = get_bankID_initial

    def first_time_setup(self):
        with requests.Session() as session:
            get_DPs = 'https://webbackend.cdsc.com.np/api/meroShare/capital/'
            response = session.get(get_DPs)
            # print(response.json())
            for dp in response.json():
                if dp.get('code') == str(self.dp):
                    self.get_id = dp.get('id')
                    break
            auth_url = 'https://webbackend.cdsc.com.np/api/meroShare/auth/'
            payload = {'clientId': self.get_id,
                       'password': self.password,
                       'username': self.username
                       }
            response = session.post(auth_url, json=payload)
            # print(response)

            authorazation = response.headers['Authorization']

            # for bank details
            bank_url = 'https://webbackend.cdsc.com.np/api/meroShare/bank/'

            response = session.get(
                bank_url, headers={'Authorization': authorazation})
            # print(response.json())
            print("Available Banks:")
            banks = response.json()
            bank_ids = [bank.get('id') for bank in banks]
            for bank in banks:
                print(f"ID: {bank.get('id')}, Name: {bank.get('name')}")

            if len(banks) == 1:
                self.get_bankID_initial = banks[0].get('id')
                print(f"Auto-selected Bank: {banks[0].get('name')}")
            else:
                while True:
                    bank_id = input("Enter the bank ID: ")
                    if int(bank_id) in bank_ids:
                        self.get_bankID_initial = bank_id
                        break
                    else:
                        print("Invalid bank ID. Please try again.")

    def apply_shares(self):
        is_right = False
        with requests.Session() as session:
            get_DPs = 'https://webbackend.cdsc.com.np/api/meroShare/capital/'
            response = session.get(get_DPs)
            # print(response.json())
            for dp in response.json():
                if dp.get('code') == str(self.dp):
                    self.get_id = dp.get('id')
                    break
            auth_url = 'https://webbackend.cdsc.com.np/api/meroShare/auth/'
            payload = {'clientId': self.get_id,
                       'password': self.password,
                       'username': self.username,
                       }
            
            headers = {
                "accept": "application/json, text/plain, */*",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "en-US,en;q=0.9",
                "authorization": "null",
                "cache-control": "no-cache",
                "connection": "keep-alive",
                "content-type": "application/json",
                "dnt": "1",
                "host": "webbackend.cdsc.com.np",
                "origin": "https://meroshare.cdsc.com.np",
                "pragma": "no-cache",
                "referer": "https://meroshare.cdsc.com.np/",
                "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
            }
            response = requests.post(url=auth_url, json=payload,headers=headers)
            # print(response.json())

            authorazation = response.headers['Authorization']

            ownDetails_url = 'https://webbackend.cdsc.com.np/api/meroShare/ownDetail/'
            response = session.get(ownDetails_url, headers={
                'Authorization': authorazation})
            get_demate = response.json().get('demat')
            print('-'*40)
            print(response.json().get('name'))
            print('-'*40)
            get_boid = response.json().get('boid')

            bank_url = 'https://webbackend.cdsc.com.np/api/meroShare/bank/'

            response = session.get(
                bank_url, headers={'Authorization': authorazation})
            # print(response.json())
        ##############################################
            get_bankID = self.get_bankID_initial

        ##############################################
            applicableIssue_url = 'https://webbackend.cdsc.com.np/api/meroShare/companyShare/applicableIssue/'

            payload = {'filterFieldParams': [{'key': 'companyIssue.companyISIN.script', 'alias': 'Scrip'}, {'key': 'companyIssue.companyISIN.company.name', 'alias': 'Company Name'}, {'key': 'companyIssue.assignedToClient.name', 'value': '', 'alias': 'Issue Manager'}],
                       'page': 1, 'size': 10, 'searchRoleViewConstants': 'VIEW_APPLICABLE_SHARE', 'filterDateParams': [{'key': 'minIssueOpenDate', 'condition': '', 'alias': '', 'value': ''}, {'key': 'maxIssueCloseDate', 'condition': '', 'alias': '', 'value': ''}]}
            response = requests.post(applicableIssue_url, json=payload, headers={
                                    'Authorization': authorazation})
            # print(response.json())

            for company in response.json().get('object'):
                # "shareGroupName":"Ordinary Shares"
                if company.get('shareGroupName') == 'Ordinary Shares':
                    get_companyShareId = company.get('companyShareId')
                    # print(get_companyShareId)
                    get_scrip = company.get('scrip')
                    print('---------')
                    print(f'Stock:{get_scrip}')
                    print('---------')
                    get_action = company.get('action', 'apply')
                    # check if eligible for the share
                    checkEligibility_url = 'https://webbackend.cdsc.com.np/api/meroShare/applicantForm/customerType/' + \
                        str(get_companyShareId)+'/'+str(get_demate)
                    # print(checkEligibility_url)
                    response = session.get(checkEligibility_url, headers={
                        'Authorization': authorazation})
                    if response.json().get('message') == 'Customer can apply.':
                        if company.get('reservationTypeName') == "RIGHT SHARE": 
                            print("You are eligible for Right Share")
                            reserve_quantity_url='https://webbackend.cdsc.com.np/api/shareCriteria/boid/'+str(get_demate)+'/'+str(get_companyShareId)
                            response = session.get(reserve_quantity_url, headers={
                                'Authorization': authorazation})
                            self.apply_kitta = int(response.json().get('reservedQuantity'))
                            right_id = response.json().get('id')
                            is_right = True
                        # GET FULL DETAIL OF BANK
                        bankDetail_url = 'https://webbackend.cdsc.com.np/api/meroShare/bank/' + \
                            str(get_bankID)
                        response = session.get(bankDetail_url, headers={
                            'Authorization': authorazation})
                        print("Bank-Branch:"+response.json()[0].get('branchName'))
                        response = response.json()[0]
                        get_accountBranchId = response.get('accountBranchId')
                        # print(get_accountBranchId)
                        get_accountNumber = response.get('accountNumber')
                        # print(get_accountNumber)
                        get_accountTypeId = response.get('accountTypeId')
                        # print(get_accountTypeId)
                        get_customerId = response.get('id')
                        # print(get_customerId)

                        # apply for the share
                        if get_action == 'apply':
                            apply_url = 'https://webbackend.cdsc.com.np/api/meroShare/applicantForm/share/apply'

                            payload = {'accountBranchId': get_accountBranchId,
                                    'accountNumber': get_accountNumber,
                                    'accountTypeId': get_accountTypeId,
                                    'appliedKitta': self.apply_kitta,
                                    'bankId': get_bankID,
                                    'boid': get_boid,
                                    'companyShareId': get_companyShareId,
                                    'crnNumber': self.crnno,
                                    'customerId': get_customerId,
                                    'demat': get_demate,
                                    'transactionPIN': self.transactionPIN
                                    }
                            if is_right:
                                payload['shareCriteriaId'] = right_id
                            response = session.post(apply_url, json=payload, headers={
                                                    'Authorization': authorazation})
                            if response.status_code == 201 or response.status_code == 200:
                                print('***********')
                                print('*         *')
                                print('* Success *')
                                print('*         *')
                                print('***********')
                            else:
                                print('**********')
                                print('*        *')
                                print('* Failed *')
                                print('*        *')
                                print('**********')
                        elif get_action == 'edit':
                                print('**********')
                                print('*        *')
                                print('*Can Edit*')
                                print('*        *')
                                print('**********')
                        elif get_action == 'inProcess':
                                print('**********')
                                print('*        *')
                                print('*Can Edit*')
                                print('*        *')
                                print('**********')


if __name__ == "__main__":

    with open('Acnt.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if reader.line_num < 2:
                continue
            get_dp = row[0]
            get_password = row[1]
            get_username = row[2]
            get_kitta = row[3]
            get_crnno = row[4]
            get_transactionPIN = row[5]
            get_bankID_initial = row[6]

            if get_bankID_initial == '0':
                print("First time setup")
                print(get_username)
                meroshare = MeroShare(
                    get_dp, get_password, get_username, get_kitta, get_crnno, get_transactionPIN)
                meroshare.first_time_setup()
            else:
                meroshare = MeroShare(get_dp, get_password, get_username,
                                      get_kitta, get_crnno, get_transactionPIN, get_bankID_initial)
                meroshare.apply_shares()
