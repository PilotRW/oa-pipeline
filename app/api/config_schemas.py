from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


SUPPORTED_MARKETPLACES = {
    "DE",
    "FR",
    "IT",
    "ES",
    "NL",
    "BE",
    "UK",
    "US",
}


class PipelineSettingsUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    use_real_keepa: bool | None = None
    default_batch_size: int | None = Field(
        default=None,
        ge=1,
        le=500,
    )
    default_marketplace: str | None = Field(
        default=None,
        min_length=2,
        max_length=16,
    )

    @field_validator("default_marketplace")
    @classmethod
    def normalize_marketplace(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return value

        normalized = value.upper()

        if normalized not in SUPPORTED_MARKETPLACES:
            supported = ", ".join(sorted(SUPPORTED_MARKETPLACES))
            raise ValueError(
                f"Unsupported marketplace. Supported values: {supported}"
            )

        return normalized


class ResearchRulesUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    min_priority_score: Decimal | None = Field(
        default=None,
        ge=0,
    )
    min_stock: int | None = Field(
        default=None,
        ge=0,
    )
    low_stock_threshold: int | None = Field(
        default=None,
        ge=0,
    )
    medium_stock_threshold: int | None = Field(
        default=None,
        ge=0,
    )
    high_stock_threshold: int | None = Field(
        default=None,
        ge=0,
    )

    preferred_cost_min: Decimal | None = Field(
        default=None,
        ge=0,
    )
    preferred_cost_max: Decimal | None = Field(
        default=None,
        ge=0,
    )
    medium_cost_max: Decimal | None = Field(
        default=None,
        ge=0,
    )
    min_cost: Decimal | None = Field(
        default=None,
        ge=0,
    )

    min_roi_percent: Decimal | None = Field(
        default=None,
        ge=0,
    )
    min_profit: Decimal | None = Field(
        default=None,
        ge=0,
    )
    referral_fee_percent: Decimal | None = Field(
        default=None,
        ge=0,
        le=100,
    )
    fulfillment_fee_fixed: Decimal | None = Field(
        default=None,
        ge=0,
    )
    max_sales_rank: int | None = Field(
        default=None,
        ge=0,
    )
    min_monthly_sales: int | None = Field(
        default=None,
        ge=0,
    )
    exclude_amazon_in_stock: bool | None = None
    lookup_excluded_brands: list[str] | None = None
    lookup_excluded_title_keywords: list[str] | None = None
    lookup_min_cost: Decimal | None = Field(
        default=None,
        ge=0,
    )
    lookup_max_cost: Decimal | None = Field(
        default=None,
        ge=0,
    )

    score_stock_high: int | None = None
    score_stock_medium: int | None = None
    score_stock_low: int | None = None
    score_stock_very_low: int | None = None

    score_cost_preferred: int | None = None
    score_cost_medium: int | None = None
    score_cost_high: int | None = None
    score_cost_low: int | None = None

    score_brand_present: int | None = None
    score_title_present: int | None = None
    score_ean_present: int | None = None

    @model_validator(mode="after")
    def validate_stock_thresholds(self):
        thresholds = [
            self.low_stock_threshold,
            self.medium_stock_threshold,
            self.high_stock_threshold,
        ]

        if all(value is not None for value in thresholds):
            if not (
                self.low_stock_threshold
                <= self.medium_stock_threshold
                <= self.high_stock_threshold
            ):
                raise ValueError(
                    "Stock thresholds must be ordered: "
                    "low <= medium <= high"
                )

        return self

    @field_validator(
        "lookup_excluded_brands",
        "lookup_excluded_title_keywords",
    )
    @classmethod
    def normalize_lookup_terms(
        cls,
        value: list[str] | None,
    ) -> list[str] | None:
        if value is None:
            return value

        terms = {
            str(item).strip()
            for item in value
            if str(item).strip()
        }

        return sorted(terms, key=str.casefold)

    @model_validator(mode="after")
    def validate_cost_ranges(self):
        ranges = [
            self.preferred_cost_min,
            self.preferred_cost_max,
            self.medium_cost_max,
        ]

        if all(value is not None for value in ranges):
            if not (
                self.preferred_cost_min
                <= self.preferred_cost_max
                <= self.medium_cost_max
            ):
                raise ValueError(
                    "Cost ranges must be ordered: "
                    "preferred_min <= preferred_max <= medium_max"
                )

        return self

    @model_validator(mode="after")
    def validate_lookup_cost_range(self):
        if (
            self.lookup_min_cost is not None
            and self.lookup_max_cost is not None
            and self.lookup_min_cost > self.lookup_max_cost
        ):
            raise ValueError(
                "Lookup cost range must be ordered: min <= max"
            )

        return self
