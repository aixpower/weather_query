
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from weather_api import (
    get_weather_forecast,
    parse_weather_data,
    format_weather_display,
    WeatherAPIError,
    NetworkError,
    APIRateLimitError,
    CityNotFoundError,
    InvalidAPIKeyError
)


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Amap Weather Query System")
        self.root.geometry("700x800")  # Increased height to show all 7 days
        self.root.resizable(True, True)
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        title_label = ttk.Label(
            main_frame,
            text="Amap Weather Query System",
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        ttk.Label(main_frame, text="City Name:", font=("Arial", 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        
        self.city_entry = ttk.Entry(main_frame, font=("Arial", 10))
        self.city_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.city_entry.focus()
        
        self.query_button = ttk.Button(
            main_frame,
            text="Query",
            command=self.on_query,
            width=10
        )
        self.query_button.grid(row=1, column=2, padx=5, pady=5)
        
        self.city_entry.bind("<Return>", lambda e: self.on_query())
        
        ttk.Label(main_frame, text="Query Result:", font=("Arial", 10)).grid(
            row=2, column=0, sticky=tk.W, pady=(15, 5)
        )
        
        self.result_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            state=tk.DISABLED
        )
        self.result_text.grid(
            row=3, column=0, columnspan=3,
            sticky=(tk.W, tk.E, tk.N, tk.S),
            pady=5
        )
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def set_result_text(self, text):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state=tk.DISABLED)
    
    def on_query(self):
        city_name = self.city_entry.get().strip()
        
        if not city_name:
            messagebox.showwarning("Warning", "Please enter a city name!")
            return
        
        if len(city_name) > 50:
            messagebox.showwarning("Warning", "City name too long!")
            return
        
        self.query_button.config(state=tk.DISABLED)
        self.status_var.set("Querying weather for " + city_name + "...")
        
        thread = threading.Thread(target=self.query_weather, args=(city_name,))
        thread.daemon = True
        thread.start()
    
    def query_weather(self, city_name):
        try:
            raw_data = get_weather_forecast(city_name)
            weather_data = parse_weather_data(raw_data)
            display_text = format_weather_display(weather_data)
            
            self.root.after(0, lambda: self.set_result_text(display_text))
            self.root.after(0, lambda: self.status_var.set("Query successful"))
            
        except CityNotFoundError as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e) + "\n\nHint: Please check if the city name is correct"))
            self.root.after(0, lambda: self.status_var.set("Query failed"))
        except NetworkError as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e) + "\n\nHint: Please check your network connection"))
            self.root.after(0, lambda: self.status_var.set("Query failed"))
        except APIRateLimitError as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e) + "\n\nHint: Please try again later"))
            self.root.after(0, lambda: self.status_var.set("Query failed"))
        except InvalidAPIKeyError as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e) + "\n\nHint: Please check API Key configuration"))
            self.root.after(0, lambda: self.status_var.set("Query failed"))
        except WeatherAPIError as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.root.after(0, lambda: self.status_var.set("Query failed"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", "Unknown error: " + str(e)))
            self.root.after(0, lambda: self.status_var.set("Query failed"))
        finally:
            self.root.after(0, lambda: self.query_button.config(state=tk.NORMAL))


def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
