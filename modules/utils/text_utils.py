

ogi_main_text = """
    For further information any of Ogi's commands, run 'ogi command -h'.
    Ogi is used for efficient and terminal based time logging. The data is stored in a SQLite database.
    which preferably can be stored in a synced part of the file system, for example Dropbox for usage
    between different computers.

    Pogi is used to visualize the data logged into Ogi. While Ogi in itself provides some ways to explore
    the logged entries, Pogi is used for creating visualizations and rendering them in HTML pages.

    --- Summary of frequently used Ogi and Pogi commands ---
    ogi
        setup   Launch interactive guide for setting up configuration file and Ogi database
        log     Create a new time entry together with information such as description and duration
        list    Print a list-view of chosen entry type
        new     Explicity create a new instance of an entry type
    pogi
        show    Generate plots and HTML page which is automatically rendered in browser

    --- Usage examples ---
    Log a worked pomodora
        ogi log pomo -m "Description of work" -p project -w type_of_work
    List all types of entries
        ogi list all
    Setup a new configuration file and database
        ogi setup
    """