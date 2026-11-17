import os
import tkinter as tk
from pathlib import Path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class StatsPage:
    def __init__(self, app):
        self.app = app

    def __getattr__(self, name):
        return getattr(self.app, name)

    def show_stats_screen(self):
        self.clear_content()
        self.crime_stats = self.calculate_crime_statistics()

        tk.Frame(self.scrollable_frame, bg=self.bg_gradient_mid, height=10).pack()
        tk.Label(self.scrollable_frame, text="Crime Statistics", font=self.font_title,
                 bg=self.bg_gradient_mid, fg=self.text_bright
                 ).pack(padx=25, pady=15, anchor=tk.W)

        for category, score in self.crime_stats.items():
            self.create_premium_stat_card(category, score)

        self.create_risk_guide()

        shadow = tk.Frame(self.scrollable_frame, bg="#000000")
        shadow.pack(fill=tk.X, padx=25, pady=25)
        tk.Button(shadow, text="📈 View Data Visualizations", font=("Arial", 16, "bold"),
                  bg=self.accent_cyan, fg="white", activebackground="#00b8d4",
                  bd=0, cursor="hand2", command=self.show_matplotlib_visualizations, height=3
                  ).pack(fill=tk.X, padx=2, pady=2)

        shadow_3d = tk.Frame(self.scrollable_frame, bg="#000000")
        shadow_3d.pack(fill=tk.X, padx=25, pady=10)
        tk.Button(shadow_3d, text="View 3D Visualizations", font=("Arial", 16, "bold"),
                  bg=self.accent_purple, fg="white", activebackground="#9333ea",
                  bd=0, cursor="hand2", command=self.show_3d_visualizations, height=3
                  ).pack(fill=tk.X, padx=2, pady=2)

    def create_premium_stat_card(self, category, score):
        formatted_name = category.replace("_", " ").title()
        if score < 3:
            color = self.accent_green
        elif score < 5:
            color = self.accent_orange
        else:
            color = self.accent_pink

        shadow = tk.Frame(self.scrollable_frame, bg="#000000")
        shadow.pack(fill=tk.X, padx=25, pady=10)
        card = tk.Frame(shadow, bg=self.card_dark);
        card.pack(fill=tk.X, padx=2, pady=2)
        inner = tk.Frame(card, bg=self.card_dark);
        inner.pack(fill=tk.X, padx=25, pady=20)

        header_row = tk.Frame(inner, bg=self.card_dark);
        header_row.pack(fill=tk.X)
        tk.Label(header_row, text=formatted_name, font=self.font_subheader,
                 bg=self.card_dark, fg=self.text_bright).pack(side=tk.LEFT)
        tk.Label(header_row, text=f"{score}/10", font=self.font_subheader,
                 bg=self.card_dark, fg=color).pack(side=tk.RIGHT)

        progress_container = tk.Frame(inner, bg=self.bg_medium, height=12)
        progress_container.pack(fill=tk.X, pady=(12, 0))
        progress_fill = tk.Frame(progress_container, bg=color, height=12)
        progress_fill.pack(side=tk.LEFT, fill=tk.Y)
        progress_fill.config(width=int((score / 10) * (self.width - 100)))

    def create_risk_guide(self):
        tk.Label(self.scrollable_frame, text="Risk Assessment Guide",
                 font=self.font_header, bg=self.bg_gradient_mid, fg=self.text_bright
                 ).pack(anchor=tk.W, padx=25, pady=(25, 15))
        risk_levels = [("Safe Zone", "0-3", self.accent_green, ""),
                       ("Moderate Risk", "3-5", self.accent_orange, ""),
                       ("Danger Zone", "5-10", self.accent_pink, "")]
        for level, range_text, color, icon in risk_levels:
            shadow = tk.Frame(self.scrollable_frame, bg="#000000");
            shadow.pack(fill=tk.X, padx=25, pady=8)
            card = tk.Frame(shadow, bg=self.card_dark);
            card.pack(fill=tk.X, padx=2, pady=2)
            tk.Frame(card, bg=color, width=6).pack(side=tk.LEFT, fill=tk.Y)
            content = tk.Frame(card, bg=self.card_dark);
            content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=15)
            tk.Label(content, text=f"{icon} {level}", font=self.font_subheader,
                     bg=self.card_dark, fg=self.text_bright, anchor=tk.W).pack(fill=tk.X)
            tk.Label(content, text=f"Score: {range_text}", font=self.font_body,
                     bg=self.card_dark, fg=self.text_dim, anchor=tk.W).pack(fill=tk.X, pady=(5, 0))

    def show_matplotlib_visualizations(self):
        viz_window = tk.Toplevel(self.root)
        viz_window.title("Data Visualizations")
        viz_window.geometry("950x750")
        viz_window.configure(bg=self.bg_gradient_start)

        header = tk.Frame(viz_window, bg=self.card_dark, height=70)
        header.pack(fill=tk.X);
        header.pack_propagate(False)
        tk.Label(header, text=f"Crime Data Analysis - {self.user_location}",
                 font=self.font_title, bg=self.card_dark, fg=self.text_bright).pack(side=tk.LEFT, padx=25, pady=20)
        tk.Button(header, text="✕", font=("Arial", 22), bg=self.card_dark, fg=self.text_bright,
                  bd=0, cursor="hand2", command=viz_window.destroy
                  ).pack(side=tk.RIGHT, padx=25, pady=20)

        csv_data = self.get_csv_statistics()

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(9.5, 6.8))
        fig.patch.set_facecolor(self.bg_gradient_start)

        # Chart 1: Bar chart - Crime Statistics Overview
        categories = list(self.crime_stats.keys())
        values = list(self.crime_stats.values())
        formatted_categories = [c.replace("_", " ").title() for c in categories]
        colors = [self.accent_pink, self.accent_orange, self.accent_green]
        bars = ax1.bar(formatted_categories, values, color=colors, alpha=0.9, edgecolor='white', linewidth=2)
        ax1.set_ylabel('Score', color='white', fontsize=12, fontweight='bold')
        ax1.set_title('Crime Statistics Overview', color='white', fontsize=14, fontweight='bold', pad=12)
        ax1.set_ylim(0, 10);
        ax1.set_facecolor(self.card_dark);
        ax1.tick_params(colors='white', labelsize=10)
        ax1.grid(axis='y', alpha=0.3, color='white', linestyle='--')
        for bar in bars:
            h = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2., h, f'{h:.1f}', ha='center', va='bottom',
                     color='white', fontweight='bold', fontsize=11)

        # Chart 2: Pie chart - Crime Type Distribution
        crime_type_counts = csv_data['crime_type_counts']
        print(crime_type_counts)
        if crime_type_counts:
            colors_pie = [self.accent_cyan, self.accent_pink, self.accent_purple,
                          self.accent_orange, self.accent_green, self.accent_gold]
            wedges, texts, autotexts = ax2.pie(
                crime_type_counts.values(),
                labels=crime_type_counts.keys(),
                autopct='%1.1f%%',
                colors=colors_pie[:len(crime_type_counts)],
                textprops={'color': 'white', 'fontsize': 9, 'fontweight': 'bold'},
                startangle=90
            )
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
        else:
            ax2.text(0.5, 0.5, 'No Data', ha='center', va='center', color='white', fontsize=14, transform=ax2.transAxes)
        ax2.set_title('Crime Type Distribution', color='white', fontsize=14, fontweight='bold', pad=12)
        ax2.set_facecolor(self.card_dark)

        # Chart 3: Horizontal Bar chart - Crime in City (only user location)
        city_counts = csv_data['city_counts']
        if city_counts and self.user_location in city_counts:
            city = self.user_location
            count = city_counts[city]
            bars = ax3.barh([city], [count], alpha=0.9, edgecolor='white', linewidth=2, color=self.accent_cyan)
            ax3.set_xlabel('Crime Count', color='white', fontsize=12, fontweight='bold')
            ax3.set_title(f'Crime in {self.user_location}', color='white', fontsize=14, fontweight='bold', pad=12)
            ax3.set_facecolor(self.card_dark);
            ax3.tick_params(colors='white', labelsize=10)
            ax3.grid(axis='x', alpha=0.3, color='white', linestyle='--')
            ax3.text(count + 0.1, 0, str(count), va='center', color='white', fontweight='bold', fontsize=10)
        else:
            ax3.text(0.5, 0.5, 'No Data', ha='center', va='center', color='white', fontsize=14, transform=ax3.transAxes)
            ax3.set_facecolor(self.card_dark)

        fig.delaxes(ax4)

        plt.tight_layout(pad=2.5)
        canvas = FigureCanvasTkAgg(fig, master=viz_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    def show_3d_visualizations(self):
        from mpl_toolkits.mplot3d import Axes3D
        import numpy as np

        viz_window = tk.Toplevel(self.root)
        viz_window.title("3D Data Visualizations")
        viz_window.geometry("1000x800")
        viz_window.configure(bg=self.bg_gradient_start)

        header = tk.Frame(viz_window, bg=self.card_dark, height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text=f"3D Crime Data Analysis - {self.user_location}",
            font=self.font_title,
            bg=self.card_dark,
            fg=self.text_bright
        ).pack(side=tk.LEFT, padx=25, pady=20)

        tk.Button(
            header,
            text="✕",
            font=("Arial", 22),
            bg=self.card_dark,
            fg=self.text_bright,
            bd=0,
            cursor="hand2",
            command=viz_window.destroy
        ).pack(side=tk.RIGHT, padx=25, pady=20)

        csv_data = self.get_csv_statistics()

        fig = plt.figure(figsize=(10, 7.5))
        fig.patch.set_facecolor(self.bg_gradient_start)

        # 3D Bar Chart - Crime Statistics by Category
        ax1 = fig.add_subplot(221, projection='3d')
        ax1.set_facecolor(self.card_dark)

        categories = list(self.crime_stats.keys())
        values = list(self.crime_stats.values())
        formatted_categories = [cat.replace("_", " ").title() for cat in categories]

        x_pos = np.arange(len(categories))
        y_pos = np.zeros(len(categories))
        z_pos = np.zeros(len(categories))

        dx = np.ones(len(categories)) * 0.5
        dy = np.ones(len(categories)) * 0.5
        dz = values

        colors_list = [self.accent_pink, self.accent_orange, self.accent_green]

        ax1.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, color=colors_list, alpha=0.8, shade=True)

        ax1.set_xlabel('Categories', color='white', fontsize=10, fontweight='bold')
        ax1.set_ylabel('', color='white')
        ax1.set_zlabel('Score', color='white', fontsize=10, fontweight='bold')
        ax1.set_title('3D Crime Statistics', color='white', fontsize=12, fontweight='bold', pad=15)
        ax1.set_xticks(x_pos + 0.25)
        ax1.set_xticklabels(formatted_categories, fontsize=8, rotation=15)
        ax1.set_zlim(0, 10)
        ax1.tick_params(colors='white', labelsize=8)
        ax1.xaxis.pane.fill = False
        ax1.yaxis.pane.fill = False
        ax1.zaxis.pane.fill = False
        ax1.xaxis.pane.set_edgecolor('white')
        ax1.yaxis.pane.set_edgecolor('white')
        ax1.zaxis.pane.set_edgecolor('white')
        ax1.grid(True, alpha=0.3, color='white')

        # 3D Scatter Plot - Crime Type Distribution
        ax2 = fig.add_subplot(222, projection='3d')
        ax2.set_facecolor(self.card_dark)

        crime_type_counts = csv_data['crime_type_counts']

        if crime_type_counts:
            sorted_crimes = sorted(crime_type_counts.items(), key=lambda x: x[1], reverse=True)[:8]

            x_data = np.arange(len(sorted_crimes))
            y_data = np.random.rand(len(sorted_crimes)) * 5
            z_data = [crime[1] for crime in sorted_crimes]
            sizes = [crime[1] * 50 for crime in sorted_crimes]

            scatter = ax2.scatter(x_data, y_data, z_data, s=sizes, c=z_data,
                                  cmap='plasma', alpha=0.8, edgecolors='white', linewidth=1.5)

            ax2.set_xlabel('Crime Types', color='white', fontsize=10, fontweight='bold')
            ax2.set_ylabel('Random Factor', color='white', fontsize=10, fontweight='bold')
            ax2.set_zlabel('Count', color='white', fontsize=10, fontweight='bold')
            ax2.set_title('3D Crime Type Scatter', color='white', fontsize=12, fontweight='bold', pad=15)
            ax2.tick_params(colors='white', labelsize=8)
            ax2.xaxis.pane.fill = False
            ax2.yaxis.pane.fill = False
            ax2.zaxis.pane.fill = False
            ax2.xaxis.pane.set_edgecolor('white')
            ax2.yaxis.pane.set_edgecolor('white')
            ax2.zaxis.pane.set_edgecolor('white')
            ax2.grid(True, alpha=0.3, color='white')
        else:
            ax2.text2D(0.5, 0.5, 'No Data Available', ha='center', va='center',
                       color='white', fontsize=12, transform=ax2.transAxes)

        # 3D Bar Chart - Age Distribution
        ax3 = fig.add_subplot(224, projection='3d')
        ax3.set_facecolor(self.card_dark)

        age_data = csv_data['victim_age_distribution']

        if age_data and sum(age_data.values()) > 0:
            age_groups = list(age_data.keys())
            age_counts = list(age_data.values())

            x_pos = np.arange(len(age_groups))
            y_pos = np.arange(len(age_groups))
            x_pos, y_pos = np.meshgrid(x_pos, y_pos)
            x_pos = x_pos.flatten()
            y_pos = y_pos.flatten()
            z_pos = np.zeros_like(x_pos)

            dx = np.ones_like(x_pos) * 0.3
            dy = np.ones_like(y_pos) * 0.3
            dz = []
            colors_3d = []

            age_colors = [self.accent_green, self.accent_cyan, self.accent_orange, self.accent_pink]

            for i in range(len(x_pos)):
                age_idx = i % len(age_groups)
                dz.append(age_counts[age_idx])
                colors_3d.append(age_colors[age_idx])

            ax3.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, color=colors_3d, alpha=0.8, shade=True)

            ax3.set_xlabel('Age Groups', color='white', fontsize=10, fontweight='bold')
            ax3.set_ylabel('', color='white')
            ax3.set_zlabel('Count', color='white', fontsize=10, fontweight='bold')
            ax3.set_title('3D Age Distribution', color='white', fontsize=12, fontweight='bold', pad=15)
            ax3.set_xticks(np.arange(len(age_groups)))
            ax3.set_xticklabels(age_groups, fontsize=8)
            ax3.tick_params(colors='white', labelsize=8)
            ax3.xaxis.pane.fill = False
            ax3.yaxis.pane.fill = False
            ax3.zaxis.pane.fill = False
            ax3.xaxis.pane.set_edgecolor('white')
            ax3.yaxis.pane.set_edgecolor('white')
            ax3.zaxis.pane.set_edgecolor('white')
            ax3.grid(True, alpha=0.3, color='white')
        else:
            ax3.text2D(0.5, 0.5, 'No Data Available', ha='center', va='center',
                       color='white', fontsize=12, transform=ax3.transAxes)

        fig.tight_layout(pad=2.0)
        ax3.set_position([0.12, 0.08, 0.76, 0.38])

        canvas = FigureCanvasTkAgg(fig, master=viz_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def get_csv_statistics(self):
        crime_type_counts = {}
        city_counts = {}
        hourly_distribution = {str(i).zfill(2): 0 for i in range(24)}
        victim_age_distribution = {'0-17': 0, '18-30': 0, '31-50': 0, '51+': 0}
        monthly_data = {}
        property_crimes = ["Theft", "Burglary", "Vehicle Theft", "Vandalism", "Arson"]
        violent_crimes = ["Assault", "Robbery", "Domestic Disturbance", "Pickpocketing"]

        try:
            if not os.path.exists(self.reports_csv):
                return {
                    'crime_type_counts': {},
                    'city_counts': {},
                    'hourly_distribution': {},
                    'victim_age_distribution': {},
                    'monthly_trends': {'months': [], 'property': [], 'violent': []}
                }
            import csv
            from datetime import datetime as dt
            with open(self.reports_csv, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    city = row.get('city', 'Unknown')
                    location_desc = row.get('location_description', '')
                    if self.user_location not in city and self.user_location not in location_desc:
                        continue
                    crime_type = row.get('crime_type', 'Unknown')
                    crime_type_counts[crime_type] = crime_type_counts.get(crime_type, 0) + 1
                    city_counts[city] = city_counts.get(city, 0) + 1

                    time_str = row.get('time', '00:00')
                    try:
                        hour = time_str.split(':')[0].zfill(2)
                        if hour in hourly_distribution:
                            hourly_distribution[hour] += 1
                    except:
                        pass

                    try:
                        age = int(row.get('victim_age', 0))
                        if age <= 17:
                            victim_age_distribution['0-17'] += 1
                        elif age <= 30:
                            victim_age_distribution['18-30'] += 1
                        elif age <= 50:
                            victim_age_distribution['31-50'] += 1
                        else:
                            victim_age_distribution['51+'] += 1
                    except:
                        pass

                    date_str = row.get('date', '')
                    if date_str:
                        try:
                            try:
                                date_obj = dt.strptime(date_str, '%Y-%m-%d')
                            except:
                                date_obj = dt.strptime(date_str, '%m/%d/%Y')
                            month_key = date_obj.strftime('%Y-%m')
                            if month_key not in monthly_data:
                                monthly_data[month_key] = {'property': 0, 'violent': 0}
                            if crime_type in property_crimes:
                                monthly_data[month_key]['property'] += 1
                            elif crime_type in violent_crimes:
                                monthly_data[month_key]['violent'] += 1
                        except:
                            pass
            city_counts = dict(sorted(city_counts.items(), key=lambda x: x[1], reverse=True))
            sorted_months = sorted(monthly_data.keys())
            months_display = [__import__('datetime').datetime.strptime(m, '%Y-%m').strftime('%b %y') for m in
                              sorted_months]
            property_counts = [monthly_data[m]['property'] for m in sorted_months]
            violent_counts = [monthly_data[m]['violent'] for m in sorted_months]
            return {
                'crime_type_counts': crime_type_counts,
                'city_counts': city_counts,
                'hourly_distribution': hourly_distribution,
                'victim_age_distribution': victim_age_distribution,
                'monthly_trends': {'months': months_display, 'property': property_counts, 'violent': violent_counts}
            }
        except Exception as e:
            print(f"Error getting CSV statistics: {e}")
            return {
                'crime_type_counts': {},
                'city_counts': {},
                'hourly_distribution': {},
                'victim_age_distribution': {},
                'monthly_trends': {'months': [], 'property': [], 'violent': []}
            }
