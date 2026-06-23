# WiFi Heatmap Generator

A Python tool that measures WiFi signal strength throughout your home or office and generates reports to help identify weak coverage areas.

---

## Features

- Scan nearby WiFi networks using your wireless adapter
- Record measurements by room or location
- Calculate signal quality percentage
- Identify encryption type
- Export results to CSV and HTML reports
- Compare signal strength between different areas
- Find WiFi dead zones
- Works with 2.4 GHz, 5 GHz, and 6 GHz networks

---

## Example Use Cases

- Determine the best location for an access point
- Identify weak WiFi coverage areas
- Optimize mesh network placement
- Troubleshoot poor wireless performance
- Compare signal strength before and after router upgrades

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/wifi-heatmap-generator.git
cd wifi-heatmap-generator
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Requirements

- Python 3.9+
- Windows or Linux
- Wireless adapter capable of scanning networks

---

## Dependencies

```txt
pywifi
comtypes
```

---

## Running

Start the program:

```bash
python wifi_heatmap.py
```

You will be prompted for a location name:

```text
Location name:
```

Examples:

```text
Bedroom
Office
Living Room
Kitchen
Garage
Basement
Hallway
```

After entering each location, the program scans nearby networks and records signal information.

When finished, type:

```text
done
```

---

## Example

```text
WiFi Heatmap Generator

Location name: Office

Top networks at this location:

HomeWiFi | -48 dBm | 100% | WPA2-PSK
GuestWiFi | -71 dBm | 58% | WPA2-PSK

Location name: Bedroom

Top networks at this location:

HomeWiFi | -62 dBm | 76% | WPA2-PSK

Location name: done
```

---

## Output

Reports are saved in:

```text
wifi_heatmap_reports/
```

Example:

```text
wifi_heatmap_reports/
├── wifi_heatmap_2026-06-23_14-05-12.csv
└── wifi_heatmap_2026-06-23_14-05-12.html
```

---

## CSV Columns

| Column | Description |
|----------|-------------|
| Location | Room or area name |
| SSID | Network name |
| BSSID | Access point MAC address |
| Signal dBm | Signal strength |
| Signal Quality % | Quality rating |
| Frequency MHz | Operating frequency |
| Encryption | Security protocol |
| Scanned At | Timestamp |

---

## Signal Quality Guide

| dBm | Quality |
|------|---------|
| -50 | Excellent |
| -60 | Very Good |
| -70 | Good |
| -80 | Fair |
| -90 | Poor |

---

## Project Structure

```text
wifi-heatmap-generator/
│
├── wifi_heatmap.py
├── requirements.txt
├── README.md
└── wifi_heatmap_reports/
```

---

## Future Improvements

### Visual Heatmap
Generate an actual color heatmap of your house layout:

```
Office      ████████ 95%
Hallway     ███████  80%
Bedroom     █████    65%
Garage      ██       35%
```

### Graph Generation

Create signal-strength charts using:

- matplotlib
- plotly

### GPS Support

Map outdoor coverage using latitude and longitude.

### Historical Comparisons

Compare scans before and after:

- Router upgrades
- Access point relocation
- Mesh system installation

### Interactive Dashboard

Build a Flask web interface with:

- Charts
- Tables
- Historical reports
- Coverage maps

---

## License

Creative Commons BY-NC 4.0
