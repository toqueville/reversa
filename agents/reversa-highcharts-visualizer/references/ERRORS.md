# Error Handling — Highcharts Visualizer

## Insufficient or empty data

**Symptom:** Chart renders empty or with "No data to display" message.

**Action:** Configure the `noData` module or verify the data before creating the chart:
```javascript
// Include: modules/no-data-to-display.js
lang: { noData: 'No data available to display' },
noData: { style: { fontWeight: 'bold', fontSize: '16px', color: '#666' } }
```

Warn the user:
> "The provided data appears to be empty or was not processed correctly. Could you verify?"

## Incompatible data format

**Symptom:** Console error or chart with NaN/undefined values.

**Action:** Validate data with `scripts/parse_data.py` before embedding. The script automatically converts
numeric strings ("1.234,56" → 1234.56) and dates in multiple formats.

## CDN module not loading

**Symptom:** Error "Highcharts is not defined" or chart type not recognized.

**Action:** Verify script order. The core `highcharts.js` must come first, then the modules.
For Stock/Maps/Gantt, use the respective main script (highstock.js, highmaps.js, highcharts-gantt.js)
**instead of** highcharts.js, not alongside it.

Correct order:
```html
<script src="https://code.highcharts.com/highcharts.js"></script>
<script src="https://code.highcharts.com/highcharts-more.js"></script>
<script src="https://code.highcharts.com/modules/solid-gauge.js"></script>
<script src="https://code.highcharts.com/modules/exporting.js"></script>
<script src="https://code.highcharts.com/modules/accessibility.js"></script>
```

## Chart not responsive

**Symptom:** Chart does not resize with the window, or gets cut off.

**Action:** Do not set a fixed `chart.width`. Use a container with responsive CSS.
Ensure that `chart.reflow` is not disabled.

```javascript
chart: {
    // DO NOT set fixed width/height
    // Let Highcharts adapt to the container
    reflow: true
}
```

## Slow performance with large data

**Symptom:** Chart freezing or taking too long to render with >10,000 points.

**Action:**
1. Include `modules/boost.js`
2. Set `boostThreshold: 5000` on the series
3. Disable animations: `plotOptions: { series: { animation: false } }`
4. Disable markers: `marker: { enabled: false }`
5. Consider aggregating data (downsampling) via `scripts/analyze_data.py`

## Tooltips with incorrect values

**Symptom:** Tooltip shows "undefined" or wrong format.

**Action:** Verify that the data is in the correct format for the chart type.
Use a custom `tooltip.formatter` for full control over the format.

## Illegible colors

**Symptom:** Series or labels with insufficient contrast.

**Action:** Use `Highcharts.getOptions().colors` to check the active palette.
For dark mode, ensure that labels/grid/tick have light colors.
The accessibility module warns about contrast issues.

## CSV with different encoding (UTF-8 BOM, Latin1)

**Symptom:** Special characters (accents) appear as "�" or "Ã©".

**Action:** `scripts/parse_data.py` tries to detect encoding automatically.
If it fails, force encoding:
```bash
python scripts/parse_data.py data.csv --encoding latin1
```

## Excel file with multiple sheets

**Symptom:** Extracted data is from the wrong sheet.

**Action:**
```bash
python scripts/parse_data.py data.xlsx --sheet "Sheet2"
```
