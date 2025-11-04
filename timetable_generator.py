import tkinter as tk
from tkinter import *
import json
import os
import csv
from datetime import datetime

class TimetableGenerator:
    def __init__(self):
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        self.timetable_data = {}
        
    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Dynamic Timetable Generator")
        self.root.geometry("800x700")
        self.root.configure(background="#1c1c1c")
        
        # Title
        title = tk.Label(self.root, text="Dynamic Timetable Generator", 
                        bg="#1c1c1c", fg="yellow", font=("Verdana", 24, "bold"))
        title.pack(pady=20)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#1c1c1c")
        main_frame.pack(padx=20, pady=20)
        
        # College start time
        tk.Label(main_frame, text="College Start Time:", bg="#1c1c1c", 
                fg="yellow", font=("Verdana", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.start_time_entry = tk.Entry(main_frame, width=10, font=("Verdana", 12))
        self.start_time_entry.insert(0, "09:00")
        self.start_time_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # College end time
        tk.Label(main_frame, text="College End Time:", bg="#1c1c1c", 
                fg="yellow", font=("Verdana", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.end_time_entry = tk.Entry(main_frame, width=10, font=("Verdana", 12))
        self.end_time_entry.insert(0, "16:00")
        self.end_time_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Period duration
        tk.Label(main_frame, text="Period Duration (min):", bg="#1c1c1c", 
                fg="yellow", font=("Verdana", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.period_duration_entry = tk.Entry(main_frame, width=10, font=("Verdana", 12))
        self.period_duration_entry.insert(0, "60")
        self.period_duration_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Short break settings
        tk.Label(main_frame, text="Number of Short Breaks:", bg="#1c1c1c", 
                fg="yellow", font=("Verdana", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.short_break_count_entry = tk.Entry(main_frame, width=10, font=("Verdana", 12))
        self.short_break_count_entry.insert(0, "2")
        self.short_break_count_entry.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(main_frame, text="Short Break Duration (min):", bg="#1c1c1c", 
                fg="yellow", font=("Verdana", 12)).grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.short_break_duration_entry = tk.Entry(main_frame, width=10, font=("Verdana", 12))
        self.short_break_duration_entry.insert(0, "15")
        self.short_break_duration_entry.grid(row=4, column=1, padx=10, pady=5)
        
        # Lunch break settings
        tk.Label(main_frame, text="Lunch Break Start Time:", bg="#1c1c1c", 
                fg="yellow", font=("Verdana", 12)).grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.lunch_start_entry = tk.Entry(main_frame, width=10, font=("Verdana", 12))
        self.lunch_start_entry.insert(0, "12:30")
        self.lunch_start_entry.grid(row=5, column=1, padx=10, pady=5)
        
        tk.Label(main_frame, text="Lunch Break Duration (min):", bg="#1c1c1c", 
                fg="yellow", font=("Verdana", 12)).grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.lunch_duration_entry = tk.Entry(main_frame, width=10, font=("Verdana", 12))
        self.lunch_duration_entry.insert(0, "45")
        self.lunch_duration_entry.grid(row=6, column=1, padx=10, pady=5)
        
        # Subjects input
        tk.Label(main_frame, text="Subjects (comma-separated):", bg="#1c1c1c", 
                fg="yellow", font=("Verdana", 12)).grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.subjects_entry = tk.Entry(main_frame, width=30, font=("Verdana", 12))
        self.subjects_entry.insert(0, "Math,Physics,Chemistry,English,CS,Break")
        self.subjects_entry.grid(row=7, column=1, columnspan=2, padx=10, pady=5)
        
        # Generate button
        generate_btn = tk.Button(main_frame, text="Generate Timetable", 
                               command=self.generate_timetable,
                               bg="#333333", fg="yellow", font=("Verdana", 14, "bold"),
                               bd=5, relief=RIDGE, padx=20, pady=10)
        generate_btn.grid(row=8, column=0, columnspan=3, pady=20)
        
        # Save button
        save_btn = tk.Button(main_frame, text="Save Timetable", 
                           command=self.save_timetable,
                           bg="#333333", fg="yellow", font=("Verdana", 12, "bold"),
                           bd=3, relief=RIDGE, padx=15, pady=5)
        save_btn.grid(row=9, column=0, columnspan=3, pady=10)
        
        # Result text area
        self.result_text = tk.Text(self.root, height=15, width=80, 
                                 bg="#333333", fg="yellow", font=("Verdana", 10))
        self.result_text.pack(pady=20)
        
        self.root.mainloop()
    
    def time_to_minutes(self, time_str):
        """Convert time string to minutes from midnight"""
        hour, minute = map(int, time_str.split(':'))
        return hour * 60 + minute
    
    def minutes_to_time(self, minutes):
        """Convert minutes from midnight to time string"""
        hour = minutes // 60
        minute = minutes % 60
        return f"{hour:02d}:{minute:02d}"
    
    def generate_timetable(self):
        try:
            # Get input values
            start_time = self.start_time_entry.get()
            end_time = self.end_time_entry.get()
            period_duration = int(self.period_duration_entry.get())
            short_break_count = int(self.short_break_count_entry.get())
            short_break_duration = int(self.short_break_duration_entry.get())
            lunch_start = self.lunch_start_entry.get()
            lunch_duration = int(self.lunch_duration_entry.get())
            subjects = [s.strip() for s in self.subjects_entry.get().split(',')]
            
            # Convert times to minutes
            start_minutes = self.time_to_minutes(start_time)
            end_minutes = self.time_to_minutes(end_time)
            lunch_start_minutes = self.time_to_minutes(lunch_start)
            lunch_end_minutes = lunch_start_minutes + lunch_duration
            
            # Clear previous results
            self.result_text.delete(1.0, tk.END)
            self.timetable_data = {}
            
            # Generate timetable for each day
            for day in self.days:
                self.result_text.insert(tk.END, f"\n{'='*50}\n")
                self.result_text.insert(tk.END, f"{day.upper()}\n")
                self.result_text.insert(tk.END, f"{'='*50}\n")
                
                current_time = start_minutes
                period_num = 1
                short_breaks_placed = 0
                day_schedule = []
                
                while current_time < end_minutes:
                    period_start = current_time
                    period_end = current_time + period_duration
                    
                    # Check if this period overlaps with lunch break
                    if period_start < lunch_start_minutes and period_end > lunch_start_minutes:
                        # Add period before lunch
                        if period_start < lunch_start_minutes:
                            subject = subjects[(period_num - 1) % len(subjects)]
                            time_slot = f"{self.minutes_to_time(period_start)} - {self.minutes_to_time(lunch_start_minutes)}"
                            self.result_text.insert(tk.END, f"Period {period_num}: {time_slot} - {subject}\n")
                            day_schedule.append({
                                'period': period_num,
                                'time': time_slot,
                                'subject': subject,
                                'type': 'regular'
                            })
                            period_num += 1
                        
                        # Add lunch break
                        lunch_time_slot = f"{self.minutes_to_time(lunch_start_minutes)} - {self.minutes_to_time(lunch_end_minutes)}"
                        self.result_text.insert(tk.END, f"LUNCH BREAK: {lunch_time_slot}\n")
                        day_schedule.append({
                            'period': 'LUNCH',
                            'time': lunch_time_slot,
                            'subject': 'Lunch Break',
                            'type': 'lunch'
                        })
                        
                        current_time = lunch_end_minutes
                    else:
                        # Regular period
                        subject = subjects[(period_num - 1) % len(subjects)]
                        
                        # Add short breaks if needed
                        if (short_breaks_placed < short_break_count and 
                            period_num > 1 and 
                            current_time < lunch_start_minutes - short_break_duration):
                            
                            # Add short break before this period
                            break_start = current_time
                            break_end = current_time + short_break_duration
                            break_time_slot = f"{self.minutes_to_time(break_start)} - {self.minutes_to_time(break_end)}"
                            self.result_text.insert(tk.END, f"SHORT BREAK: {break_time_slot}\n")
                            day_schedule.append({
                                'period': f'BREAK{short_breaks_placed + 1}',
                                'time': break_time_slot,
                                'subject': 'Short Break',
                                'type': 'short_break'
                            })
                            
                            short_breaks_placed += 1
                            current_time = break_end
                            
                            # Now add the actual period
                            period_start = current_time
                            period_end = current_time + period_duration
                            
                            if period_end <= end_minutes:
                                time_slot = f"{self.minutes_to_time(period_start)} - {self.minutes_to_time(period_end)}"
                                self.result_text.insert(tk.END, f"Period {period_num}: {time_slot} - {subject}\n")
                                day_schedule.append({
                                    'period': period_num,
                                    'time': time_slot,
                                    'subject': subject,
                                    'type': 'regular'
                                })
                                current_time = period_end
                                period_num += 1
                        else:
                            # Normal period without preceding break
                            if period_end <= end_minutes:
                                time_slot = f"{self.minutes_to_time(period_start)} - {self.minutes_to_time(period_end)}"
                                self.result_text.insert(tk.END, f"Period {period_num}: {time_slot} - {subject}\n")
                                day_schedule.append({
                                    'period': period_num,
                                    'time': time_slot,
                                    'subject': subject,
                                    'type': 'regular'
                                })
                                current_time = period_end
                                period_num += 1
                            else:
                                break
                
                self.timetable_data[day] = day_schedule
            
            self.result_text.insert(tk.END, f"\n{'='*50}\n")
            self.result_text.insert(tk.END, "Timetable generated successfully!\n")
            self.result_text.insert(tk.END, "Click 'Save Timetable' to save to file.\n")
            
        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Error generating timetable: {str(e)}\n")
    
    def save_timetable(self):
        if not self.timetable_data:
            self.result_text.insert(tk.END, "\nPlease generate a timetable first!\n")
            return
        
        try:
            # Create timetable directory if it doesn't exist
            timetable_dir = "Timetable"
            if not os.path.exists(timetable_dir):
                os.makedirs(timetable_dir)
            
            # Save as JSON
            json_filename = f"{timetable_dir}/timetable_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(json_filename, 'w') as f:
                json.dump(self.timetable_data, f, indent=4)
            
            # Save as CSV for easy viewing
            csv_filename = f"{timetable_dir}/timetable_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(csv_filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Day', 'Period', 'Time', 'Subject', 'Type'])
                
                for day, schedule in self.timetable_data.items():
                    for period in schedule:
                        writer.writerow([
                            day,
                            period['period'],
                            period['time'],
                            period['subject'],
                            period['type']
                        ])
            
            self.result_text.insert(tk.END, f"\nTimetable saved successfully!\n")
            self.result_text.insert(tk.END, f"JSON: {json_filename}\n")
            self.result_text.insert(tk.END, f"CSV: {csv_filename}\n")
            
        except Exception as e:
            self.result_text.insert(tk.END, f"\nError saving timetable: {str(e)}\n")

def create_timetable_generator():
    generator = TimetableGenerator()
    generator.create_gui()

if __name__ == "__main__":
    create_timetable_generator()