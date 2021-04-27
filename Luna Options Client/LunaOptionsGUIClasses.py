from tkinter import *
from tkinter import font
from PIL import ImageTk, Image


class LunaPage:
    """
    The base class for the Luna Options GUI
    """
    def __init__(self, root, bg_color):
        self.root = root
        self.homepage = None
        self.quit_page = None
        self.security_search = None
        self.searched_security = None
        self.trend_window = None
        self.report = None
        # Colors
        self.bg_color = bg_color
        self.menu_color = '#8131D3'
        # Manu/Nav Window
        self.menu_window = None
        self.slider = True
        # Create Fonts
        self.title_font = font.Font(family='Courier', weight="bold", size=46)
        self.menu_font = font.Font(family='Courier', weight="bold", size=30)
        self.back_font = font.Font(family='Courier', weight="bold", size=24)
        self.text_font = font.Font(family='Courier', weight="bold", size=18)
        self.choice_font = font.Font(family='Courier', weight="bold", size=14, underline=True)
        self.category_font = font.Font(family='Courier', weight="bold", size=14)
        self.data_font = font.Font(family='Courier', size=14)
        self.button_font = font.Font(family='Courier', weight="bold", size=12)
        self.report_font = font.Font(family='Courier', size=14, weight="bold")

        # Create Frame for raise functionality
        bg_frame = Frame(root, bg=bg_color, height=960, width=880)
        bg_frame.place(relx=0.0, rely=0.0, anchor='nw')
        self.bg_frame = bg_frame

        # Create and Set Title
        Label(bg_frame, text='Luna Options', font=self.title_font, bg=self.bg_color).place(relx=0.5, rely=0.1, anchor='center')

        # Create and Set Luna Symbol
        luna_raw = Image.open('luna-transparent.png')
        luna = ImageTk.PhotoImage(luna_raw)
        luna_label = Label(bg_frame, bg=self.bg_color, image=luna, cursor='hand2')
        luna_label.photo = luna
        luna_label.place(relx=1.0, rely=0.0, anchor='ne')
        # Bind Luna Symbol to Clock event
        luna_label.bind("<Button>", self.slide_menu_logic)

    # Create Sliding Menu
    def slide_menu(self, *args):
        """
        This method will slide the navigation in or or out based on the value of self.slider.  If the value is True it
        will slide the menu out, if it is False it will slide the menu in.
        """
        # Nav Menu Window and Logic
        menu_window = Frame(self.bg_frame, width=252, height=960)
        self.slider = True

        # Navigation Buttons
        # Home Button
        home = Label(menu_window, bg=self.menu_color, text="Home", font=self.menu_font, width=10, height=5,
                     borderwidth=5,
                     relief='solid', cursor='hand2')
        home.place(relx=0.0, rely=0.0, anchor='nw')
        home.bind("<Button>", self.homepage_window_link)

        # Security Button
        security = Label(menu_window, bg=self.menu_color, text="Search a\nSecurity", font=self.menu_font, width=10,
                         height=5, borderwidth=5, relief='solid', cursor='hand2')
        security.place(relx=0.0, rely=0.25, anchor='nw')
        security.bind("<Button>", self.security_search_window_link)

        # Trend Button
        trend = Label(menu_window, bg=self.menu_color, text="Trends and\nReports", font=self.menu_font, width=10,
                      height=5,
                      borderwidth=5, relief='solid', cursor='hand2')
        trend.place(relx=0.0, rely=0.5, anchor='nw')
        trend.bind("<Button>", self.trend_window_link)

        # Quit Button
        quit_button = Label(menu_window, bg=self.menu_color, text="Quit", font=self.menu_font, width=10, height=5,
                     borderwidth=5,
                     relief='solid', cursor='hand2')
        quit_button.place(relx=0.0, rely=0.75, anchor='nw')
        quit_button.bind("<Button>", self.quit_window_link)

        # Back Button
        close_label = Label(menu_window, text='\u279C', bg=self.menu_color, cursor='hand2',
                            font=self.back_font)
        close_label.place(relx=.95, rely=0.005, anchor='ne')
        close_label.bind("<Button>", self.slide_menu_logic)
        self.menu_window = menu_window

    def slide_menu_logic(self, *args):
        """
        This method is the logic for the slide menu
        """
        # Logic to Open Menu
        if self.slider is True:
            self.slide_menu()
            self.menu_window.place(relx=1.0, rely=0.0, anchor='ne')
            self.slider = False
        else:
            self.menu_window.destroy()
            self.slider = True

    def raise_window(self, page):
        """
        Method to raise frame to top of root
        """
        if page is not None:
            if page.searched_security:
                page.searched_security.destroy()
            frame = page.return_frame()
            frame.lift()

    def return_frame(self):
        """
        Returns frame for raise function
        """
        return self.bg_frame

    def quit_window_link(self, *args):
        """
        Links to the quit window
        """
        self.raise_window(self.quit_page)
        if self.menu_window:
            self.menu_window.destroy()

    def homepage_window_link(self, *args):
        """
        Links to the quit window
        """
        self.raise_window(self.homepage)
        if self.menu_window:
            self.menu_window.destroy()

    def security_search_window_link(self, *args):
        """
        Links to the quit window
        """
        self.raise_window(self.security_search)
        if self.menu_window:
            self.menu_window.destroy()

    def trend_window_link(self, *args):
        """
        Links to the quit window
        """
        self.raise_window(self.trend_window)
        if self.menu_window:
            self.menu_window.destroy()
        if self.report:
            self.report.destroy()


class HomePage(LunaPage):
    """
    The Home Page Class for Luna Options
    """
    def __init__(self, root, bg_color):
        super().__init__(root, bg_color)

        explore = Label(self.bg_frame, text="Explore:", font=self.menu_font, bg=self.bg_color)
        explore.place(relx=0.5, rely=0.35, anchor='center')

        security_button = Button(self.bg_frame, width=20, height=1, text='Search a Security', bg='grey',
                                 font=self.text_font, command=self.security_search_window_link)
        security_button.place(relx=0.5, rely=0.45, anchor="center")

        trend_button = Button(self.bg_frame, width=20, height=1, text='Trends & Reports', bg='grey',
                                 font=self.text_font, command=self.trend_window_link)
        trend_button.place(relx=0.5, rely=0.55, anchor="center")


class QuitPage(LunaPage):
    """
    The Quit Page Class for Luna Options
    """
    def __init__(self, root, bg_color):
        super().__init__(root, bg_color)

        quit_button = Button(self.bg_frame, width=20, height=1, text="Quit Luna Options", bg='grey',
                             font=self.text_font, command=self.bg_frame.quit)
        quit_button.place(relx=0.5, rely=0.5, anchor='center')


class SecuritySearch(LunaPage):
    """
    The Security Search Page Class for Luna Options
    """
    def __init__(self, root, bg_color):
        super().__init__(root, bg_color)
        self.suc_rate = 70
        self.exp_win = 2

        search_box = Entry(self.bg_frame, width=15, font=self.text_font)
        search_box.place(relx=0.5, rely=0.4, anchor="ne")
        self. search_box = search_box

        search_button = Button(self.bg_frame, text='Search Ticker', bg='grey', command=self.search_security,
                               font=self.button_font, height=1)
        search_button.place(relx=0.5, rely=0.4, anchor='nw')

    def search_security(self):
        """
        Takes information from teh search box and searches for a specific security
        """
        if self.searched_security:
            self.searched_security.destroy()
        security = self.search_box.get()

        # Logic to communicate with server will go here!
        print(security)
        searched_security = self.build_security_page(security)
        self.searched_security = searched_security

    def build_security_page(self, security_information):
        """
        This method will build the Security Page Frame and populate it
        """
        security_frame = Frame(self.bg_frame, height=800, width=880, bg=self.bg_color)
        security_frame.place(relx=0.0, rely=1.0, anchor="sw")

        # Program and load needed information from API call
        ticker = security_information
        ticker_label = Label(security_frame, text=ticker, bg=self.bg_color, font=self.menu_font)
        ticker_label.place(relx=0.5, rely=0.05, anchor="center")

        company_name = "Place Holder Company Name"
        company_name_label = Label(security_frame, text=company_name, bg=self.bg_color, font=self.text_font)
        company_name_label.place(relx=0.5, rely=0.1, anchor="center")

        updated = "Last Updated: xx/xx/xx at xx:xx PM"
        updated_label = Label(security_frame, text=updated, bg=self.bg_color, font=self.button_font)
        updated_label.place(relx=0.5, rely=0.135, anchor="center")

        sentiment = "Market Sentiment: Neutral"
        sentiment_label = Label(security_frame, text=sentiment, bg=self.bg_color, font=self.text_font)
        sentiment_label.place(relx=0.5, rely=0.25, anchor="center")

        divider = Canvas(security_frame, height=450, bg=self.bg_color, highlightthickness=0,)
        divider.place(relx=0.49, rely=1.0, anchor="sw")
        divider.create_line(0, 0, 0, 450, width=10)

        # Data Labels
        current_field_label = Label(security_frame, text="Current:", bg=self.bg_color, font=self.category_font)
        current_field_label.place(relx=0.015, rely=0.43, anchor="nw")
        current_value = "$xx"
        current_value_label = Label(security_frame, text=current_value, bg=self.bg_color, font=self.data_font)
        current_value_label.place(relx=0.18, rely=0.43, anchor="nw")

        dh_field_label = Label(security_frame, text="Daily High:", bg=self.bg_color, font=self.category_font)
        dh_field_label.place(relx=0.015, rely=0.51, anchor="nw")
        dh_value = "$xx"
        dh_value_label = Label(security_frame, text=dh_value, bg=self.bg_color, font=self.data_font)
        dh_value_label.place(relx=0.18, rely=0.51, anchor="nw")

        dl_field_label = Label(security_frame, text="Daily Low:", bg=self.bg_color, font=self.category_font)
        dl_field_label.place(relx=0.015, rely=0.59, anchor="nw")
        dl_value = "$xx"
        dl_value_label = Label(security_frame, text=dl_value, bg=self.bg_color, font=self.data_font)
        dl_value_label.place(relx=0.18, rely=0.59, anchor="nw")

        wh_field_label = Label(security_frame, text="Weekly High:", bg=self.bg_color, font=self.category_font)
        wh_field_label.place(relx=0.015, rely=0.67, anchor="nw")
        wh_value = "$xx"
        wh_value_label = Label(security_frame, text=wh_value, bg=self.bg_color, font=self.data_font)
        wh_value_label.place(relx=0.18, rely=0.67, anchor="nw")

        wl_field_label = Label(security_frame, text="Weekly Low:", bg=self.bg_color, font=self.category_font)
        wl_field_label.place(relx=0.015, rely=0.75, anchor="nw")
        wl_value = "$xx"
        wl_value_label = Label(security_frame, text=wl_value, bg=self.bg_color, font=self.data_font)
        wl_value_label.place(relx=0.18, rely=0.75, anchor="nw")

        mh_field_label = Label(security_frame, text="30 Day High:", bg=self.bg_color, font=self.category_font)
        mh_field_label.place(relx=0.015, rely=0.83, anchor="nw")
        mh_value = "$xx"
        mh_value_label = Label(security_frame, text=mh_value, bg=self.bg_color, font=self.data_font)
        mh_value_label.place(relx=0.18, rely=0.83, anchor="nw")

        ml_field_label = Label(security_frame, text="30 Day Low:", bg=self.bg_color, font=self.category_font)
        ml_field_label.place(relx=0.015, rely=0.91, anchor="nw")
        ml_value = "$xx"
        ml_value_label = Label(security_frame, text=ml_value, bg=self.bg_color, font=self.data_font)
        ml_value_label.place(relx=0.18, rely=0.91, anchor="nw")

        vol_field_label = Label(security_frame, text="Daily Volume:", bg=self.bg_color, font=self.category_font)
        vol_field_label.place(relx=0.25, rely=0.43, anchor="nw")
        vol_value = "High"
        vol_value_label = Label(security_frame, text=vol_value, bg=self.bg_color, font=self.data_font)
        vol_value_label.place(relx=0.42, rely=0.43, anchor="nw")

        wvol_field_label = Label(security_frame, text="Daily Volume:", bg=self.bg_color, font=self.category_font)
        wvol_field_label.place(relx=0.25, rely=0.51, anchor="nw")
        wvol_value = "Med"
        wvol_value_label = Label(security_frame, text=wvol_value, bg=self.bg_color, font=self.data_font)
        wvol_value_label.place(relx=0.42, rely=0.51, anchor="nw")

        iv_field_label = Label(security_frame, text="IV Rank:", bg=self.bg_color, font=self.category_font)
        iv_field_label.place(relx=0.25, rely=0.59, anchor="nw")
        iv_value = "120%"
        iv_value_label = Label(security_frame, text=iv_value, bg=self.bg_color, font=self.data_font)
        iv_value_label.place(relx=0.42, rely=0.59, anchor="nw")

        hiv_field_label = Label(security_frame, text="Historic IV:", bg=self.bg_color, font=self.category_font)
        hiv_field_label.place(relx=0.25, rely=0.67, anchor="nw")
        hiv_value = "20%"
        hiv_value_label = Label(security_frame, text=hiv_value, bg=self.bg_color, font=self.data_font)
        hiv_value_label.place(relx=0.42, rely=0.67, anchor="nw")

        opt_field_label = Label(security_frame, text="Option Vol:", bg=self.bg_color, font=self.category_font)
        opt_field_label.place(relx=0.25, rely=0.75, anchor="nw")
        opt_value = "High"
        opt_value_label = Label(security_frame, text=opt_value, bg=self.bg_color, font=self.data_font)
        opt_value_label.place(relx=0.42, rely=0.75, anchor="nw")

        # Option Section
        suc_field_label = Label(security_frame, text="Success Chance:", bg=self.bg_color, font=self.category_font)
        suc_field_label.place(relx=0.51, rely=0.43, anchor="nw")
        suc_70_label = Label(security_frame, text="70%", bg=self.bg_color, font=self.choice_font, fg='blue',
                             cursor='hand2')
        suc_70_label.place(relx=0.72, rely=0.43, anchor="nw")
        suc_75_label = Label(security_frame, text="75%", bg=self.bg_color, font=self.choice_font,
                             fg='blue', cursor='hand2')
        suc_75_label.place(relx=0.79, rely=0.43, anchor="nw")
        suc_80_label = Label(security_frame, text="80%", bg=self.bg_color, font=self.choice_font,
                             fg='blue', cursor='hand2')
        suc_80_label.place(relx=0.86, rely=0.43, anchor="nw")
        suc_85_label = Label(security_frame, text="85%", bg=self.bg_color, font=self.choice_font, fg='blue',
                             cursor='hand2')
        suc_85_label.place(relx=0.93, rely=0.43, anchor="nw")

        exp_field_label = Label(security_frame, text="Time Till Exp.:", bg=self.bg_color, font=self.category_font)
        exp_field_label.place(relx=0.51, rely=0.51, anchor="nw")
        exp_1w_label = Label(security_frame, text="1W", bg=self.bg_color, font=self.choice_font, fg='blue',
                             cursor='hand2')
        exp_1w_label.place(relx=0.72, rely=0.51, anchor="nw")
        exp_2w_label = Label(security_frame, text="2W", bg=self.bg_color, font=self.choice_font,
                             fg='blue', cursor='hand2')
        exp_2w_label.place(relx=0.79, rely=0.51, anchor="nw")
        exp_3w_label = Label(security_frame, text="3W", bg=self.bg_color, font=self.choice_font,
                             fg='blue', cursor='hand2')
        exp_3w_label.place(relx=0.86, rely=0.51, anchor="nw")
        exp_4w_label = Label(security_frame, text="4w", bg=self.bg_color, font=self.choice_font, fg='blue',
                             cursor='hand2')
        exp_4w_label.place(relx=0.93, rely=0.51, anchor="nw")

        statement = "With a success rate of " + str(self.suc_rate) + "% or more, \nexpiration window of " + str(
            self.exp_win) + " weeks or less, \nthe recommended option strategy is:"
        statement_label = Label(security_frame, text=statement, bg=self.bg_color, font=self.data_font)
        statement_label.place(relx=0.50, rely=0.59, anchor="nw")

        # Option Strategy
        rect = Label(security_frame, width=55, height=15, borderwidth=8, relief='solid', bg=self.bg_color)
        rect.place(relx=0.51, rely=0.69, anchor="nw")

        opt_name = "Iron Condor"
        opt_name_label = Label(rect, text=opt_name, bg=self.bg_color, font=self.menu_font)
        opt_name_label.place(relx=0.5, rely=0.125, anchor="center")

        point1_finance = "Sell"
        point1_strat = "Put"
        point1_price = "212.50"
        point1_exp = "xx/xx"
        point1_finacne_label = Label(rect, text=point1_finance, bg=self.bg_color, font=self.data_font)
        point1_strat_label = Label(rect, text=point1_strat, bg=self.bg_color, font=self.data_font)
        point1_price_label = Label(rect, text=point1_price, bg=self.bg_color, font=self.data_font)
        point1_exp_label = Label(rect, text=point1_exp, bg=self.bg_color, font=self.data_font)
        point1_finacne_label.place(relx=0.2, rely=0.4, anchor="center")
        point1_strat_label.place(relx=0.4, rely=0.4, anchor="center")
        point1_price_label.place(relx=0.6, rely=0.4, anchor="center")
        point1_exp_label.place(relx=0.8, rely=0.4, anchor="center")

        point2_finance = "Buy"
        point2_strat = "Put"
        point2_price = "211.00"
        point2_exp = "xx/xx"
        point2_finacne_label = Label(rect, text=point2_finance, bg=self.bg_color, font=self.data_font)
        point2_strat_label = Label(rect, text=point2_strat, bg=self.bg_color, font=self.data_font)
        point2_price_label = Label(rect, text=point2_price, bg=self.bg_color, font=self.data_font)
        point2_exp_label = Label(rect, text=point2_exp, bg=self.bg_color, font=self.data_font)
        point2_finacne_label.place(relx=0.2, rely=0.55, anchor="center")
        point2_strat_label.place(relx=0.4, rely=0.55, anchor="center")
        point2_price_label.place(relx=0.6, rely=0.55, anchor="center")
        point2_exp_label.place(relx=0.8, rely=0.55, anchor="center")

        point3_finance = "Sell"
        point3_strat = "Call"
        point3_price = "245.50"
        point3_exp = "xx/xx"
        point3_finacne_label = Label(rect, text=point3_finance, bg=self.bg_color, font=self.data_font)
        point3_strat_label = Label(rect, text=point3_strat, bg=self.bg_color, font=self.data_font)
        point3_price_label = Label(rect, text=point3_price, bg=self.bg_color, font=self.data_font)
        point3_exp_label = Label(rect, text=point3_exp, bg=self.bg_color, font=self.data_font)
        point3_finacne_label.place(relx=0.2, rely=0.7, anchor="center")
        point3_strat_label.place(relx=0.4, rely=0.7, anchor="center")
        point3_price_label.place(relx=0.6, rely=0.7, anchor="center")
        point3_exp_label.place(relx=0.8, rely=0.7, anchor="center")

        point4_finance = "Buy"
        point4_strat = "Call"
        point4_price = "250.00"
        point4_exp = "xx/xx"
        point4_finacne_label = Label(rect, text=point4_finance, bg=self.bg_color, font=self.data_font)
        point4_strat_label = Label(rect, text=point4_strat, bg=self.bg_color, font=self.data_font)
        point4_price_label = Label(rect, text=point4_price, bg=self.bg_color, font=self.data_font)
        point4_exp_label = Label(rect, text=point4_exp, bg=self.bg_color, font=self.data_font)
        point4_finacne_label.place(relx=0.2, rely=0.85, anchor="center")
        point4_strat_label.place(relx=0.4, rely=0.85, anchor="center")
        point4_price_label.place(relx=0.6, rely=0.85, anchor="center")
        point4_exp_label.place(relx=0.8, rely=0.85, anchor="center")

        return security_frame


class TrendPage(LunaPage):
    """
    The Home Page Class for Luna Options
    """
    def __init__(self, root, bg_color):
        super().__init__(root, bg_color)

        # Buttons for different reports
        trend = Label(self.bg_frame, text="Trends & Reports:", font=self.menu_font, bg=self.bg_color)
        trend.place(relx=0.5, rely=0.35, anchor='center')

        highiv_button = Button(self.bg_frame, width=23, height=1, text='Highest IV Securities', bg='grey',
                                 font=self.text_font, command=self.highest_iv_report)
        highiv_button.place(relx=0.5, rely=0.45, anchor="center")

        highvol_button = Button(self.bg_frame, width=23, height=1, text='Highest Vol Securities', bg='grey',
                                 font=self.text_font, command=self.highest_vol_report)
        highvol_button.place(relx=0.5, rely=0.53, anchor="center")

        winners_button = Button(self.bg_frame, width=23, height=1, text='Daily Winners', bg='grey',
                                font=self.text_font, command=self.daily_winners_report)
        winners_button.place(relx=0.5, rely=0.61, anchor="center")

        losers_button = Button(self.bg_frame, width=23, height=1, text='Daily Losers', bg='grey',
                                font=self.text_font, command=self.daily_losers_report)
        losers_button.place(relx=0.5, rely=0.69, anchor="center")

    # Report Logic
    def create_report(self, type):
        """
        Creates and runs a report based on the requested report
        """
        if type == "IV":
            symbol = "%"
            color = "black"
            title = "Highest Daily IV Securities"
            # Logic to receive list from server
        elif type == "vol":
            symbol = "M"
            color = "black"
            title = "Highest Daily Volume"
            # Logic to receive list from server
        elif type == "win":
            symbol = "%"
            color = "green"
            title = "Daily Winners"
            # Logic to receive list from server
        elif type == "lose":
            symbol = "%"
            color = "red"
            title = "Daily Losers"
            # Logic to receive list from server

        report_window = Frame(self.bg_frame, height=800, width=880, bg=self.bg_color)
        report_window.place(relx=0.5, rely=0.6, anchor="center")
        report_window_label = Label(report_window, width=800, height=880, bg=self.bg_color)
        report_window_label.place(relx=0.0, rely=0.0, anchor='nw')

        title_label = Label(report_window, text=title, font=self.menu_font, bg=self.bg_color)
        title_label.place(relx=0.5, rely=0.2, anchor="center")

        report_data = Frame(report_window, height=740, width=880, bg=self.bg_color)
        report_data.place(relx=0.5, rely=0.6, anchor="center")

        # Populate Table
        data = "xx"
        security = "XYZ"
        i = 1
        for row in range(10):
            for column in range(5):
                info = str(i) + '. ' + security + " " + data + symbol
                Label(report_data, text=info, bg=self.bg_color, fg=color, font=self.report_font).grid(row=row, column=column, padx=10, pady=12)
                i += 1

        self.report = report_window

    def highest_iv_report(self):
        """
        Function for Highest IV Report
        """
        self.create_report("IV")

    def highest_vol_report(self):
        """
        Function for the highest volume report
        """
        self.create_report("vol")

    def daily_winners_report(self):
        """
        Function for the daily winners report
        """
        self.create_report("win")

    def daily_losers_report(self):
        """
        Function for the daily losers report
        """
        self.create_report("lose")
