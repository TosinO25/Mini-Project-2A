# Mini-Project-2A
# Classification of Accelerometer Data using the Micro:bit

## Project Overview

Your goal is to build a system that can recognize whether a micro:bit is being held steady or shaken using accelerometer data. You'll record motion data from the micro:bit, extract features from the accelerometer signals, and train a classifier to distinguish between these two states. This is a practical introduction to real-time motion classification and hardware data collection.

## Background and Resources

Before starting, familiarize yourself with the micro:bit accelerometer:

1. **Movement Data Logger Tutorial**: Learn how to record accelerometer data
   - https://microbit.org/projects/make-it-code-it/movement-data-logger/

2. **Additional Helpful Resources**:
   - Python Data Logger: https://microbit.org/projects/make-it-code-it/python-data-logger/
   - Sensitive Step Counter: https://microbit.org/projects/make-it-code-it/sensitive-step-counter/
   - User Guide – Data Logging: https://microbit.org/get-started/user-guide/data-logging/

3. **Reference Notebook**: This notebook demonstrates classification techniques
   - https://colab.research.google.com/github/cyneuro/ML_camp/blob/main/camp_logreg_microbit.ipynb

## Project Workflow

### Step 1: Record Accelerometer Data

Your first task is to collect accelerometer data from the micro:bit. You can use either MakeCode or Python.

**Recording Sequence:**
- Hold the micro:bit steady for 5 seconds (labeled as "steady")
- Shake the micro:bit for 5 seconds (labeled as "shaking")
- Hold the micro:bit steady for 5 seconds (labeled as "steady")
- Shake the micro:bit for 5 seconds (labeled as "shaking")

This should give you approximately 20 seconds of data with clear "steady" and "shaking" labels.

**Questions to consider:**
- What sampling rate are you using? (How many acceleration measurements per second?)
- What axes does the micro:bit measure? (x, y, z)
- How will you label the data so you know which parts are "steady" vs "shaking"?

### Step 2: Transfer Data to Your Computer

Choose one of these methods:

**Option A: USB Connection**
- Connect micro:bit via USB
- Use MakeCode data logging to save to CSV
- Or use Python script to read serial data

**Option B: Radio Connection**
- Set up radio communication between micro:bit and PC
- Stream accelerometer data wirelessly
- Receive and save on your computer

**Your task:** Successfully transfer at least one recording session (20 seconds) to your computer. Save it as a CSV file with columns like:
```
time, acceleration_x, acceleration_y, acceleration_z, label
```

### Step 3: Explore Your Data

Before building a classifier, understand what you recorded.

**Load and visualize your data:**
- How many data points did you collect?
- What are the ranges of x, y, z acceleration values?
- Do the "steady" and "shaking" periods look visually different when you plot them?

**Questions to answer:**
- When the micro:bit is steady, what acceleration values do you see? (Hint: think about gravity)
- When the micro:bit is shaking, how do the values change?
- Which axis (x, y, or z) shows the biggest differences between steady and shaking?

### Step 4: Extract Features

Raw acceleration values change too quickly to classify directly. You need to extract features that summarize the motion.

**Common features to try:**
- **Magnitude**: Total acceleration = sqrt(x² + y² + z²)
- **Mean**: Average acceleration in each axis
- **Variance**: How much the signal varies
- **Standard Deviation**: Spread of values around the mean
- **Min/Max**: Minimum and maximum values
- **Range**: Max - Min
- **Correlation**: How different axes relate to each other

**Your task:** Extract features from your data. You might compute features over a time window (e.g., every 1 second).

**Questions:**
- Which features show the biggest difference between "steady" and "shaking"?
- Can you create a simple rule? (e.g., "if variance > X, it's shaking")

### Step 5: Build a Classifier

Train a machine learning model using your extracted features. You can use:
- **Logistic Regression**: Simple, interpretable baseline
- **Random Forest**: More complex, may handle nonlinear patterns
- **SVM**: Support Vector Machine
- **Simple Rule-Based**: If variance > threshold, classify as shaking

**Your task:**
- Split your data into training and testing sets
- Train the classifier
- Evaluate accuracy on test data

**Questions to answer:**
- What accuracy did you achieve?
- Does your model do better than random guessing (50%)?
- Which examples did it get wrong?

### Step 6: Analyze and Improve

Think critically about your results.

**Questions to address in your report:**
1. **What was your classification accuracy?**
   - On training data?
   - On test data?
   - Better than random guessing?

2. **What are potential improvements?**
   - Different features?
   - Different classifiers?
   - More training data?
   - Different time windows for feature extraction?

3. **How could you use this in a real application?**
   - Step counter?
   - Activity recognition?
   - Gesture detection?
   - Motion alarm?

## Environment Setup

**Step 1: Create Virtual Environment**

Using Conda:
```bash
conda create -n microbit_accel python=3.9
conda activate microbit_accel
pip install -r requirements.txt
```

Using Pip:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Step 2: Install Jupyter**
```bash
jupyter notebook
```

## Deliverables

You will submit:

- [ ] **Jupyter Notebook** containing:
  - Data loading and exploration code
  - Feature extraction code with visualizations
  - Classifier implementation (training and testing)
  - Results and accuracy metrics
  - Visualizations (plots of raw data, feature distributions, confusion matrix)
  - Your analysis and answers to the questions

- [ ] **CSV Data File(s)**
  - Your recorded accelerometer data (at least one 20-second recording session)

- [ ] **Brief Report** (1-2 pages) with:
  - Classification accuracy achieved
  - Which features were most useful
  - Suggested improvements
  - Real-world applications

## Micro:bit Setup Quick Reference

**To record data on micro:bit:**

MakeCode blocks:
- Input → Accelerometer → acceleration (mg) x, y, or z
- Input → Accelerometer → strength
- Logic → Create variables to store data
- Serial → Write value to serial

Or Python:
```python
from microbit import accelerometer, display, uart
import time

while True:
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    z = accelerometer.get_z()
    uart.write(f"{x},{y},{z}\n")
    time.sleep(50)  # Sample every 50ms = 20Hz
```

**To transfer data:**
- Via USB: Use Mu editor's serial monitor or extract from device storage
- Via Radio: Write a Python script on PC to receive and save data

## Running on FABRIC

Once your code works locally:
1. Upload your notebook and data to FABRIC
2. Run the same Python/Jupyter code
3. FABRIC is useful if you want to try many parameter combinations or train multiple models

## Next Steps

After completing this project, you'll have learned:
- How to collect data from hardware (micro:bit accelerometer)
- How to extract meaningful features from sensor data
- How to train and evaluate classifiers on real data
- How to debug and improve classification systems
- Practical applications of machine learning in embedded systems
