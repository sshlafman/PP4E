#!/usr/bin/python3
"""
=====================================================================================
Compute ACA (a.k.a. "obamacare") health insurance premium tax credit
from income, number people, actual and benchmark plan premiums, IRS
povertylevel%=>contribution% mappings, and HHS poverty levels.
Main entry point:
    credit = ACApremiumTaxCredit(income, numpeople, actualpremium, benchmarkpremium)
    netpremium = actualpremium - credit

Used to create functions in Excel for future year projections -- either as
a prototype for translation to VBA, or usable directly with a plug-in like 
PyXLL or DataNitro.  Requires inflation of some parematers in this role, not
shown here.  (Personally, the ACA law today means a 50% premiums increase with
no offsetting tax credit, but later years may offset, and possibly eclipse, 
some of this cost increase.)

Sources and resources:
An online credit calculator --  http://www.wahbexchange.org/;
IRS docs --  http://www.gpo.gov/fdsys/pkg/FR-2012-05-23/pdf/2012-12421.pdf;
IRS docs --  http://www.gpo.gov/fdsys/pkg/FR-2013-05-03/pdf/2013-10463.pdf;
HHS poverty bases --  http://aspe.hhs.gov/poverty/13poverty.cfm#guidelines;
An overview -- http://www.cbpp.org/files/QA-on-Premium-Credits.pdf;
An example -- http://consumersunion.org/wp-content/uploads/2013/05/Tax_Credit_Worksheet_2014.pdf

Note: you should not take the results of this code as gospel (and should
not use them for your taxes!); these are ballpark calculations only
which may differ slightly from IRS final procedures, and are used for
only rough estimation purposes in spreadsheet yearly projections.
=====================================================================================
"""
trace = print   # or: lambda *args: None

#####################################################################################
# poverty percent => pay percent (per IRS)
#####################################################################################

#
# Per IRS, for mapping income to insuree maximum premium contribution:
# (Income/poverty)% low..high  =>  MaxContributionIncome% low..high
#

IRSpovertyToContribRanges = [
     [(0,   133), (2.0,  2.0) ],           # povlow%..povhigh%, paylow%..payhigh%
     [(133, 150), (3.0,  4.0) ],           # should this be 2.0..4.0?: not in IRS doc
     [(150, 200), (4.0,  6.3) ],
     [(200, 250), (6.3,  8.05)],
     [(250, 300), (8.05, 9.5) ],
     [(300, 400), (9.5,  9.5)]]            # inclusive at 400, but not for 400.0001

def mapRanges(povpct, povlow, povhigh, paylow, payhigh):     # 135, (133..150), (3.0..4.0)
    """
    Evenly map povpct in [povlow..povhigh] to [paylow..payhigh].
    All aruments and return value are scaled percentages (*100).
    See # comments to the right for an example's expected calcs.
    This scheme may or may not match the final IRS technique.
    """
    povrange = povhigh - povlow                              # 17  = 150 - 133
    payrange = payhigh - paylow                              # 1.0 = 4.0 - 3.0
    povincr  = povpct  - povlow                              # 2   = 135 - 133
    pctincr  = povincr / povrange                            # pct = 2 / 17
    paypct   = paylow + (pctincr * payrange)                 # 3.0 + (pct * 1.0)
    return round(paypct, 2)                                  # per IRS: round to nearest 100th


def test_mapRanges():
    for [(povlow, povhigh), (paylow, payhigh)] in IRSpovertyToContribRanges:
        for povpct in range(povlow, povhigh):
            paypct = mapRanges(povpct, povlow, povhigh, paylow, payhigh)
            print(povpct, '=>', paypct)
        print('-' * 40)
        
    assert mapRanges(210, 200, 250, 6.3, 8.05) == 6.65       # per IRS doc example
    assert mapRanges(135, 133, 150, 3.0, 4.0)  == 3.12       # original dev example
    assert mapRanges(150, 150, 200, 4.0, 6.3)  == 4.0
    assert mapRanges(200, 150, 200, 4.0, 6.3)  == 6.3
    assert mapRanges(300, 300, 400, 9.5, 9.5)  == 9.5
    assert mapRanges(400, 300, 400, 9.5, 9.5)  == 9.5

           
#####################################################################################
# income => poverty percent (per HHS)
#####################################################################################

def povertyPercent(income, numpeople):
    """
    Result is a percent * 100.
    Calculate poverty level base from income and size of household.
    This can change per year, and may or may not reflect inflation.
    """                                         
    HHSpovertyLevels = {
         1: 11490,                      # or index a list[numpeople-1]
         2: 15510,                      # 15510 = 62040 / 4
         3: 19530,                      # 11490 = 45960 / 4
         4: 23550,
         5: 27570,
         6: 31590,                      # VB: must inflate levels?
         7: 35610,
         8: 39630}

    if numpeople in HHSpovertyLevels:
        povlevel = HHSpovertyLevels[numpeople]
    else:
        povlevel = HHSpovertyLevels[8] + (4020 * (numpeople - 8))
    return (income / povlevel) * 100


testincomes = (100000,
               62039, 62040, 62041,    # +$1 income = $0 credit threshhold for 2 ppl!
               45959, 45960, 45961,    # +$1 income = $0 credit thresshold for 1 ppl!
               22980, 52988,           # see asserts ahead
               40000, 31021, 31020, 20000, 10000)
              
def test_povertyPercent():
    print('=' * 40)
    for numpeople in (2, 1):
        for income in testincomes:
            print(numpeople, income, '=>', povertyPercent(income, numpeople))
    print('=' * 40)


#####################################################################################
# income => taxcredit (combine tools)
#####################################################################################

def applyContribRanges(povpct):
    """
    Calculate max premium contribution % from poverty %.
    Result and inputs are both scaled percents (* 100).
    """
    lenofranges = len(IRSpovertyToContribRanges)
    countranges = enumerate(IRSpovertyToContribRanges)
    
    for row, [(povlow, povhigh), (paylow, payhigh)] in countranges:
        lastrow = (row+1 == lenofranges)
        if lastrow:
            inrange = (povlow <= povpct <= povhigh)        # VB: x <= y and y <= z
        else:                                                    
            inrange = (povlow <= povpct < povhigh)

        if inrange:
            paypct = mapRanges(povpct, povlow, povhigh, paylow, payhigh)
            trace('(%.2f => %.2f)' % (povpct, paypct))
            return paypct

    return 100  # > high end of ranges: no tax credit offset, pays premium in full
    
def insureePremiumContribution(income, numpeople):
    """
    Calculate insuree's maximum premium contribution $ from
    income, poverty levels, and contribution percent ranges.
    """
    povertyPct = povertyPercent(income, numpeople)
    contribPct = applyContribRanges(povertyPct)
    contribAmt = income * (contribPct / 100)
    trace('[%s, %s => %.2f, %.2f, %.2f]' %
                (income, numpeople, contribPct, contribAmt, contribAmt/12))
    return contribAmt

def ACApremiumTaxCredit(income, numpeople, actualpremium, benchmarksilverpremium):
    """
    ============================================================================
    MAIN ENTRY POINT: calculate the premium credit, for Excel formulas.
    All values here are give as yearly/annual amounts, not monthly.
    Caveats:
    --does not handle Medicaid cutoff at 100/133% of poverty line.
    --does nothing about uneven monthly amounts or prepayments.
    --really computed for -prior- year from payments and old plans.
    --does nothing for cost-sharing subsidies for out-of-pockets.
    --may differ slightly from IRS due to rounding errors.
    --some aspects very per location but are ignored or givens here.

    Not taxcredit = max(0, (yourpremium - contribution(income, numpeople)):
    Raw tax credit is difference between the benchmark silver plan's
    premium for area and the insurees's maximum contribution calculated
    from income and family size (not insuree premium - contribution).

    This credit can then be applied to actual premiums regardless of plan
    (and may hence decrease or increase actual insuree premium contribution),
    but is capped at the total actual plan cost paid.  Thus, calculating tax
    credits and plan net cost requires income details, plus two plan premiums
    for your area per year: insuree's actual, and "benchmark" silver plan,
    in addition to each year's expected poverty line data.

    There are 6 permutations of the ap, bp, and yc premium and contibution
    variables, only 2 of which (plus their equality cases) are truly valid:
    [ap >= bp >= c] (ex:gold>silver) and [bp >= ap >= c] (ex:bronze<silver).

    ============================================================================
    Per final? IRS docs...
    § 1.36B–3 Computing the premium assistance credit amount.
    a) In general. A taxpayer’s premium assistance credit amount for a taxable 
    year is the sum of the premium assistance amounts determined under
    paragraph (d) of this section for all coverage months for individuals in the 
    taxpayer’s family.
    ...
    (d) ***Premium assistance amount.
    The premium assistance amount for a coverage month is the lesser of— 
    (1) The premiums for the month for one or more qualified health plans in 
    which a taxpayer or a member of the taxpayer’s family enrolls; or 
    (2) The excess of the adjusted monthly premium for the applicable 
    benchmark plan over 1/12 of the product of a taxpayer’s household 
    income and the applicable percentage for the taxable year.
    ...
    (f) Applicable benchmark plan—(1) In general. Except as otherwise provided 
    in this paragraph (f), the applicable benchmark plan for each coverage 
    month is the second lowest cost silver plan ... offered through the Exchange
    for the rating area where the taxpayer resides ...
    ============================================================================
    """
    contributionbase = insureePremiumContribution(income, numpeople)
    benchmarkexcess  = max(0, benchmarksilverpremium - contributionbase)
    taxcredit        = min(actualpremium, benchmarkexcess) 
    netpremium       = actualpremium - taxcredit              # VB: must inflate premiums
    return taxcredit                                          # VB: netpremium not returned


def test_ACApremiumTaxCredit():
    """
    Actual insuree and benchmark annual premiums will be taken
    from spreadsheet table cells in Excel (and possibly inflated
    for future years): hardcode/estimate here.
    """
    examplepremiums = (431, 816)
    for numpeople in (2, 1):
        benchprem  = examplepremiums[numpeople-1] * 12        # 2nd lowest silver for area
        actualprem = benchprem - (100 * 12)                   # bronze est: $100/mo < silver
        print('-' * 79)
        for income in testincomes:
            print('ppl=%d, inc=%d' % (numpeople, income))
            
            yrtaxcredit  = ACApremiumTaxCredit(income, numpeople, actualprem, benchprem)
            yrnetpremium = actualprem - yrtaxcredit 

            print('** [Month: %d (prem) = %.2f (tax) + %.2f (you)] [Year: %d=%d+%d]\n' %
                           (actualprem/12, yrtaxcredit/12, yrnetpremium/12,
                            actualprem,    yrtaxcredit,    yrnetpremium))

    global trace
    trace = lambda *args: None
    assert round(ACApremiumTaxCredit(22980,1,5000,5000), 2) == 3552.26     # actual = benchmark, 200% pov
    assert round(ACApremiumTaxCredit(22980,1,4500,5000), 2) == 3552.26     # actual < benchmark
    assert round(ACApremiumTaxCredit(22980,1,3500,5000), 2) == 3500.00
    assert round(ACApremiumTaxCredit(22980,1,1000,5000), 2) == 1000.00
    
    assert round(ACApremiumTaxCredit(22980,1,6000,5000), 2) == 3552.26     # actual > benchmark
    assert round(ACApremiumTaxCredit(22980,1,10000,5000),2) == 3552.26
    
    assert round(ACApremiumTaxCredit(22980,1,1448,5000), 2) == 1448.00     # actual near contribution
    assert round(ACApremiumTaxCredit(22980,1,1447,5000), 2) == 1447.00
    assert round(ACApremiumTaxCredit(22980,1,5,5000), 2)    == 5.00        # unlikely but true
    assert round(ACApremiumTaxCredit(52988,4,15000,15000), 2) == 11195.46  # 225%:   15000=11195+3804

    assert round(ACApremiumTaxCredit(62039,2,8592,9792), 2)   == 3898.30   # 399.99%: 8592=3898+4693 (716,816)
    assert round(ACApremiumTaxCredit(62040,2,8592,9792), 2)   == 3898.20   # 400.00%: 8592=3898+4693 (716,816)
    assert round(ACApremiumTaxCredit(62041,2,8592,9792), 2)   == 0         # MASSIVE $4k DROPOFF FOR $1 INCOME!

    assert round(ACApremiumTaxCredit(94200,4,12000,13200), 2) == 4251.00   # 400%:  12k=4251+7749 (354/645)
    assert round(ACApremiumTaxCredit(94199,4,12000,13200), 2) == 4251.09   # 400%:  ditto
    assert round(ACApremiumTaxCredit(94201,4,12000,13200), 2) == 0         # MASSIVE DROPOFF FOR 4: (0/1000)
    trace = print


def test_interactive():
    """
    Test main function with interactively entered parameters.
    """
    print('*' * 80)
    while True:
        try:
            reply = input('[income,people,actprem,benchprem]? ')
            if not reply: break
            income, numpeople, actprem, benchprem = [int(x) for x in reply.split(',')]
            yrtaxcredit  = ACApremiumTaxCredit(income, numpeople, actprem, benchprem)
            yrnetpremium = actprem - yrtaxcredit
            print('Taxcredit => %.2f, Netpremium => %.2f  [Monthly credit/premium: %.2f/%.2f]\n' %
                            (yrtaxcredit,      yrnetpremium,
                             yrtaxcredit / 12, yrnetpremium / 12))
        except EOFError:
            break


#####################################################################################
# main: self test
#####################################################################################

if __name__ == '__main__':
    test_mapRanges()
    test_povertyPercent()         # comment-out to disable (see also 'trace' setting)
    test_ACApremiumTaxCredit()
    test_interactive()
        
    
  
