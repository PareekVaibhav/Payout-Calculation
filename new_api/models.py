from django.db import models


class MASDiv(models.Model):
    division_name = models.CharField(db_column="sBuName", max_length=60)


class MASUom(models.Model):  # Used in esIN, esPR, esWO, eTender only
    unit_of_measure = models.CharField(db_column="sUomName", max_length=5)
    MEASURE_CHOICE = (
        ("1", "Count"),
        ("2", "Area"),
        ("3", "Volume"),
        ("4", "Weight"),
        ("5", "Time"),
    )
    measure_type = models.CharField(
        db_column="sUomType", max_length=1, choices=MEASURE_CHOICE, default="1"
    )
    unit_desc = models.CharField(db_column="sDesc", max_length=25, blank=True)

    class Meta:
        db_table = "MASUOM"
        verbose_name = "d1.UoM Master"


class MASCat(models.Model):  # Category used in all modules
    category_code = models.IntegerField(db_column="nGrpNo", null=True)
    category_name = models.CharField(db_column="sGrpName", max_length=20, blank=True)
    system_code = models.CharField(
        db_column="sSysNo", max_length=2, blank=True, null=True
    )
    program_code = models.CharField(
        db_column="sPrgCode", max_length=8, blank=True, null=True
    )

    class Meta:
        #    managed = False
        db_table = "MASCAT"
        ordering = ["category_code"]
        verbose_name = "a8.Category Master"

    def __str__(self):
        return f"{self.category_code}"


class MASSlm(models.Model):
    first_name = models.CharField(db_column="sFrstNm", max_length=255)
    last_name = models.CharField(
        db_column="sLstNm", max_length=255, blank=True, null=True
    )
    mobile = models.CharField(db_column="sMobile", max_length=30, blank=True, null=True)
    telephone = models.CharField(
        db_column="stelephn", max_length=30, blank=True, null=True
    )
    email = models.EmailField(db_column="eEmail", max_length=255)

    class Meta:
        db_table = "MASSLM"
        verbose_name = "a6.Sales Person"

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"


class MASLan(models.Model):
    language_name = models.CharField(db_column="sLanguage", max_length=40)

    class Meta:
        db_table = "MASLAN"
        verbose_name = "a9.Language"

    def __str__(self) -> str:
        return self.language_name


class CRMInv(models.Model):
    division = models.ForeignKey(MASDiv, models.PROTECT, db_column='IdDivInv', null=True)
    item_code = models.CharField(db_column='sItmCode', max_length=19, blank=True, null=True)
    tax_percent = models.DecimalField(max_digits=32, db_column='fTaxPerc', decimal_places=2, default='0.05')
    item_name = models.CharField(db_column='sDesc', max_length=50, blank=True, null=True)
    add_desc = models.CharField(db_column='sAddDesc', max_length=50, blank=True, null=True)
    primary_uom = models.ForeignKey(MASUom, models.DO_NOTHING, db_column='IDPrimUnit', blank=True, null=True)
    category1 = models.ForeignKey(MASCat, models.PROTECT, db_column='IdInvCat1', blank=True, null=True)
    category2 = models.ForeignKey(MASCat, models.PROTECT, related_name='invcat2', db_column='IdInvCat2', blank=True,
                                  null=True)
    category3 = models.ForeignKey(MASCat, models.PROTECT, related_name='invcat3', db_column='IdInvCat3', blank=True,
                                  null=True)
    gl_code = models.IntegerField(db_column='nGLCode', blank=True, null=True)
    current_stock = models.FloatField(db_column='fCurStk', blank=True, null=True)
    reserve_stock = models.FloatField(db_column='fResStk', blank=True, null=True)
    average_cost = models.FloatField(db_column='fCostAvg', blank=True, null=True)
    market_cost = models.FloatField(db_column='fCostMkt', blank=True, null=True)
    sell_price = models.FloatField(db_column='fSellPrice', blank=True, null=True)

    class Meta:
        #    managed = False
        db_table = 'CRMINV'
        verbose_name = 'a3.Product Master'


class CRMLed(models.Model):
    contact = models.ForeignKey('CRMCnt', models.PROTECT, db_column='IdCnt', null=True, blank=True)
    first_name = models.CharField(db_column='sNameF', max_length=255, blank=True)
    last_name = models.CharField(db_column='sNameL', max_length=255, blank=True)
    email = models.EmailField(db_column='eEmail', max_length=80, null=True, blank=True)
    phone = models.CharField(db_column='sPhone', max_length=20)
    language = models.ForeignKey(MASLan, models.PROTECT, db_column='IdLan', null=True, blank=True)
    STATUS_CHOICE = (('assigned', 'Assigned'), ('in process', 'In Process'), ('converted', 'Converted'),
                     ('recycled', 'Recycled'), ('closed', 'Closed'))
    lead_status = models.CharField(db_column='sLedStats', max_length=50, choices=STATUS_CHOICE, blank=True)
    lead_source = models.ForeignKey('CRMEvt', models.PROTECT, db_column='IdEvt', null=True, blank=True)  # From event
    pipeline = models.ForeignKey('CRMPil', models.PROTECT, db_column='IdPil', null=True, blank=True)
    city = models.CharField(db_column='sCity', max_length=40, blank=True)
    country = models.CharField(db_column='sCountry', max_length=40, blank=True)
    website = models.CharField(db_column='sWebsite', max_length=60, blank=True)
    description = models.TextField(db_column='tDesc', blank=True)
    assigned_to = models.ForeignKey(MASSlm, models.PROTECT, db_column='IdSlm', null=True, blank=True)
    opportunity_amount = models.IntegerField(db_column='nOppAmt', blank=True, null=True)
    generated_by = models.CharField(db_column='sGenBy', max_length=80, blank=True)
    created_on = models.DateTimeField(db_column='dCreatedOn', auto_now_add=True)
    enquiry_type = models.CharField(db_column='sEnqType', max_length=40, blank=True)
    IND_CHOICE = (("ADVERTISING", "ADVERTISING"),
                  ("REAL_ESTATE", "REAL_ESTATE"),
                  ("RETAIL", "RETAIL"),
                  ("AUTOMOTIVE", "AUTOMOTIVE"),
                  ("BANKING", "BANKING"),
                  ("CONTRACTING", "CONTRACTING"),
                  ("DISTRIBUTOR", "DISTRIBUTOR"),
                  ("SERVICES", "SERVICES"),
                  ("OTHERS", "OTHERS"))
    industry = models.CharField(db_column='sIndstry', max_length=20, choices=IND_CHOICE, blank=True)

    class Meta:
        db_table = 'CRMLED'
        verbose_name = 'b1.Lead'

    def __str__(self):
        return str(self.first_name) + str(self.last_name)


class CRMCnt(models.Model):
    contact = models.CharField(max_length=10, db_column='sCnt', blank=True, null=True)
    class Meta:
        db_table = 'CRMCNT'


class CRMEvt(models.Model):
    event = models.CharField(max_length=128, db_column='ev_name', blank=True, null=True)
    destination = models.CharField(max_length=128, db_column='ev_dest', blank=True, null=True)
    class Meta:
        db_table = 'CRMEVT'


class CRMPil(models.Model):
    pipeline_name = models.CharField(db_column='sPilName', max_length=255)
    target_days = models.IntegerField(db_column='nAllwDur', default=0)
    probability_percent = models.IntegerField(db_column='nProbPerc', default=0)
    is_active = models.BooleanField(db_column='bIsActive', default=False)

    class Meta:
        db_table = 'CRMPIL'
        verbose_name = 'a4.Pipeline Setup'

    def __str__(self):
        return self.pipeline_name


class CRMOpp(models.Model):
    lead = models.ForeignKey(CRMLed, models.PROTECT, db_column='IdLed', null=True, blank=True)
    opportunity_name = models.CharField(db_column='sOppName', max_length=255)
    pipeline_stage = models.ForeignKey('CRMPil', models.PROTECT, db_column='IdPil', null=True, blank=True)
    CURRENCY_CHOICE = (('AED', 'AED'), ('EUR', 'EUR'), ('USD', 'USD'), ('GBP', 'GBP'))
    currency = models.CharField(db_column='sCurr', max_length=3, choices=CURRENCY_CHOICE, blank=True)
    amount = models.IntegerField(db_column='nAmt', blank=True, default=0)
    probability = models.IntegerField(db_column='nProb', default=0)
    description = models.TextField(db_column='tDesc', blank=True)
    created_on = models.DateTimeField(db_column='dtCreatedOn', auto_now_add=True)
    target_date = models.DateField(db_column='dTrgtdte', blank=True, null=True)
    closed_on = models.DateField(db_column='dClosedOn', blank=True, null=True)

    class Meta:
        db_table = 'CRMOPP'
        verbose_name = 'b2.Opportunity'

    def __str__(self):
        return self.opportunity_name


class CRMTsk(models.Model):
    opportunity = models.ForeignKey(CRMOpp, models.PROTECT, db_column='IdOpp', null=True)
    lead = models.ForeignKey(CRMLed, models.PROTECT, db_column='IdLed', null=True)
    STATUS_CHOICES = (
        ("New", "New"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    )
    PRIORITY_CHOICES = (("Low", "Low"), ("Medium", "Medium"), ("High", "High"))
    TASKTYPE_CHOICES = (
        ("call", "Call"),
        ("telephone call", "TelePhone Call"),
        ("email", "Email"),
        ("visit", "Visit"),
        ("meeting", "Meeting"),
        ("demo", "Demo"),
    )
    task_date = models.DateField(db_column='dTskDt', blank=True, null=True)  # default current date
    task_type = models.CharField(db_column='sTskType', max_length=25, choices=TASKTYPE_CHOICES)
    task_notes = models.TextField(db_column='tTskNts', max_length=255)
    status = models.CharField(db_column='sStatus', max_length=25, choices=STATUS_CHOICES)
    priority = models.CharField(db_column='sPriorty', max_length=25, choices=PRIORITY_CHOICES)
    due_date = models.DateField(db_column='dduedt', blank=True, null=True)
    created_on = models.DateTimeField(db_column='dtCreatedOn', auto_now_add=True)

    class Meta:
        db_table = 'CRMTSK'
        verbose_name = 'b3.Task'

    def __str__(self):
        return self.task_type
