import tkinter as tk
from tkinter import messagebox, font as tkfont
import tensorflow as tf
import numpy as np

# Load the model using TFSMLayer for inference
model_path = '/model'
probability_model = tf.keras.models.load_model("model.h5")

print("MuMarrow is initializing... Please wait.")

# Function to predict and display results
def predict_survival():
    try:
        # Collect input values, converting them directly to np.double at input
        input_values = [
            np.double(donor_age_entry.get()), np.double(recipient_age_entry.get()), 
            np.double(recipient_body_mass_entry.get()), np.double(CD34_x1e6_per_kg_entry.get()),
            np.double(CD3_x1e8_per_kg_entry.get()), np.double(CD3_to_CD34_ratio_entry.get()),
            np.double(ANC_recovery_entry.get()), np.double(PLT_recovery_entry.get()), 
            np.double(time_to_acute_GvHD_III_IV_entry.get()), np.double(survival_time_entry.get())
        ]
        inputs = np.array([input_values], dtype=np.double)
        
        # Explicitly cast to tf.double when creating the tensor
        inputs_tf = tf.convert_to_tensor(inputs, dtype=tf.double)

        # Predict using the model
        prediction = probability_model(inputs_tf)
        prediction_percentage = max(min(abs(prediction.numpy()[0][0] * 100), 100), 0)

        # Show the result in a messagebox
        messagebox.showinfo("Prediction Result", f"The patient's chance of survival is around: {prediction_percentage:.2f}%")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to calculate survival chance. Please check the input values. Error: {str(e)}")

# Set up the GUI
root = tk.Tk()
root.title("MuMarrow Survival Prediction")

# Define and place widgets
labels = ["Please enter the donor's age (years):", "Please enter the recipient's age (years):",
          "Please enter the recipient's body mass (kg):", "Please enter the CD34 x1e6 per kilogram:",
          "Please enter the x1e8 per kilogram:", "Please enter the CD3 to CD34 ratio:",
          "Please enter the ANC recovery:", "Please enter the PLT recovery:",
          "Please enter the time to acute GvHD III/IV:", "Please enter an estimated survival time (days):"]
entries = []

for idx, label in enumerate(labels):
    label_widget = tk.Label(root, text=label, font=tkfont.Font(family="Helvetica", size=12), anchor="e", padx=10)
    label_widget.grid(row=idx, column=0, sticky="e")
    entry = tk.Entry(root, font=tkfont.Font(family="Helvetica", size=12))
    entry.grid(row=idx, column=1, sticky="w")
    entries.append(entry)

(donor_age_entry, recipient_age_entry, recipient_body_mass_entry, CD34_x1e6_per_kg_entry,
 CD3_x1e8_per_kg_entry, CD3_to_CD34_ratio_entry, ANC_recovery_entry, PLT_recovery_entry,
 time_to_acute_GvHD_III_IV_entry, survival_time_entry) = entries

# Predict button
predict_button = tk.Button(root, text="Predict Survival", command=predict_survival, font=tkfont.Font(family="Helvetica", size=12))
predict_button.grid(row=10, column=0, columnspan=2, pady=10)

# Start the GUI event loop
root.mainloop()
