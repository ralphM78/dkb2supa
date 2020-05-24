#!/usr/bin/env python3

'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Dieses Programm ist Freie Software: Sie können es unter den Bedingungen
    der GNU General Public License, wie von der Free Software Foundation,
    Version 3 der Lizenz oder (nach Ihrer Wahl) jeder neueren
    veröffentlichten Version, weiter verteilen und/oder modifizieren.

    Dieses Programm wird in der Hoffnung bereitgestellt, dass es nützlich sein wird, jedoch
    OHNE JEDE GEWÄHR,; sogar ohne die implizite
    Gewähr der MARKTFÄHIGKEIT oder EIGNUNG FÜR EINEN BESTIMMTEN ZWECK.
    Siehe die GNU General Public License für weitere Einzelheiten.

    Sie sollten eine Kopie der GNU General Public License zusammen mit diesem
    Programm erhalten haben. Wenn nicht, siehe <https://www.gnu.org/licenses/>.
'''


import argparse, csv, os
from sys import exit
from datetime import datetime
from re import match
from schwifty import IBAN

parser = argparse.ArgumentParser(description="Convert DKB CSV into SUPA CSV.")
parser.add_argument("-i", "--input", help="DKB CSV input file", type=argparse.FileType("r", encoding="iso-8859-1"), required=True, metavar="INPUTFILE")
parser.add_argument("-o", "--output", help="SUPA formated CSV output file", type=argparse.FileType("w", encoding="utf-8"), required=True, metavar="OUTPUTFILE")
parser.add_argument("--iban", help="Optionally your IBAN", metavar="DE820000000000")
parser.add_argument("--cur", default="EUR", help="Optional Currency. Default is EUR", metavar="EUR")
args = parser.parse_args()


OwnrAcctIBAN = ""
OwnrAcctBankCode = ""
OwnrAcctBIC = ""
OwnrAcctNo = ""

# check for valid IBAN
if args.iban:
    try:
        OwnrAcctIBAN = IBAN(args.iban)
    except ValueError as error:
        error_string = str(error)
        print("ERROR in --iban argument: ", error_string)
        exit(1)

# check for currency length if passed
if args.cur:
    if len(args.cur) != 3:
        print("Currency can have a length of 3 chars only. EUR,USD,CHF ...")
        exit(1)
    else:
        cur = args.cur.upper()

# convert IBAN if passed
if OwnrAcctIBAN:
    OwnrAcctIBANformated = OwnrAcctIBAN.formatted
    OwnrAcctBIC = str(OwnrAcctIBAN.bic)
    OwnrAcctBankCode = OwnrAcctIBAN.bank_code
    OwnrAcctNo = OwnrAcctIBAN.account_code

with args.input as CsvInputfile:
    inputData = csv.reader(CsvInputfile, delimiter=";", quotechar='"')

# don't process first 7 lines
    for _ in range(7):
        next(inputData)

    with args.output as CsvOutputfile:
        outputData = csv.writer(CsvOutputfile, delimiter=',')
        # writing header line
        outputData.writerow(["Id", "AcctId", "OwnrAcctCcy", "OwnrAcctIBAN", "OwnrAcctNo", "OwnrAcctBIC", "OwnrAcctBankCode", "BookgDt", "ValDt", "TxDt", "Amt", "AmtCcy", "CdtDbtInd", "EndToEndId", "PmtInfId", "MndtId", "CdtrId", "RmtInf", "PurpCd", "BookgTxt", "PrimaNotaNo", "BankRef", "BkTxCd", "RmtdNm", "RmtdUltmtNm", "RmtdAcctCtry", "RmtdAcctIBAN", "RmtdAcctNo", "RmtdAcctBIC", "RmtdAcctBankCode", "BookgSts", "BtchBookg", "BtchId", "GVC", "GVCExtension", "Category", "Notes", "ReadStatus", "Flag"])

        bookings = 0

        for row in inputData:

            # check if line starts with 2 date fields
            if match("^\[('(\d{2}\.){2}\d{4}', ){2}", str(row)):
                # convert booking date
                BookDt = datetime.strptime(row[0], "%d.%m.%Y").strftime("%Y-%m-%d")
                # convert value date
                ValDt = datetime.strptime(row[1], "%d.%m.%Y").strftime("%Y-%m-%d")
                # remove HTML markup
                br = row[4].replace("<br />", " ")
                # convert value format
                Amt = row[7].replace(".", "")
                Amt = Amt.replace(",", ".")
                # remove double spaces
                RmtdNm = ' '.join(row[3].split())
                RmtInf = ' '.join(br.split())

                outputData.writerow(["", "", cur, OwnrAcctIBAN, OwnrAcctNo, OwnrAcctBIC, OwnrAcctBankCode, BookDt, ValDt, "", Amt, cur, "", row[10].strip(), "", row[9].strip(), row[8].strip(), RmtInf, "", row[2], "", "", "", RmtdNm, "", "", row[5], "", row[6], "", "", "", "", "", "", "", "", "false", "None"])
                # count converted lines
                bookings += 1

print("")

if args.iban:
    print("{:<25s} {:s}".format("Used IBAN is:", OwnrAcctIBANformated))
    print("{:<25s} {:s}".format("Used BIC is:", OwnrAcctBIC))
    print("{:<25s} {:s}".format("Used Bankcode is:", OwnrAcctBankCode))
    print("{:<25s} {:s}".format("Used account number is:", OwnrAcctNo))

print("{:<25s} {:s}".format("Used currency:", cur))
print("{:<25s} {:s}".format("Used input file:", os.path.dirname(os.path.realpath(__file__)) + "/" + args.input.name))
print("{:<25s} {:s}".format("Used output file:", os.path.dirname(os.path.realpath(__file__)) + "/" + args.output.name))
print("{:<25s} {:d}".format("Converted bookings:", bookings))
print("")
