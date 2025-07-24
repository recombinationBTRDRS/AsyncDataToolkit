# 🧭 User Flow — AsyncDataToolkit

This document describes the typical user interaction flow through the AsyncDataToolkit platform.

---

## 1. Start Session

The user opens the app and initiates a data session.

## 2. Upload or Fetch Data

The user chooses to:

- Upload a local file (Excel, CSV, JSON), or
- Provide an external API endpoint to fetch data from.

## 3. Automatic Format Detection

The system detects the data format based on file type or payload structure.

## 4. Preview Columns & Adjust Formatting

The app displays detected columns and allows the user to:

- Rename headers
- Change data types
- Apply formatting options

## 5. Validate Input

AsyncDataToolkit validates structure and content:

- Checks for missing values
- Flags type mismatches or inconsistent fields
- Notifies the user about detected issues

## 6. Decision Point

If validation fails:

- Show errors and request user correction  
  Else:
- Proceed to action selection

## 7. Choose Processing Action(s)

User selects one or more of the following:

- **Analyze** – Generate summaries or statistics
- **Transform** – Clean, filter, or enrich data
- **Visualize** – Create charts or graphical representations

## 8. Execute Actions Asynchronously

The system runs selected tasks in background threads, ensuring responsiveness.

## 9. Display Results

Results (summaries, transformed tables, charts) are shown within the interface.

## 10. Export Output

The user downloads or shares the result:

- File formats: Excel, CSV, JSON
- Or: Send via API POST request

---

This flow ensures users can efficiently inspect, clean, analyze, and export data in a streamlined, asynchronous manner.
