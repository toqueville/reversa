# estimate.md Template

This is the Markdown template that the `reversa-pricing-estimate` agent uses to generate `_reversa_sdd/_pricing/<feature>/estimate.md`. Replace all `<placeholders>` with actual values. Maintain the fixed structure.

```markdown
# Price Estimate

**Feature:** `<relative_feature_dir>`
**Generated on:** <created_at_local_readable>
**Calculation versions:** Effort v<effort_formula_version>, Value v<value_formula_version>, Market v<market_table_version>

**Consumed prerequisites:**
- Profile: `<output_folder>/_pricing/profile.json`
- Size: `<output_folder>/_pricing/<feature>/size.json` (class `<complexity_class>`, auxiliary score `<size_score>`)

## Overview

| Scenario | Range | Comment |
|---|---|---|
| **Effort** | <effort_str> | <hours_min> to <hours_max>h, cost + tax + markup |
| **Value** | <value_str> | 10% to 30% of declared annual value |
| **Market Range** | <market_str> | hourly rate sourced by country and seniority |

## Effort Scenario

**What it is:** price calculated from probable hours, hourly rate, approximate tax reserve, and project markup. It is the defensible floor to avoid subsidizing the client.

**When to use:** always as a sanity check. Charging below Effort means taking a loss or reducing project profit too much.

| Item | Value |
|---|---|
| Complexity class | <complexity_class> |
| Seniority | <seniority> |
| Seniority factor | <seniority_factor> |
| Estimated hours | <hours_min> to <hours_max> h |
| Midpoint | <estimated_hours> h |
| Hourly rate | <hourly_rate> <currency>/h |
| Direct cost | <direct_cost_min> to <direct_cost_max> <currency> |
| Approximate tax reserve | <approximate_tax_min> to <approximate_tax_max> <currency> |
| Project markup (<margin_percent>%) | <applied_markup_min> to <applied_markup_max> <currency> |
| **Effort Range** | **<price_min> to <price_max> <currency>** |
| Midpoint | <total_price> <currency> |

<vat_warning_if_applicable>
<billing_currency_block_if_applicable>

## Value Scenario

**What it is:** price based on a portion of the annual economic value that the feature generates or protects for the client. Reversa uses a 10% to 30% capture of the declared annual value.

**When to use:** when the client can declare return, savings, or cost of not doing.

<if value.available>

| Item | Value |
|---|---|
| Declared monthly return | <monthly_return_declared> <currency> |
| Users impacted | <users_impacted> |
| Cost of not doing | <cost_of_not_doing> <currency> |
| Annual value used | <annual_value> <currency> |
| Applied capture | 10% to 30% |
| Recommended price | <recommended_price> <currency> |
| **Value Range** | **<price_min> to <price_max> <currency>** |
| Approximate payback | <payback_str> |

<billing_currency_block_if_applicable>

<if NOT value.available>

> **Value Scenario not available:** <unavailable_reason>

</if>

## Market Range Scenario

**What it is:** range derived from hourly benchmark by country and seniority, multiplied by the same hour range from the Effort scenario.

**When to use:** as an external reference. v2 does not multiply by client profile because there is no reliable public dataset for that.

<if market.available>

| Item | Value |
|---|---|
| Country / Seniority | <country_name> / <seniority> |
| Model / Client profile | <pricing_model> / <client_profile> |
| Complexity | <complexity_class> |
| Market hourly rate | <market_hourly_min> to <market_hourly_max> <currency>/h |
| Source type | <source_kind> |
| Reference year | <source_year> |
| Sources | <sources> |
| **Market Range** | **<market_price_min> to <market_price_max> <currency>** |

<if fallback applied>

> Fallback applied: <reason>

</if>

<billing_currency_block_if_applicable>

<if NOT market.available>

> **Market Scenario not available:** <unavailable_reason>

</if>

## How to choose among the three

<guidance_based_on_scenarios>

General heuristic:

1. Client without clear return: use Effort as the floor and Market as external reference
2. Client with high and clear return: prefer Value, with Effort only as minimum floor
3. Effort above Market: review profile, size, or client fit
4. Market above Effort: there is room to increase markup or improve the proposal

## Disclaimer

The numbers in this estimate are approximations for budget guidance, not a guarantee of closing a deal. The tax factor is an approximate reserve, not an exact legal tax rate. Actual tax validation is the responsibility of the user's accountant. The market range is static and based on the sources documented in `market-benchmarks.md`. The return declared by the client in the Value scenario is raw input, not validated. It is recommended to add `_reversa_sdd/_pricing/<feature>/estimate.{md,json}` to `.gitignore` before committing.
```

## Billing currency

When `profile.billing_currency` is filled, each scenario gets an extra row:

```markdown
| In <billing_currency> | <billing_value> <billing_currency> (exchange rate: 1 <billing_currency> = <exchange_rate_to_local> <currency>) |
```

## Short comments

| Scenario | Short comment |
|---|---|
| Effort | `<hours_min> to <hours_max>h, cost + tax + markup` |
| Value | `10% to 30% of declared annual value` or `Not available` |
| Market | `hourly rate sourced by country and seniority` or `Not available` |
