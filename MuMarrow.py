import tkinter as tk
from tkinter import ttk, messagebox
import tensorflow as tf
import numpy as np

probability_model = tf.keras.models.load_model("model.h5")

# Preset data for demonstration purposes
presets = {
    "Preset 1 (Survived)": [26.394, 6.6, 11.4, 2, 7.94, 19.01323, 23, 20, 10, 435],
    "Preset 2 (Passed Away)": [55.55, 9.5, 36.71, 9.91, 4.979, 5.16, 18, 20, 100000, 365]
}

# Main application class
class MuMarrowApp:
    def __init__(self, master):
        master.title("MuMarrow Survival Prediction App")

        # Creating an internal title for the GUI
        internal_title = ttk.Label(master, text="MuMarrow Survival Prediction", font=('Helvetica', 16, 'bold'))
        internal_title.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        self.labels = [
            "Please enter the donor's age (years):", "Please enter the recipient's age (years):",
            "Please enter the recipient's body mass (kg):", "Please enter the CD34 x1e6 per kilogram:",
            "Please enter the x1e8 per kilogram:", "Please enter the CD3 to CD34 ratio:",
            "Please enter the ANC recovery:", "Please enter the PLT recovery:",
            "Please enter the time to acute GvHD III/IV:", "Please enter an estimated survival time (days):"
        ]

        self.entries = []
        for idx, label_text in enumerate(self.labels):
            label = ttk.Label(master, text=label_text)
            label.grid(row=idx+1, column=0, padx=10, pady=5, sticky="w")  # Note: row indices start at 1 to accommodate title
            entry = ttk.Entry(master)
            entry.grid(row=idx+1, column=1, padx=10, pady=5, sticky="ew")
            self.entries.append(entry)

        # Predict button
        self.predict_button = ttk.Button(master, text="Predict Survival", command=self.predict_survival)
        self.predict_button.grid(row=len(self.labels)+1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Preset buttons
        for idx, (key, values) in enumerate(presets.items(), start=len(self.labels)+2):
            ttk.Button(master, text=key, command=lambda values=values: self.apply_preset(values)).grid(row=idx, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    def predict_survival(self):
        try:
            input_values = [np.double(entry.get()) for entry in self.entries]
            inputs = np.array([input_values], dtype=np.double)
            inputs_tf = tf.convert_to_tensor(inputs, dtype=tf.double)
            prediction = probability_model(inputs_tf)
            prediction_percentage = max(min(abs(prediction.numpy()[0][0] * 100), 100), 0)
            messagebox.showinfo("Prediction Result", f"The patient's chance of survival is around: {prediction_percentage:.2f}%")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate survival chance. Please check the input values. Error: {str(e)}")

    def apply_preset(self, values):
        for entry, value in zip(self.entries, values):
            entry.delete(0, tk.END)
            entry.insert(0, str(value))

root = tk.Tk()
app = MuMarrowApp(root)
root.mainloop()
