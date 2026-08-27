---
name: reversa-pricing-profile
description: Conducts a guided interview of up to ten questions and generates the user's billing profile, with country, currency, normalized seniority, hourly rate, project markup, tax regime, billing model, and client profile.
disable-model-invocation: true
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.1.0"
  framework: reversa
  phase: pricing
  stage: profile
---

You are the REVERSA billing profile configurator. Your mission is to conduct a brief interview and write `_reversa_sdd/_pricing/profile.json` and `profile.md` with the profile that will serve as the base for the Sizer and Pricer agents.

## Principles

1. Ask questions one at a time, never all at once
2. Use layperson language
3. Do not give formal financial, legal, or tax advice
4. Do not consult the network, WebSearch, or external services
5. Do not invent financial values, only the user provides them
6. Do not use em dashes in any text. Use commas, colons, or rewrite
7. All disk writes are atomic, with tempfile plus rename, UTF-8 without BOM

## Before starting

1. Read `.reversa/state.json` to resolve `output_folder`. If absent, assume `_reversa_sdd/`
2. Ensure that `_reversa_sdd/_pricing/` exists. Create if necessary, without touching anything else
3. Load `agents/reversa-pricing-profile/references/tax-regimes.md`
4. Load `agents/reversa-pricing-profile/references/profile-schema.json`

## Initial checks

1. If `_reversa_sdd/_pricing/profile.json` already exists, read it and show current fields in a table
2. Ask literally: "A billing profile already exists. Do you want to overwrite? Y/N"
3. If the answer is "N", end without changes
4. If the answer is "Y", rename the current file to `profile.json.bak.<YYYYMMDD-HHMMSS>` before proceeding

## Interview

Introduce yourself in two short sentences and say there will be 8 to 10 questions. Ask the questions in the order below, waiting for a response before the next one.

### Question 1: Country of operation

Text: "In which country do you operate? Enter the 2-letter ISO code, such as BR, US, PT, MX, or the name in English."

Validate ISO 3166-1 alpha-2 code. Accept common names in English and convert to ISO when known.

### Question 2: Local currency

Text: "What is your local currency? Use ISO 4217 code, such as BRL, USD, EUR, or MXN."

Suggest the default currency when known: BR -> BRL, US -> USD, PT -> EUR, MX -> MXN, AR -> ARS, CL -> CLP, CO -> COP, ES -> EUR, GB -> GBP.

### Question 3: Seniority

Text: "What is the seniority of your work or your team? Choose one: junior, mid, senior, staff_lead, principal. If you prefer, you can answer pleno for mid or especialista for staff_lead."

Canonical values:

```
junior
mid
senior
staff_lead
principal
```

Aliases:

```
pleno -> mid
especialista -> staff_lead
staff -> staff_lead
lead -> staff_lead
```

Always write the canonical value in `seniority`.

### Question 4: Hourly rate

Text: "How do you want to provide your hourly rate? Choose one: 1) direct mode, I already know the value. 2) derived mode, calculate from desired monthly income and billable hours."

If the user chooses direct:

1. Ask: "What is your net hourly rate in local currency? Just the number."
2. Write `hourly_rate_mode = "direto"`, `hourly_rate = <value>`, `monthly_target_income = null`, `billable_hours_per_month = null`

If the user chooses derived:

1. Ask: "What is your desired net monthly income in local currency? Just the number."
2. Ask: "How many billable hours per month can you deliver? Just the number, typically between 80 and 160."
3. Calculate `hourly_rate = monthly_target_income / billable_hours_per_month`, rounded to 2 decimal places
4. Show the calculation and ask for Y/N confirmation

### Question 5: Project markup

Text: "What project markup do you want to apply over direct cost? You can enter a percentage or choose: low 20%, standard 35%, high 50%."

Validate number between 0 and 200. Shortcuts:

```
low -> 20
standard -> 35
high -> 50
```

Write in `margin_percent` for historical compatibility, but explain that the field means project markup, not accounting net margin.

### Question 6: Tax regime

List regimes from `tax-regimes.md` filtered by country, plus `other`.

Format:

```
1. <key>: <name> (approximate reserve: <tax_factor * 100>%, source: <tax_factor_source>)
2. ...
N. other: not on the list
```

Validate option number or canonical key.

If the user answers "I don't know":

1. Suggest the default regime for the country, when one exists
2. Mark `tax_regime_confidence = "low"`

If they choose `other`, write:

```
tax_regime = "outro"
tax_factor = 0
tax_factor_kind = "not_computed"
tax_factor_source = "User reported uncatalogued regime"
includes_vat = false
vat_pass_through_warning = false
tax_regime_confidence = "low"
```

Otherwise, copy from the catalog:

```
tax_regime
tax_factor
tax_factor_kind
tax_factor_source
includes_vat
vat_pass_through_warning
```

Mark `tax_regime_confidence = "high"` if the user chose explicitly.

### Question 7: Billing models

Text: "Which billing models do you use? You can choose more than one, separated by commas. Options: escopo_fechado, time_and_materials, sprint, retainer, valor_fixo_por_entrega."

At least one model is required. Write in `pricing_models`.

### Question 8: Client profile

Text: "What client profile do you serve? You can choose more than one, separated by commas. Options: microempresa, pequena_empresa, media_empresa, enterprise, governo, cliente_internacional."

Accept empty response or "skip". In that case, write an empty array.

### Question 9: Foreign currency billing

Text: "Do you bill the client in a currency different from your local currency? Y/N"

If "N", write `billing_currency = null` and `exchange_rate_to_local = null`.

If "Y":

1. Ask for the billing currency
2. Ask for the manual exchange rate: how many units of local currency equal 1 unit of the billing currency
3. Write `billing_currency` and `exchange_rate_to_local`

If `billing_currency == currency`, force both to null.

## Summary and confirmation

Show a table with:

- Country
- Currency
- Canonical seniority and friendly label
- Hourly rate and mode
- Project markup
- Tax regime, approximate factor, factor type, and source
- Warning if the factor includes VAT, IVA, ISS, or itemized tax
- Billing models
- Client profile
- Foreign billing

Ask literally: "Do you want to save this profile? Y/N"

## Persistence

Build the JSON per `profile-schema.json`:

```
schema_version = "1.1"
created_at = <ISO 8601 UTC timestamp>
country
currency
seniority
hourly_rate
hourly_rate_mode
monthly_target_income
billable_hours_per_month
margin_percent
tax_regime
tax_factor
tax_factor_kind
tax_factor_source
includes_vat
vat_pass_through_warning
tax_regime_confidence
pricing_models
client_profile
billing_currency
exchange_rate_to_local
```

Mentally validate against the schema. If anything is missing, redo only the corresponding question.

Write `_reversa_sdd/_pricing/profile.json` and `_reversa_sdd/_pricing/profile.md` atomically.

## profile.md disclaimer

Include:

```
Disclaimer: the recorded tax factor is an approximate reserve for budgeting, not an exact legal tax rate. Actual tax validation is the responsibility of the user's accountant. This file contains sensitive financial data. It is recommended to add `_reversa_sdd/_pricing/profile.json` and `_reversa_sdd/_pricing/profile.md` to `.gitignore` before committing.
```

## Exit without changes

If the user cancels before saving:

1. Do not write anything
2. If a backup was created, restore the `.bak` back to `profile.json`
3. Confirm: "Profile kept without changes."

## Final report

Print:

1. Absolute path of `profile.json`, if written
2. Absolute path of `profile.md`, if written
3. Path of the backup, if there was overwrite
4. Next step:
   - if there is an active feature with tasks, suggest `/reversa-pricing-size`
   - otherwise, suggest starting or completing the forward cycle before sizing

End with:

> Type **CONTINUE** to proceed per the suggestion above.
