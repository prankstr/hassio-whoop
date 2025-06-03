# WHOOP Integration for Home Assistant

Home Assistant integration for WHOOP. Fetches your latest sleep, recovery, strain and workout metrics and exposes them as sensors in Home Assistant.

![Sensor overview](https://github.com/prankstr/hassio-whoop/blob/main/images/sensors.png?raw=true)

>[!IMPORTANT]
>This is an unofficial integration, I have nothing to do with WHOOP.

## Prerequisites

1. **WHOOP Account**
2. **WHOOP Developer Application:**
    * Go to the [WHOOP Developer Dashboard](https://developer-dashboard.whoop.com/) (Log in > Apps > Create  App).
    * **Name:** e.g., "Home Assistant WHOOP"
    * **Contact:** Your email
    * **Privacy Policy:** Has to be a valid URL(e.g. <https://dummy.com/privacy>)
    * **Redirect URI(s):**
        `https://my.home-assistant.io/redirect/oauth`
    * **Scopes:** Check the scopes you want metrics for. I recommend checking all of them, Profile is required*

After creating the app you will be able to see a **Client ID** and **Client Secret** for the app. You will need these during the integration setup in Home Assistant.

>[!NOTE]
>While Privacy Policy isnt listed as a required value I havent manged  to create an app without it, hence the dummy URL.
>
>*The integration uses your name from the Profile scope, primarily needed for multi-users support but used even for single users right now.

## Installation

This integration can be installed via [HACS](https://hacs.xyz/) (Home Assistant Community Store).

1. **Ensure HACS is installed.**
    * You can find installation instructions [here](https://hacs.xyz/docs/use/download/download/)
2. **Add as a Custom Repository**:
    * In Home Assistant, navigate to HACS in your sidebar.
    * Click the three dots in the top right, select "Custom repositories".
    * **Repository:** `https://github.com/prankstr/hassio-whoop`
    * **Type:** Select "Integration".
    * Click "ADD".
3. **Install from HACS:**
    * Search for "WHOOP" in HACS" or click the button below.
    * Click "DOWNLOAD" in the bottom right corner.
    * Restart Home Assistant

 [![Open WHOOP on Home Assistant Community Store (HACS).](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=prankstr&repository=hassio-whoop&category=frontend)

## Configuration

1. Go to **Settings > Devices & Services** in Home Assistant.
2. Click **"+ ADD INTEGRATION"**.
3. Search for and select **"WHOOP"**.
4. A dialog will appear: **"Add Credentials"**.
    * **Name:** A name for the credentials, e.g. "WHOOP Integration"
    * **Client ID:** Enter the Client ID from your WHOOP Developer App.
    * **Client Secret:** Enter the Client Secret from your WHOOP Developer App.
    * Click **"Create"**.
5. You will be redirected to the WHOOP website to log in and authorize the connection.
6. After authorization, you'll be redirected back to Home Assistant, and the integration will be set up.

## Available Sensors

Only a few key WHOOP metrics enabled by default but many additional detailed sensors are created but as disabled initially. You can enable any sensor you wish to track from the Home Assistant **Settings > Devices & Services > Entities** tab (filter by the WHOOP integration or device).

**Enabled by Default:**

* **Day Strain**: Your overall Strain score for the day.
* **Recovery Score**: Your overall Recovery score.
* **HRV**: Heart Rate Variability.
* **Resting Heart Rate**: Your resting heart rate.
* **Sleep Performance**: Your sleep performance score.
* **Last Workout Strain**: Strain score for your most recent workout.

**Available (Disabled by Default - Enable as Needed):**

### Overview Sensors (Provide Contextual Attributes)

* **Cycle Overview**: Current status of your physiological cycle.
  * *Attributes:* Cycle ID, Start Time, End Time (if cycle is complete), User ID, Timezone Offset, Score State.
* **Recovery Overview**: Status of your latest recovery period.
  * *Attributes:* Cycle ID, Sleep ID, User ID, Created At, Updated At, User Calibrating status, Score State.
* **Sleep Overview**: Status of your latest sleep period.
  * *Attributes:* Sleep ID, User ID, Created At, Updated At, Start Time, End Time, Timezone Offset, Nap status, Score State.
* **Last Workout Overview**: Status of your most recent workout.
  * *Attributes:* Workout ID, User ID, Created At, Updated At, Start Time, End Time, Timezone Offset, Sport ID, Percent Recorded (from score), Score State.

### User Profile

* **User ID**: Your unique WHOOP user identifier.
* **Email**: Your account email.
* **First Name**: Your first name.
* **Last Name**: Your last name.

### Body Measurements

* **Height**: Your height (in meters).
* **Weight**: Your weight (in kilograms).
* **Max Heart Rate**: Your calculated maximum heart rate.

### Additional Cycle Metrics

* **Day Kilojoules**: Kilojoules expended during the current day.
* **Day Average Heart Rate**: Average heart rate during the current day.
* **Day Max Heart Rate**: Maximum heart rate during the current cycle day.

### Additional Recovery Metrics

* **SpO2**: Blood oxygen saturation.
* **Skin Temperature**: Skin temperature.

### Additional Sleep Metrics

* **Sleep Respiratory Rate**: Your average respiratory rate during sleep.
* **Sleep Consistency**: Your sleep consistency score.
* **Sleep Efficiency**: Your sleep efficiency score.
* **Sleep Time in Bed**: Total time spent in bed.
* **Sleep Time Awake**: Total time spent awake during the sleep period.
* **Sleep Time No Data**: Total time during the sleep period with no data.
* **Sleep Light Sleep Time**: Total time in light sleep.
* **Sleep SWS Time** (Slow Wave Sleep): Total time in deep sleep.
* **Sleep REM Sleep Time**: Total time in REM sleep.
* **Sleep Cycles**: Number of sleep cycles.
* **Sleep Disturbances**: Number of sleep disturbances.
* **Sleep Baseline Need**: Your baseline sleep need.
* **Sleep Debt Need**: Additional sleep needed due to sleep debt.
* **Sleep Strain Need**: Additional sleep needed due to recent strain.
* **Sleep Nap Credit**: Reduction in sleep need due to recent naps.

### Additional Last Workout Metrics

* **Last Workout Average HR**: Average heart rate during the last workout.
* **Last Workout Max HR**: Maximum heart rate during the last workout.
* **Last Workout Kilojoules**: Kilojoules expended during the last workout.
* **Last Workout Percent Recorded**: Percentage of HR data recorded during the workout.
* **Last Workout Distance**: Distance covered.
* **Last Workout Altitude Gain**: Altitude gained.
* **Last Workout Altitude Change**: Net altitude change.
* **Last Workout Zone 0 Time**: Time in HR Zone 0.
* **Last Workout Zone 1 Time**: Time in HR Zone 1.
* **Last Workout Zone 2 Time**: Time in HR Zone 2.
* **Last Workout Zone 3 Time**: Time in HR Zone 3.
* **Last Workout Zone 4 Time**: Time in HR Zone 4.
* **Last Workout Zone 5 Time**: Time in HR Zone 5.
