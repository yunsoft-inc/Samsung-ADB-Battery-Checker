# Samsung ADB Battery Checker

<p align="center">
  <!-- App Icon -->
  <img src="img.ico" width="120" alt="App Icon">
</p>

**Samsung ADB Battery Checker** is a Windows GUI application written in Python that uses **Android ADB** to read and display **hidden internal battery information** from Samsung Galaxy devices.

This tool reads data on demand when the user presses the button, and shows both interpreted values and raw system data from ADB.

---

## 📸 Screenshots

### Main Window
![Main UI](assets/screenshot_main.png)

### Manual Calculation Result
![Manual Calculation](assets/screenshot_manual.png)

---

## 🔧 Requirements

1. **Android ADB must be installed**
2. ADB must be added to the **Windows PATH environment variable**
3. USB debugging must be enabled on your Samsung Galaxy device
4. Windows OS

If ADB is not installed or cannot be found, the program will display an error message and close.

---

## 🚀 How to Use

1. Install **ADB** and add it to the system PATH  
2. Connect your Samsung Galaxy phone via USB  
3. Enable **USB debugging** on the phone  
4. Click **Refresh**  
5. The connected device serial number will appear in the dropdown list  
6. Select the desired device  
7. Click **Receive Data From Device**

⚠️ If you press **Receive Data From Device** without selecting a device, an error will appear.

---

## 📊 Field Descriptions

| Field | Description |
|------|-------------|
| **Battery Technology** | Battery chemistry type (e.g. Li-ion) |
| **Battery Level** | Current charge percentage |
| **Battery Voltage** | Current battery voltage (V) |
| **Battery Temperature** | Battery temperature in °C |
| **Charge Counter** | Current stored charge (mAh) |
| **Current Now** | Instant current draw (+ / - mA) |
| **Battery FirstUseDate** | First battery activation date |
| **LLB CAL** | Last battery calibration date |
| **LLB MAN** | Manufacturer calibration date |
| **LLB CURRENT** | Current battery calibration reference |
| **LLB DIFF** | Weeks since last calibration |
| **ASOC** | Actual State of Charge (estimated health %) |
| **BSOH** | Battery State of Health |
| **BATTERY CYCLE** | Total battery charge cycles |

---

## 📑 Raw DATA Panel

The **Raw DATA** section shows the original values directly received from ADB shell commands.

If a value is not supported by your device, it will be displayed as: -1


---

## 🔢 Manual Battery Health Calculation

1. Enter your phone’s **Typical Battery Capacity (mAh)**  
2. Click **Manual Calculation**

The program will estimate battery health.

> This value is an estimate, not an exact measurement.  
> It is most accurate when the battery is around **50%**  
> and the temperature is between **20°C and 30°C**.

---

## 🔓 Open Source

This project is open source and may be modified and used freely for **non-commercial purposes**.

---


