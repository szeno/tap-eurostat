# tap-eurostat

`tap-eurostat` is a Singer tap for EuroStat.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

This custom Singer tap allows users to extract curated datasets from the [Eurostat REST API](https://ec.europa.eu/eurostat/web/json-and-unicode-web-services) in JSON-stat format. It supports a predefined selection of Eurostat dataset codes relevant to key social, environmental, and economic indicators. The tap streamlines integration with Meltano for pipeline development and analytics workflows.

## Supported Datasets

- `gov_10dd_edpt1`: Government deficit and debt  
- `demo_pjan`: Population on 1 January by age and sex  
- `env_air_gge`: Greenhouse gas emissions  
- `lfsa_urgan`: Unemployment by sex and age  
- `ilc_mddd11`: Material deprivation rate  
- `isoc_ci_ifp_iu`: Internet use by individuals  
- `nrg_ind_ren`: Share of renewable energy in industry  
- `migr_imm1ctz`: Immigration by citizenship  
- `nama_10_gdp`: GDP and main aggregates  
- `prc_hicp_aind`: Harmonised Index of Consumer Prices (HICP)

## Installation

Install from GitHub:

```bash
pipx install git+https://github.com/szeno/tap-eurostat.git@main
```

-->

## Configuration

### Accepted Config Options

<!--
Developer TODO: Provide a list of config options accepted by the tap.

This section can be created by copy-pasting the CLI output from:

```
tap-eurostat --about --format=markdown
```
-->

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-eurostat --about
```

### **Important: If `tap-eurostat` is not found**

If the `tap-eurostat` command is not found after installation, you may need to ensure that the directory containing the executable is in your `PATH`. This can happen if the binary is located in a non-standard directory.

To resolve this, you can add the directory to your `PATH`. The location of the binary is typically in a directory like `~/.local/bin`, but it may vary depending on your installation method or environment.

To temporarily add the directory to your `PATH`, run the following command:

```bash
export PATH="/path/to/directory:$PATH"
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.


## Usage

You can easily run `tap-eurostat` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-eurostat --version
tap-eurostat --help
tap-eurostat --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

Prerequisites:

- Python 3.9+
- [uv](https://docs.astral.sh/uv/)

```bash
uv sync
```

### Create and Run Tests

Create tests within the `tests` subfolder and
  then run:

```bash
uv run pytest
```

You can also test the `tap-eurostat` CLI interface directly using `uv run`:

```bash
uv run tap-eurostat --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-eurostat
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-eurostat --version

# OR run a test ELT pipeline:
meltano run tap-eurostat target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
