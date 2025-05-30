# WHOOP Integration for Home Assistant

Home Assistant integration for WHOOP. Fetches your latest fitness, sleep, and recovery and exposes them as sensors in Home Assistant.

>[!NOTE]
>This is an unofficial integration.

## Prerequisites

1. **WHOOP Account**
2. **WHOOP Developer Application:**
    * Go to the [WHOOP Developer Dashboard](https://developer-dashboard.whoop.com/) (Log in > Apps > Create  App).
    * **Name:** e.g., "Home Assistant WHOOP"
    * **Contact:** Your email
    * **Privacy Policy:** Has to be a valid URL(e.g. https://dummy.com/privacy)
    * **Redirect URI(s):**
        `https://my.home-assistant.io/redirect/oauth`
    * **Scopes:** Check the scopes you want metrics for. The integration will try to fetch everything regardless of what it has access to.

After creating the app you will be able to see a **Client ID** and **Client Secret** for the app. You will need these during the integration setup in Home Assistant.

>[!NOTE]
>While Privacy Policy isnt listed as a required value I havent manged  to create an app without it, hence the dummy URL.

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
    * Click "DOWNLOAD".
    * Restart Home Assistant when prompted.

 [![Open WHOOP on Home Assistant Community Store (HACS).](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=prankstr&repository=hassio-whoop&category=frontend)

## Configuration

1. Go to **Settings > Devices & Services** in Home Assistant.
2. Click **"+ ADD INTEGRATION"**.
3. Search for and select **"WHOOP"**.
4. A dialog will appear: **"Create Application Credential for WHOOP"**.
    * **Name:** A name for the credentials, e.g. "WHOOP Integration"
    * **Client ID:** Enter the Client ID from your WHOOP Developer App.
    * **Client Secret:** Enter the Client Secret from your WHOOP Developer App.
    * Click **"Create"**.
5. You will be redirected to the WHOOP website to log in and authorize the connection.
6. After authorization, you'll be redirected back to Home Assistant, and the integration will be set up.

## Available Sensors

Once configured, the integration creates sensors for your profile, body measurements, and detailed metrics for each major WHOOP category (Cycle, Recovery, Sleep, Workout). Metadata for each event type is available on its respective "Overview" sensor.

### User Profile

* **User ID**: Your unique WHOOP user identifier.
* **Email**: Your account email.
* **First Name**: Your first name.
* **Last Name**: Your last name.

### Body Measurements

* **Height**: Your height.
* **Weight**: Your weight.
* **Max Heart Rate**: Your calculated maximum heart rate.

### Cycle (Current Day)

* **Cycle Overview**: Provides the current status(scored or not) of your current cycle.
  * *Attributes include:* Cycle ID, Start Time, End Time (if cycle is complete), User ID, Timezone Offset.
* **Day Strain**: Your overall Strain score for the day.
* **Day Kilojoules**: Kilojoules expended during the day.
* **Day Average Heart Rate**: Average heart rate during the day.
* **Day Max Heart Rate**: Maximum heart rate during the day.

### Recovery (Latest)

* **Recovery Overview**: Provides the status of your latest recovery period.
  * *Attributes include:* Cycle ID, Sleep ID, User ID, Created At, Updated At, User Calibrating status.
* **Recovery Score**: Your overall Recovery score.
* **HRV**: Heart Rate Variability.
* **Resting Heart Rate**: Your resting heart rate.
* **SpO2**: Blood oxygen saturation.
* **Skin Temperature**: Skin temperature.

### Sleep (Latest)

* **Sleep Overview**: Provides the status of your latest sleep period.
  * *Attributes include:* Sleep ID, User ID, Created At, Updated At, Start Time, End Time, Timezone Offset, Nap status.
* **Sleep Performance**: Your sleep performance score.
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

### Last Workout

* **Last Workout Overview**: Provides the status of your most recent workout.
  * *Attributes include:* Workout ID, User ID, Created At, Updated At, Start Time, End Time, Timezone Offset, Sport ID, Percent Recorded from score.
* **Last Workout Strain**: Strain score for your most recent workout.
* **Last Workout Average HR**: Average heart rate during the last workout
* **Last Workout Max HR**: Maximum heart rate during the last workout
* **Last Workout Kilojoules**: Kilojoules expended during the last workout.
* **Last Workout Percent Recorded**: Percentage of HR data recorded during the workout.
* **Last Workout Distance**: Distance covered
* **Last Workout Altitude Gain**: Altitude gained
* **Last Workout Altitude Change**: Net altitude change
* **Last Workout Zone 0 Time**: Time in HR Zone 0.
* **Last Workout Zone 1 Time**: Time in HR Zone 1.
* **Last Workout Zone 2 Time**: Time in HR Zone 2.
* **Last Workout Zone 3 Time**: Time in HR Zone 3.
* **Last Workout Zone 4 Time**: Time in HR Zone 4.
* **Last Workout Zone 5 Time**: Time in HR Zone 5.
