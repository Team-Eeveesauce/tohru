import curses

def main(stdscr):
    print("Starting main function")  # Did we get here?
    curses.curs_set(0)  
    stdscr.clear()
    stdscr.refresh()

    current_site = "EXAMPLE.COM>HOME"

    while True:
        display_mock_content(stdscr, current_site) 
        stdscr.refresh()  # Force screen update
        user_input = get_input(stdscr)

        if user_input.startswith("GOTO"):
            target_page = user_input.split(" ")[1]
            current_site = "EXAMPLE.COM>" + target_page  
        else:
            display_message(stdscr, "Invalid command")
        
        time.sleep(1)  # Pause for 1 second


def display_mock_content(stdscr, page):
    print("display_mock_content was called!")  # Check!
    stdscr.addstr(0, 0, f"You are on {page}")
    stdscr.addstr(2, 0, "You can try: GOTO ABOUT or GOTO CONTACT")

def get_input(stdscr):
    stdscr.addstr(5, 0, "> ") 
    return stdscr.getstr(5, 2).decode('utf-8') 

def display_message(stdscr, message):
    stdscr.addstr(6, 0, message)
    stdscr.refresh()

if __name__ == "__main__":
    print("Calling curses.wrapper")  # Did we reach this point?
    curses.wrapper(main)
