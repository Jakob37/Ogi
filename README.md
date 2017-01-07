# Ogi - Efficient time logging for terminal users

The idea with Ogi is to provide a as-simple-as-possible logging utility for people who do a 
large part of their work at a computer with a terminal open. It should be as easy as 
possible to get the data into the system.

Ogi provides efficient logging and a simple way to overview time spent on different
projects, as well as listing performed tasks similarly to the log in Git.

Ogi takes inspiration for its syntax from Git, so if you are an avid Git user,
you should feel right at home.

The next step in Ogi's development will be to develop a sibling application Pogi for
which the purpose is to use Python's fantastic plotting libraries fully to visualize
data logged using Ogi.

## Getting started

To run Ogi you will need to have Python3 installed on your computer. Other than that
there should be no dependencies (let me know if this isn't the case).

Start with cloning this repository.

```
git clone https://github.com/Jakob37/Ogi
```

Next, enter the Ogi directory and run the setup utility.

```
cd Ogi
./ogi.py setup
```

The setup will create a configuration file for you. This can be edited later and
is found at `Ogi/ogi.conf`.

If you plan to use Ogi on multiple computers it is recommended to pick a synced location
for saving your data, such as in Dropbox. Then, assign this as save directory on all
computers where you run Ogi.

## Using Ogi

### Logging time

Time is logged using the `ogi log` command. You must provide a message and a project
when logging.

```
ogi log -m "Descriptive message" -p "my_great_project"
```

In the setup, you specified your default logging unit - whether you work in pomodoras,
or a custom time unit (here called 'blocks'). This can be explicitly specified
when running the command.

```
# Logging a pomodora
ogi log pomo -m "I have worked a whole pomodora" -p my_other_great_project

# Logging a block of custom length
ogi log block -m "This time, I worked an entire block" -p my_great_project
```

You can also log custom length sessions by using the 'session'. When logging a session,
you must specify its duration using the `-u` flag.

```
ogi log session -u 60 -m "I worked for a whole hour today" -p my_great_project
```

### Projects and categories

Each time entry you log need to be assigned to a project. This is done using the `-p` flag.
If the project you specify is unknown, you will be prompted for creating a new project.

```
ogi log -m "Working on new project!" -p "new_project"
new_project does not exist, do you want to create it? [y/N] y
What category? (Empty for uncategorized): 
```

Projects can belong to a category, or be uncategorized. This is useful if you for example
later on want to visualize time spent on work tasks vs. time spent on hobby projects.

You can also create projects explicitly using the `ogi new` command.

```
ogi new project --name my_new_project --category hobby_project
```

### Looking into your data

Now we come to the actual purpose of Ogi. For now, this part is somewhat limited,
but will still prove to be useful. Keep your eyes out for the later Pogi if you
are a sucker for nice plots.

You can list logged entries from today by running `ogi list day`. The 'day' can be replaced by 'week',
'year' or 'date_range'.

```
ogi list day
my_great_project
* Descriptive message (40 minutes)
* This time, I worked an entire block (40 minutes)
* I worked for a whole hour today (60 minutes)
my_other_great_project
* I have worked a whole pomodora (25 minutes)
new_project
* Working on new project! (40 minutes)
```

You can get an overview of your project by adding the '--summary' or '-s' flag.

```
ogi list week --summary
Projects                 Time
------------------------------------
my_great_project         525 minutes
my_other_great_project   230 minutes
new_project              40 minutes
```

Finally, you can list present projects and categories.

```
ogi list projects
my_great_project         work
new_project              hobby
my_other_great_project   hobby

ogi list categories
uncategorized
work
hobby
```




