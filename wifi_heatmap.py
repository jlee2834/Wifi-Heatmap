import pywifi
from pywifi import const
import time
import csv
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path("wifi_heatmap_reports")
SCAN_SECONDS = 4


def clean_ssid(ssid):
    ssid = ssid.strip()
    return ssid if ssid else "<Hidden SSID>"


def get_encryption(akm):
    if const.AKM_TYPE_NONE in akm:
        return "Open"
    if const.AKM_TYPE_WPA3 in akm:
        return "WPA3"
    if const.AKM_TYPE_WPA2PSK in akm:
        return "WPA2-PSK"
    if const.AKM_TYPE_WPAPSK in akm:
        return "WPA-PSK"
    return "Unknown"


def signal_quality(dbm):
    if dbm >= -50:
        return 100
    if dbm <= -100:
        return 0
    return 2 * (dbm + 100)


def scan_wifi(location):
    wifi = pywifi.PyWiFi()
    interfaces = wifi.interfaces()

    if not interfaces:
        raise RuntimeError("No WiFi adapter found.")

    iface = interfaces[0]

    print(f"\nScanning location: {location}")
    iface.scan()
    time.sleep(SCAN_SECONDS)

    results = []

    for network in iface.scan_results():
        ssid = clean_ssid(network.ssid)

        results.append({
            "Location": location,
            "SSID": ssid,
            "BSSID": network.bssid,
            "Signal dBm": network.signal,
            "Signal Quality %": signal_quality(network.signal),
            "Frequency MHz": network.freq,
            "Encryption": get_encryption(network.akm),
            "Scanned At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return sorted(results, key=lambda x: x["Signal dBm"], reverse=True)


def save_csv(all_results, filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=all_results[0].keys())
        writer.writeheader()
        writer.writerows(all_results)


def save_html(all_results, filename):
    rows = ""

    for r in all_results:
        quality = r["Signal Quality %"]

        if quality >= 80:
            rating = "Excellent"
        elif quality >= 60:
            rating = "Good"
        elif quality >= 40:
            rating = "Fair"
        else:
            rating = "Poor"

        rows += f"""
        <tr>
            <td>{r["Location"]}</td>
            <td>{r["SSID"]}</td>
            <td>{r["BSSID"]}</td>
            <td>{r["Signal dBm"]}</td>
            <td>{quality}%</td>
            <td>{rating}</td>
            <td>{r["Frequency MHz"]}</td>
            <td>{r["Encryption"]}</td>
            <td>{r["Scanned At"]}</td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>WiFi Heatmap Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                padding: 30px;
            }}

            h1 {{
                color: #222;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
            }}

            th, td {{
                border: 1px solid #ccc;
                padding: 10px;
                text-align: left;
            }}

            th {{
                background: #222;
                color: white;
            }}
        </style>
    </head>
    <body>
        <h1>WiFi Heatmap Report</h1>
        <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

        <table>
            <tr>
                <th>Location</th>
                <th>SSID</th>
                <th>BSSID</th>
                <th>Signal dBm</th>
                <th>Quality</th>
                <th>Rating</th>
                <th>Frequency MHz</th>
                <th>Encryption</th>
                <th>Scanned At</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """

    with open(filename, "w", encoding="utf-8") as file:
        file.write(html)


def print_location_summary(location_results):
    print("\nTop networks at this location:")

    for net in location_results[:5]:
        print(
            f"{net['SSID']} | "
            f"{net['Signal dBm']} dBm | "
            f"{net['Signal Quality %']}% | "
            f"{net['Encryption']}"
        )


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    all_results = []

    print("WiFi Heatmap Generator")
    print("Enter room/location names as you walk around.")
    print("Type 'done' when finished.\n")

    while True:
        location = input("Location name: ").strip()

        if location.lower() == "done":
            break

        if not location:
            print("Enter a valid location.")
            continue

        results = scan_wifi(location)
        all_results.extend(results)
        print_location_summary(results)

    if not all_results:
        print("No scans were collected.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    csv_file = OUTPUT_DIR / f"wifi_heatmap_{timestamp}.csv"
    html_file = OUTPUT_DIR / f"wifi_heatmap_{timestamp}.html"

    save_csv(all_results, csv_file)
    save_html(all_results, html_file)

    print("\nReports saved:")
    print(f"- {csv_file}")
    print(f"- {html_file}")


if __name__ == "__main__":
    main()
