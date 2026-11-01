from datetime import datetime, date
from typing import Literal
from pydantic import BaseModel, Field, field_validator
import re

class Company(BaseModel):
    symbol: str
    name: str
    sector: str
    exchange: str = 'NSE'
    isin: str | None = None

class DailyBar(BaseModel):
    symbol: str
    date: date
    open: float
    high: float
    low: float
    close: float = Field(gt=0, allow_inf_nan=False)
    volume: int = Field(ge=0)
    basis: Literal['raw','adjusted']
    provider: str
    currency: str
    source_url: str
    ingested_at: datetime
    finalized: bool

class SourceDocument(BaseModel):
    id: str
    symbol: str
    title: str
    kind: str
    url: str
    date: str | None
    section: str
    text: str
    hash: str
    status: str

class RawFiling(BaseModel):
    id: str
    symbol: str
    subject: str
    url: str
    raw_category: str
    source_published_at: datetime
    ingested_at: datetime
    source_exchange: str
    record_date: date | None = None
    payment_date: date | None = None

class CanonicalEvent(BaseModel):
    id: str
    symbol: str
    headline: str
    category: str
    score: int
    reason_codes: list[str]
    evidenceRefs: list[str]
    source_published_at: str

class Query(BaseModel):
    as_of: datetime | None = None
    @field_validator('as_of')
    @classmethod
    def aware(cls,v):
        if v is not None and v.tzinfo is None:raise ValueError('as_of needs timezone')
        return v
    symbol: str = Field(min_length=1,max_length=24)
    question: str = Field(min_length=3,max_length=2000)
    @field_validator('symbol')
    @classmethod
    def ticker(cls,v):
        v=v.strip().upper().removesuffix('.NS').removesuffix('.BO')
        if not re.fullmatch(r'[A-Z0-9][A-Z0-9&-]{0,19}',v):raise ValueError('Use a valid exchange ticker')
        return v
    @field_validator('question')
    @classmethod
    def safe(cls,v):
        if re.search(r'(\.\./|<script|\b(?:SELECT|DROP|EXEC|INSERT)\b.*\b(?:FROM|TABLE|INTO)\b|__import__|os\.system)',v,re.I):raise ValueError('Unsupported query content')
        return v.strip()

class QueryPlan(BaseModel):
    intent: Literal['financial_snapshot','guidance_vs_actuals','business_overview','cash_conversion','financial_trajectory','unknown']
    symbol: str
    metric: str | None = None
    ratio: Literal['pat_margin'] | None = None
    metrics: list[str] = Field(default_factory=list)
    period: str = 'FY25 / Q4 FY25 historical corpus'
    operations: list[Literal['retrieve','compare','explain']]
    max_passages: int = 4
    fiscal_year: int | None = None
    quarter: int | None = None
    basis: str | None = None

class AlertRule(BaseModel):
    price_pct: float = Field(default=3,ge=0.1,le=50,allow_inf_nan=False)
    volume_multiple: float = Field(default=2,ge=0.1,le=20,allow_inf_nan=False)

# Evidence is source data, never executable instructions.
from decimal import Decimal
from pydantic import model_validator, HttpUrl

class SourceEvidence(BaseModel):
    id: str
    symbol: str
    title: str
    publisher: str
    url: HttpUrl
    kind: Literal['annual_report','concall_transcript','exchange_result','investor_presentation']
    report_date: date | None = None
    published_at: datetime | None = None
    ingested_at: datetime
    page: int | None = Field(default=None,ge=1)
    section: str
    text: str = Field(max_length=5000)
    evidence_method: Literal['legacy_curated_note','pdf_extracted_reviewed','pdf_extracted_unverified']
    content_hash: str
    document_hash: str | None = None
    offsets: tuple[int,int] | None = None
    rights: str = 'Minimal derived records; publisher retains copyright; redistribution rights not certified.'
    @model_validator(mode='after')
    def valid_evidence(self):
        if self.url.scheme!='https':raise ValueError('HTTPS publisher source required')
        if self.published_at and self.published_at.tzinfo is None:raise ValueError('Timezone required')
        if self.evidence_method.startswith('pdf_') and (not self.document_hash or not self.page):
            raise ValueError('PDF evidence requires original file hash and page')
        if self.offsets and not (0<=self.offsets[0]<self.offsets[1]):raise ValueError('Invalid extraction offsets')
        return self

class FinancialFact(BaseModel):
    id: str
    symbol: str
    evidence_id: str
    metric: Literal['revenue','pbt','pat','ebitda','free_cash_flow','operating_margin','revenue_growth_cc']
    value: Decimal = Field(allow_inf_nan=False)
    currency: Literal['INR','USD','NONE']
    scale: Literal['rupee','thousand','crore','million','billion','percent']
    basis: Literal['consolidated','standalone','company_reported']
    accounting_standard: str
    period_start: date
    period_end: date
    fiscal_year: int = Field(ge=2000,le=2100)
    quarter: int | None = Field(default=None,ge=1,le=4)
    period_type: Literal['quarter','annual']
    definition: str
    verification: Literal['curated_verified','pdf_reviewed','unverified']
    @model_validator(mode='after')
    def valid_period(self):
        if self.period_start>=self.period_end:raise ValueError('Invalid period bounds')
        days=(self.period_end-self.period_start).days+1
        if self.period_type=='quarter' and (self.quarter is None or not 80<=days<=100):raise ValueError('Not a discrete quarter')
        if self.period_type=='annual' and (self.quarter is not None or not 350<=days<=380):raise ValueError('Not an annual period')
        if self.period_type=='annual':
            expected_start=date(self.fiscal_year-1,4,1);expected_end=date(self.fiscal_year,3,31)
        else:
            ends={1:(6,30),2:(9,30),3:(12,31),4:(3,31)};starts={1:(4,1),2:(7,1),3:(10,1),4:(1,1)}
            y=self.fiscal_year if self.quarter==4 else self.fiscal_year-1
            expected_start=date(y,*starts[self.quarter]);expected_end=date(y,*ends[self.quarter])
        if (self.period_start,self.period_end)!=(expected_start,expected_end):raise ValueError('Fiscal period dimensions mismatch (March-year-end Indian FY only)')
        if self.scale=='percent' and self.metric not in ('operating_margin','revenue_growth_cc'):raise ValueError('Monetary metric cannot use percent scale')
        if self.scale=='percent' and self.currency!='NONE':raise ValueError('Percent is not currency')
        return self

class GuidanceRecord(BaseModel):
    id: str
    symbol: str
    evidence_id: str
    actual_fact_id: str
    metric: str
    low: Decimal
    high: Decimal
    target_start: date
    target_end: date
    basis: str
    scale: str
    definition: str
    @model_validator(mode='after')
    def valid_range(self):
        if self.low>self.high or self.target_start>=self.target_end:raise ValueError('Invalid guidance range/period')
        return self
