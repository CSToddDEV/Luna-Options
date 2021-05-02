from tkinter import *
import LunaOptionsGUIClasses as gui

# Create Tkinter Object
root = Tk()

# Set window size and make it non-resizeable
root.geometry('960x1018')
root.resizable(False, False)

# Set Root Color
bg_color = '#AC71E9'
root.configure(bg=bg_color)

# Call Luna Page Class
luna_pages = []
quit_page = gui.QuitPage(root, bg_color)
luna_pages.append(quit_page)
search_security = gui.SecuritySearch(root, bg_color)
luna_pages.append(search_security)
trend = gui.TrendPage(root, bg_color)
luna_pages.append(trend)
homepage = gui.HomePage(root, bg_color)
luna_pages.append(homepage)

# Update init
for page in luna_pages:
    page.homepage, page.quit_page, page.security_search, page.trend_window = homepage, quit_page, search_security, trend

# Run object on loop
root.mainloop()