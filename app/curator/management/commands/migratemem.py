from django.core.management.base import BaseCommand, CommandError
from memdir.models import Member
from django.db import models
from datetime import datetime
from decimal import Decimal

import xlrd
import os
import re

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Error(Exception):
    pass

class MigrateError(Error):
    """
    This is raised when the migration fails
    """
    def __init__(self, prev, next, msg):
        self.prev = prev
        self.next = next
        self.msg = msg

class RegionError(Error):
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

def match_region(longregion):
    lr = longregion
    if lr == "Other":
        return 'other'
    elif lr == "Fraser Valley":
        return 'fraservalley'
    elif lr == "Interior":
        return 'vancoast'
    elif lr == "Vancouver Island":
        return 'vanisle'
    elif lr == "Northern":
        return 'northern'
    elif lr == "Vancouver Coastal":
        return 'vancoast'
    else:
        return 'unknown'
    """
    except RegionError as e:
        print "There was no region found for the cell: %s" % e
    """

def getrenew(date):
    if date == "Not Renewing":
        return
    else:
        return datetime(*xlrd.xldate_as_tuple(date, 0))

def getfee(cellval):
    if cellval.value == '' or cellval.value == None:
        return
    else:
        return Decimal(str(cellval.value))

def yesbool(renew):
    if renew == "YES":
        return True
    else:
        return False

def getrec(cell):
    """ Get the reciept number if there is one """
    if cell.value == '' or cell.value == None:
        return
    else:
        return int(cell.value)

def getnum(phonecell):
    """ Get phone number """
    if phonecell.value == '' or phonecell.value == None:
        return
    else:
        phonepatt = re.compile(r'\D*(\d{3})\D*(\d{3})\D*(\d{4})$')
        found = phonepatt.search(str(phonecell.value))
        if found != None:
            found = found.groups()
            return "%s-%s-%s" % (found[0], found[1], found[2])
        else:
            return


def migrate(row):
    """
    The magical migration function
    """
    mem = Member()
    # A
    mem.memnum = row[0].value
    # B, C
    mem.renewal = getrenew(row[2].value)
    # D
    mem.region = match_region(row[3].value)
    # E
    mem.agency = row[4].value
    # F
    mem.address = row[5].value
    # G
    mem.city = row[6].value
    # H
    mem.province = row[7].value
    # I
    mem.postal_code = row[8].value
    # J
    mem.agphone = getnum(row[9])
    # K
    mem.agfax = getnum(row[10])
    # L
    mem.agdirect = row[11].value
    # M
    mem.dirphone = getnum(row[12])
    # N
    mem.email = row[13].value
    # O
    mem.resname = row[14].value
    # P
    mem.frpphone = getnum(row[15])
    # Q
    mem.coordinator = row[16].value
    # R
    mem.coemail = row[17].value
    # S
    mem.website = "http://%s" % row[18].value
    # T
    mem.joint = yesbool(row[19].value)
    # U
    mem.prior = yesbool(row[20].value)
    # V
    mem.newjoint2009 = yesbool(row[21].value)
    # W
    mem.newjoint2010 = yesbool(row[22].value)
    # X
    mem.newjoint2011 = yesbool(row[23].value)
    # Y
    mem.newbc2010 = yesbool(row[24].value)
    # Z
    mem.frpbcfee = getfee(row[25])
    # AA
    mem.jointmemfee = getfee(row[26])
    # AB -- AUTO 28 [27]
    ## AC -- AUTO TK 29 [28]
    # AD
    mem.receipt = getrec(row[29])
    # AE
    mem.owecanada = getfee(row[30])
    # AF
    mem.paidfrpc = yesbool(row[31].value)
    # AG
    mem.owefrpbc = getfee(row[32])
    # AH
    mem.paidfrpbc = yesbool(row[33].value)
    # AI
    mem.notes = row[34].value

    try:
        mem.save()
    except Error as e: #models.FieldError as e:
        print "There was a field error: %s" % e
    #    raise MigrateError
    #finally:
    #    raise MigrateError

class Command(BaseCommand):
    args = '<None>'
    help = 'Migrates excel to the database'
    def handle(self, *args, **options):
        book = xlrd.open_workbook("%s/../../../../assets/members.xls" % BASE_DIR)
        sheet = book.sheets()[0]
        ret = ""
        for row in range(1, sheet.nrows):
            try:
                migrate(sheet.row(row))
                ret += "No errors! WOOT!"
            except MigrateError as e:
                ret += "Migration failed with error: %s" % e.value

