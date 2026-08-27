# Value Scenario Formula (value-formula.md)

**Formula version:** 2.0

Documents the deterministic calculation that the `reversa-pricing-estimate` agent applies for the Value scenario. The v2 formula replaces the fixed 6-to-12-month multiple with a percentage capture of the declared annual economic value.

## Source and rationale

Value-based pricing uses the perceived or economic value for the client as the price base, not just internal cost or competitor prices.

References:

- Hinterhuber, A. (2008), *Customer value-based pricing strategies: why companies resist*, Journal of Business Strategy, 29(4), DOI 10.1108/02756660810887079
- Nagle, Hogan and Zale, *The Strategy and Tactics of Pricing*, 5th ed., Routledge, 2016, especially Economic Value to the Customer

The 10% to 30% range is a Reversa commercial heuristic for B2B/freelance/agency. It should be described as a capture of part of the annual value, not as a universal academic law.

## Step 1: input validation

```
if monthly_return_declared == 0 AND cost_of_not_doing == 0:
  available = false
  explanation_pt_br = "Value Scenario cannot be calculated: client did not declare measurable return."
```

`users_impacted` is commercial context. It appears in estimate.md but does not enter the v2 numerical calculation.

## Step 2: annual economic value

```
annual_value =
  max(monthly_return_declared * 12, cost_of_not_doing)
```

The client may declare:

- recurring monthly return
- annual cost of not doing
- both

When both exist, the formula uses the larger defensible economic value.

## Step 3: value capture

```
value_capture_min = 0.10
value_capture_recommended = 0.20
value_capture_max = 0.30

price_min = round_currency(annual_value * value_capture_min)
recommended_price = round_currency(annual_value * value_capture_recommended)
price_max = round_currency(annual_value * value_capture_max)
```

## Step 4: explanatory payback

If `monthly_return_declared > 0`, calculate payback as secondary explanation:

```
payback_months_min = price_min / monthly_return_declared
payback_months_max = price_max / monthly_return_declared
```

If `monthly_return_declared == 0`, write `payback_months_min = null` and `payback_months_max = null`.

Payback does not define price. It only helps the user explain the proposal.

## Examples

### Example 1: clear monthly return

```
monthly_return_declared = 2000 BRL
cost_of_not_doing = 5000 BRL

annual_value = max(2000 * 12, 5000) = 24000
price_min = 24000 * 0.10 = 2400
recommended_price = 24000 * 0.20 = 4800
price_max = 24000 * 0.30 = 7200
payback_months_min = 1.2
payback_months_max = 3.6
```

### Example 2: annual loss prevention

```
monthly_return_declared = 0
cost_of_not_doing = 60000 BRL

annual_value = max(0, 60000) = 60000
price_min = 6000
recommended_price = 12000
price_max = 18000
payback_months_min = null
payback_months_max = null
```

### Example 3: no measurable data

```
monthly_return_declared = 0
cost_of_not_doing = 0

available = false
```

## Billing currency conversion

Identical to Effort. When `profile.billing_currency` is filled:

```
price_min_billing = round_currency(price_min / exchange_rate_to_local)
recommended_price_billing = round_currency(recommended_price / exchange_rate_to_local)
price_max_billing = round_currency(price_max / exchange_rate_to_local)
```

## Limitations and assumptions

1. The return declared by the client is not validated by the agent
2. The 10% to 30% capture range is a documented heuristic
3. `users_impacted` does not enter the v2 numerical calculation
4. Extreme values are not truncated
5. The explanation may mention months of payback, but must not say the price is "6 to 12 months"
