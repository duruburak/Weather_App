########################################################
#---------------- github.com/duruburak ----------------#
########################################################

import tkinter as tk
import customtkinter
from weather_api import (
    CurrentWeather,
    WeatherFiveDays,
    AirQuality,
    location_to_geo_coords,
    requests,
    get_current_weather,
    get_current_weather_details,
    get_current_air_pollution,
    get_current_air_pollution_details,
    get_five_days_weather,
    get_five_days_weather_details,
)


customtkinter.deactivate_automatic_dpi_awareness()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.minsize(750, 500)
        self.maxsize(950, 2000)
        self.geometry("825x790")
        self.title("Weather Information")

        self.five_days_weather_data_widgets: dict = {}

        self.label_font: customtkinter.CTkFont = customtkinter.CTkFont(
            "Montserrat Alternates", 15, "bold"
        )
        self.btn_font: customtkinter.CTkFont = customtkinter.CTkFont(
            "Quicksand", 15, "bold"
        )
        self.date_font: customtkinter.CTkFont = customtkinter.CTkFont(
            "Gruppo", 21, "normal"
        )
        self.time_font: customtkinter.CTkFont = customtkinter.CTkFont(
            "Roboto Mono", 15, "bold"
        )
        self.celsius_font: customtkinter.CTkFont = customtkinter.CTkFont(
            "Quicksand", 17, "normal"
        )
        self.status_font: customtkinter.CTkFont = customtkinter.CTkFont(
            "Bradley Hand ITC", 16, "bold"
        )

        self.master_container = customtkinter.CTkScrollableFrame(
            self, width=1000, fg_color="gray16"
        )
        self.master_container.grid(sticky="nsew")
        self.master_container.grid_columnconfigure(0, weight=1)
        self.master_container.grid_rowconfigure(2, weight=1)

        self.input_location_container = customtkinter.CTkFrame(
            self.master_container, fg_color="transparent", height=20, corner_radius=15
        )
        self.input_location_container.grid(
            row=0, column=0, padx=10, pady=(10, 0), sticky="ew"
        )

        self.input_location_label = customtkinter.CTkLabel(
            self.input_location_container,
            text="Location:",
            text_color="#B799FF",
            font=("Montserrat", 15, "bold"),
        )
        self.input_location_label.pack(side="left", padx=(10, 5), pady=5)

        self.input_location = customtkinter.CTkEntry(
            self.input_location_container,
            width=300,
            placeholder_text="e.g. London, GB",
            placeholder_text_color="#98EECC",
            text_color="#98EECC",
            font=("Kalam", 15, "normal"),
        )
        self.input_location.pack(side="left", padx=(5, 10), pady=5)

        self.btn_get_data = customtkinter.CTkButton(
            self.input_location_container,
            text="Get Data",
            font=self.btn_font,
            command=self.get_data,
        )
        self.btn_get_data.pack(side="left", padx=(5, 10), pady=5, fill="x", expand=True)

        self.current_weather_section = customtkinter.CTkFrame(
            self.master_container, fg_color="transparent"
        )
        self.current_weather_section.grid(
            row=1, column=0, padx=10, pady=(15, 10), sticky="ew"
        )

        self.min_max_master_frame = customtkinter.CTkFrame(
            self.current_weather_section, fg_color="gray14", corner_radius=10
        )
        self.min_max_master_frame.pack(side="left", padx=(5, 10), pady=0)

        self.min_max_labels_frame = customtkinter.CTkFrame(
            self.min_max_master_frame, fg_color="gray14", corner_radius=10
        )
        self.min_max_labels_frame.pack(side="left", padx=(5, 3), pady=5)

        self.min_degrees_label = customtkinter.CTkLabel(
            self.min_max_labels_frame,
            text="Min.",
            text_color="#D4FAFC",
            font=("Montserrat Alternates", 16, "bold"),
        )
        self.min_degrees_label.pack(padx=10, pady=0)

        self.max_degrees_label = customtkinter.CTkLabel(
            self.min_max_labels_frame,
            text="Max.",
            text_color="#820000",
            font=("Montserrat Alternates", 16, "bold"),
        )
        self.max_degrees_label.pack(padx=10, pady=0)

        self.min_max_values_frame = customtkinter.CTkFrame(
            self.min_max_master_frame, fg_color="gray14", corner_radius=10
        )
        self.min_max_values_frame.pack(side="left", padx=(3, 5), pady=5)

        self.min_degrees = customtkinter.CTkLabel(
            self.min_max_values_frame,
            text="21.5°C",
            text_color="#F1F6F9",
            font=("Montserrat Alternates", 15, "normal"),
        )
        self.min_degrees.pack(padx=10, pady=0)

        self.max_degrees = customtkinter.CTkLabel(
            self.min_max_values_frame,
            text="23.8°C",
            text_color="#F1F6F9",
            font=("Montserrat Alternates", 15, "normal"),
        )
        self.max_degrees.pack(padx=10, pady=0)

        self.current_degrees_frame = customtkinter.CTkFrame(
            self.current_weather_section, fg_color="gray14", corner_radius=10
        )
        self.current_degrees_frame.pack(side="left", padx=(5, 10), pady=1)

        self.current_degrees_label = customtkinter.CTkLabel(
            self.current_degrees_frame,
            text="Current Temp.",
            text_color="#00C4FF",
            font=self.label_font,
        )
        self.current_degrees_label.pack(padx=10, pady=(5, 1))

        self.current_degrees = customtkinter.CTkLabel(
            self.current_degrees_frame,
            text="",
            text_color="#FFDEDE",
            font=("Quicksand", 16, "normal"),
        )
        self.current_degrees.pack(padx=10, pady=(1, 5))

        self.feels_like_frame = customtkinter.CTkFrame(
            self.current_weather_section, fg_color="gray14", corner_radius=10
        )
        self.feels_like_frame.pack(side="left", padx=(5, 10), pady=1)

        self.feels_like_label = customtkinter.CTkLabel(
            self.feels_like_frame,
            text="Feels like",
            text_color="#D0F5BE",
            font=self.label_font,
        )
        self.feels_like_label.pack(padx=10, pady=(5, 1))

        self.feels_like = customtkinter.CTkLabel(
            self.feels_like_frame,
            text="",
            text_color="#FFDEDE",
            font=("Quicksand", 16, "normal"),
        )
        self.feels_like.pack(padx=10, pady=(1, 5))

        self.humidity_frame = customtkinter.CTkFrame(
            self.current_weather_section, fg_color="gray14", corner_radius=10
        )
        self.humidity_frame.pack(side="left", padx=(5, 10), pady=1)

        self.humidity_label = customtkinter.CTkLabel(
            self.humidity_frame,
            text="Humidity",
            text_color="#8B1874",
            font=self.label_font,
        )
        self.humidity_label.pack(padx=10, pady=(5, 1))

        self.humidity = customtkinter.CTkLabel(
            self.humidity_frame,
            text="",
            text_color="#FFDEDE",
            font=("Quicksand", 16, "normal"),
        )
        self.humidity.pack(padx=10, pady=(1, 5))

        self.wind_speed_frame = customtkinter.CTkFrame(
            self.current_weather_section, fg_color="gray14", corner_radius=10
        )
        self.wind_speed_frame.pack(side="left", padx=(5, 10), pady=1)

        self.wind_speed_label = customtkinter.CTkLabel(
            self.wind_speed_frame,
            text="Wind",
            text_color="#F6FA70",
            font=self.label_font,
        )
        self.wind_speed_label.pack(padx=10, pady=(5, 1))

        self.wind_speed = customtkinter.CTkLabel(
            self.wind_speed_frame,
            text="",
            text_color="#FFDEDE",
            font=("Quicksand", 16, "normal"),
        )
        self.wind_speed.pack(padx=10, pady=(1, 5))

        self.air_pollution_frame = customtkinter.CTkFrame(
            self.current_weather_section, fg_color="gray14", corner_radius=10
        )
        self.air_pollution_frame.pack(side="left", padx=(5, 10), pady=1)

        self.air_pollution_label = customtkinter.CTkLabel(
            self.air_pollution_frame,
            text="Air Pollution",
            text_color="#643843",
            font=self.label_font,
        )
        self.air_pollution_label.pack(padx=10, pady=(5, 1))

        self.air_pollution_score = customtkinter.CTkLabel(
            self.air_pollution_frame,
            text="",
            text_color="#FFDEDE",
            font=("Quicksand", 16, "normal"),
        )
        self.air_pollution_score.pack(padx=10, pady=(1, 5))

        self.five_days_weather_container = customtkinter.CTkFrame(
            self.master_container, fg_color="#4C0033", corner_radius=10
        )
        self.five_days_weather_container.grid(
            row=2, column=0, padx=10, pady=(0, 10), sticky="nsew"
        )
        self.five_days_weather_container.grid_columnconfigure((0, 1), weight=1)
        self.five_days_weather_container.grid_rowconfigure(1, weight=1)

        self.five_days_weather_label = customtkinter.CTkLabel(
            self.five_days_weather_container,
            text="5 Days Weather:",
            text_color="#F9F5F6",
            font=self.label_font,
        )
        self.five_days_weather_label.grid(
            row=0, column=0, padx=(15, 5), pady=(10, 5), sticky="nsw"
        )

        self.data_location = customtkinter.CTkLabel(
            self.five_days_weather_container,
            text="",
            text_color="#98EECC",
            font=self.label_font,
        )
        self.data_location.grid(
            row=0, column=1, padx=5, pady=(10, 5), sticky="w"
        )

        self.frame_five_days_weather_results = customtkinter.CTkScrollableFrame(
            self.five_days_weather_container, height=self.five_days_weather_container.winfo_screenheight()*0.6
        )
        self.frame_five_days_weather_results.grid(
            row=1, column=0, columnspan=2, padx=15, pady=(5, 10), sticky="nsew"
        )

    def get_data(self):
        city_name: str = self.input_location.get().strip()

        try:
            self.fetch_current_weather(city_name)
            self.fetch_air_pollution(city_name)
            self.fetch_five_days_weather_data(city_name)

        except (KeyError, IndexError, requests.exceptions.Timeout):
            tk.messagebox.showerror(
                "Request not found",
                "Please check city name or wait for a while before you request again.",
            )

    def fetch_five_days_weather_data(self, city_name):
        user_city: str = city_name

        # Get the current weather details
        current_weather: dict = get_five_days_weather(user_city)
        weather_details: list[WeatherFiveDays] = get_five_days_weather_details(
            current_weather
        )
        # Get the current days
        dfmt: str = "%Y/%m/%d"
        days: list[str] = sorted({f"{date.date:{dfmt}}" for date in weather_details})

        try:
            for widget in self.frame_five_days_weather_results.winfo_children():
                widget.destroy()
        except Exception:
            pass

        self.container_five_days_weather_data_ = customtkinter.CTkFrame(
            self.frame_five_days_weather_results,
            height=0,
            fg_color="gray14",
            bg_color="transparent",
            corner_radius=20,
        )
        self.container_five_days_weather_data_.pack(padx=5, pady=5, anchor="center")

        for day_index, day in enumerate(days):
            date_widget_name = f"five_days_weather_data_{day_index}_date"
            horizontal_line_widget_name = f"horizontal_line_{day_index}_five_days"

            self.five_days_weather_data_widgets[
                date_widget_name
            ] = customtkinter.CTkLabel(
                self.container_five_days_weather_data_,
                height=0,
                text=day,
                text_color="#E8A9A9",
                font=self.date_font,
                fg_color="transparent",
            )
            self.five_days_weather_data_widgets[date_widget_name].pack(
                padx=15, pady=5, anchor="w"
            )

            self.five_days_weather_data_widgets[
                horizontal_line_widget_name
            ] = customtkinter.CTkFrame(
                self.container_five_days_weather_data_,
                height=2,
                width=0,
                fg_color="black",
            )
            self.five_days_weather_data_widgets[horizontal_line_widget_name].pack(
                padx=10, fill="x"
            )

            # Group the weather data by date to make it easier to read
            grouped: list[WeatherFiveDays] = [
                current
                for current in weather_details
                if f"{current.date:{dfmt}}" == day
            ]
            for hour_index, data in enumerate(grouped):
                frame_widget_name = (
                    f"frame_five_days_weather_data{day_index}-{hour_index}"
                )
                time_widget_name = (
                    f"five_days_weather_data{day_index}-{hour_index}_time"
                )
                vertical_line_widget_name = (
                    f"vertical_line_five_days{day_index}-{hour_index}"
                )
                celsius_widget_name = (
                    f"five_days_weather_data{day_index}-{hour_index}_celsius"
                )
                status_widget_name = (
                    f"five_days_weather_data{day_index}-{hour_index}_status"
                )

                data = str(data).split()

                self.five_days_weather_data_widgets[
                    frame_widget_name
                ] = customtkinter.CTkFrame(
                    self.container_five_days_weather_data_,
                    height=0,
                    fg_color="transparent",
                    corner_radius=30,
                )
                self.five_days_weather_data_widgets[frame_widget_name].pack(
                    padx=5, pady=5, anchor="w"
                )

                self.five_days_weather_data_widgets[
                    time_widget_name
                ] = customtkinter.CTkLabel(
                    self.five_days_weather_data_widgets[frame_widget_name],
                    height=0,
                    text=data[0].replace("[", "").replace("]", ""),
                    text_color="#FF0060",
                    font=self.time_font,
                    fg_color="transparent",
                )
                self.five_days_weather_data_widgets[time_widget_name].pack(
                    side="left", padx=(10, 4), pady=5, anchor="center"
                )

                self.five_days_weather_data_widgets[
                    vertical_line_widget_name
                ] = customtkinter.CTkFrame(
                    self.five_days_weather_data_widgets[frame_widget_name],
                    width=2,
                    height=0,
                    fg_color="black",
                )
                self.five_days_weather_data_widgets[vertical_line_widget_name].pack(
                    side="left", padx=(4, 5), pady=5, fill="y", expand=False
                )

                self.five_days_weather_data_widgets[
                    celsius_widget_name
                ] = customtkinter.CTkLabel(
                    self.five_days_weather_data_widgets[frame_widget_name],
                    height=0,
                    text=data[1],
                    justify="center",
                    font=self.celsius_font,
                    fg_color="transparent",
                )
                self.five_days_weather_data_widgets[celsius_widget_name].pack(
                    side="left", padx=10, pady=(2, 5), anchor="center"
                )

                self.five_days_weather_data_widgets[
                    status_widget_name
                ] = customtkinter.CTkLabel(
                    self.five_days_weather_data_widgets[frame_widget_name],
                    height=0,
                    text=(
                        (" ".join(data[2:])).replace("(", "").replace(")", "")
                    ).capitalize(),
                    text_color="#B799FF",
                    justify="center",
                    font=("Jokerman", 18, "normal"),
                    fg_color="transparent",
                )
                self.five_days_weather_data_widgets[status_widget_name].pack(
                    side="left", padx=(10, 15), pady=5, anchor="center"
                )

    def fetch_current_weather(self, city_name):
        user_city: str = city_name

        # Get the current weather details
        current_weather: dict = get_current_weather(user_city)
        weather_details: list[CurrentWeather] = get_current_weather_details(
            current_weather
        )
        parsed_weather_details: list = str(weather_details).split("-")
        self.current_degrees.configure(text=parsed_weather_details[0])
        self.min_degrees.configure(text=parsed_weather_details[1])
        self.max_degrees.configure(text=parsed_weather_details[2])
        self.feels_like.configure(text=parsed_weather_details[3])
        self.humidity.configure(text=parsed_weather_details[4])
        self.wind_speed.configure(text=parsed_weather_details[5])


    def fetch_air_pollution(self, city_name):
        user_city: str = city_name

        # Get the current weather details
        geo_coordinates: list = location_to_geo_coords(user_city)
        pollution_data: dict = get_current_air_pollution(
            geo_coordinates["lat"], geo_coordinates["lon"]
        )
        pollution_details: AirQuality = get_current_air_pollution_details(
            pollution_data
        )

        self.data_location.configure(text=f'{geo_coordinates["name"]} - {geo_coordinates["country"]} [{geo_coordinates["lat"]:.5f}/{geo_coordinates["lon"]:.5f}]')
        self.air_pollution_score.configure(text=pollution_details)



if __name__ == "__main__":
    app = App()
    app.mainloop()
