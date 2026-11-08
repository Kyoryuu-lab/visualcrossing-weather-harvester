<h1>visualcrossing-weather-harvester</h1>
<p>Automated historical meteorological ETL pipeline extracting hourly observations via Visual Crossing API, aggregating diurnal wind metrics, and generating continuous time-series datasets</p>

<h2>Project description</h2>
<p>This project provides an automated data collection and extraction pipeline designed to harvest multi-year historical climate records for municipal monitoring across Ukraine:</p>
<ol>
  <li>
    <dl>
      <dt><b>REST API Integration (Visual Crossing Timeline):</b></dt>
      <dd>Automates authenticated HTTP requests for specific geographical coordinates and date intervals using metric units.</dd>
      <dd>Extracts detailed hourly observation payload structures (ambient temperature, wind velocity).</dd>
    </dl>
  </li>
  <li>
    <dl>
      <dt><b>Diurnal Wind Speed &amp; Temperature Aggregation:</b></dt>
      <dd>Computes representative daily mean wind speeds from 24-hour observation arrays.</dd>
      <dd>Preserves single-decimal precision for temperature and wind metrics.</dd>
    </dl>
  </li>
  <li>
    <dl>
      <dt><b>Standardized Time-Series Serialization:</b></dt>
      <dd>Serializes processed records into whitespace-delimited tabular formats (<code>YYYYMMDD Temp Wind</code>) optimized for numerical modeling and econometric tools.</dd>
      <dd>Aggregates multiple heating seasons (October through April) into contiguous observation logs.</dd>
    </dl>
  </li>
</ol>

<h2>Project files</h2>
<table>
  <tr>
    <th colspan="2">visualcrossing-weather-harvester</th>
  </tr>
  <tr>
    <td>main.py</td>
    <td>Master CLI runner managing credential injection, configuration loading, and ETL execution</td>
  </tr>
  <tr>
    <td>modules/api_client.py</td>
    <td>HTTP client encapsulating the Visual Crossing Timeline REST endpoints with error handling</td>
  </tr>
  <tr>
    <td>modules/data_processor.py</td>
    <td>Data aggregation routines computing daily wind averages and text serialization</td>
  </tr>
  <tr>
    <td>config/targets.json</td>
    <td>Configurable target definitions containing city stations and seasonal date intervals</td>
  </tr>
  <tr>
    <td>.env.example</td>
    <td>Environment variable template for securely storing API authentication credentials</td>
  </tr>
  <tr>
    <td>README.md</td>
    <td>Project documentation and technical specification</td>
  </tr>
  <tr>
    <td>.gitignore</td>
    <td>Exclusion rules for sensitive API credentials (.env), local data dumps, and caches</td>
  </tr>
</table>

<h2>Data Format Specification</h2>
<table>
  <tr>
    <th>Field</th>
    <th>Format</th>
    <th>Example</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><b>Date</b></td>
    <td><code>YYYYMMDD</code></td>
    <td><code>20191001</code></td>
    <td>Calendar date identifier without delimiter characters</td>
  </tr>
  <tr>
    <td><b>Mean Temperature</b></td>
    <td><code>Float (&deg;C)</code></td>
    <td><code>19.1</code></td>
    <td>Daily average ambient air temperature in degrees Celsius</td>
  </tr>
  <tr>
    <td><b>Mean Wind Velocity</b></td>
    <td><code>Float (km/h)</code></td>
    <td><code>12.1</code></td>
    <td>Computed diurnal mean wind velocity across hourly measurements</td>
  </tr>
</table>

<h2>Installation and launch</h2>
<ol>
  <b>
    <li>
      <dl>
        <dt>Clone repository</dt>
        <dd>
          <code>git clone https://github.com/Kyoryuu-lab/visualcrossing-weather-harvester.git</code>
        </dd>
        <dd>
          <code>cd visualcrossing-weather-harvester</code>
        </dd>
      </dl>
    </li>
  </b>
  <b>
    <li>
      <dl>
        <dt>Install dependencies</dt>
        <dd>
          <code>pip install requests</code>
        </dd>
      </dl>
    </li>
  </b>
  <b>
    <li>
      <dl>
        <dt>Configure API credentials &amp; run</dt>
        <dd>Pass the key directly via CLI:</dd>
        <dd>
          <code>python main.py --api-key YOUR_API_KEY</code>
        </dd>
        <dd>Or export to environment: <code>export VISUAL_CROSSING_API_KEY="YOUR_KEY" &amp;&amp; python main.py</code></dd>
      </dl>
    </li>
  </b>
</ol>

<h2>Example of console output (python main.py)</h2>
<samp>
  <p>
    ==============================================================================<br />
    &nbsp;&nbsp;VISUAL CROSSING WEATHER HARVESTER | HISTORICAL ETL PIPELINE<br />
    ==============================================================================<br />
    <br />
    [*] Verarbeite Station: Ізмаїл (5 Zeitintervalle)...<br />
    &nbsp;&nbsp;&nbsp;&nbsp;- Lade Intervall 2019-10-01 bis 2020-04-30...<br />
    &nbsp;&nbsp;&nbsp;&nbsp;- Lade Intervall 2020-10-01 bis 2021-04-30...<br />
    &nbsp;&nbsp;&nbsp;&nbsp;- Lade Intervall 2021-10-01 bis 2022-04-30...<br />
    &nbsp;&nbsp;&nbsp;&nbsp;- Lade Intervall 2022-10-01 bis 2023-04-30...<br />
    &nbsp;&nbsp;&nbsp;&nbsp;- Lade Intervall 2023-10-01 bis 2024-04-30...<br />
    [+] Fertiggestellt: Ізмаїл -&gt; 1065 Datensaetze in 'data/Ізмаїл_weather_data.txt' exportiert.<br />
    <br />
    ==============================================================================<br />
    &nbsp;&nbsp;DATENERFASSUNG ERFOLGREICH BEENDET.<br />
    ==============================================================================<br />
  </p>
