import os
import sys
import shutil
import rich
from rich.text import Text
from rich.align import Align
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, track, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
import time
from pyfiglet import Figlet
from datetime import datetime

console = Console()
file_list = []
file_ext_list = []

def list_all_files_in_directory(): #IMPLEMENTED ABOVE LIST COMPREHENSION.  NEED TO TEST
    global console
    global file_list
    global file_ext_list

    cwd = os.getcwd() # Get the current working directory and save it to cwd
    file_list =[file for file in os.listdir() if os.path.isfile(file)] # List comprehension that gets all the files in the current directory and saves it to file_list

    console.print(f"Total files found: {len(file_list)}", style = "bold red") #Prints the total number of files found in the directory

    file_ext_list = [] # Create an empty list called file_ext_list
    empty_file_ext_list = [] # Create an empty list called empty_file_ext_list
    
    for file in file_list: # For each file in the file list
        file_ext = os.path.splitext(file)[1] # OS.path is a module that provides a way to work with the file system, splitext is a function that splits the path name into a pair root and extention, file is the file in the file list
        # [1] is the extension of the file
        if file_ext not in file_ext_list: # If the file extension is not in the file extension list.  This way we can avoid duplicates becuase it won't add the file extension to the list if it is already there
            file_ext_list.append(file_ext) # Add the file extension to the file extension list
        if file_ext == "": # If the file extension is empty
            empty_file_ext_list.append(file) # Add the file to the empty file extension list

    console.print("The following files were found in the Downloads folder:\n", style="bold green")
    for file in file_list:
        console.print(file, style="bold green")
    console.print("\n")

    console.print(f"The following file extensions were found in the directory: {file_ext_list}\n", style="bold green") # Print the following file extensions were found in the directory: and then the file extension list

    console.print(f"The following files do not have an extension: {empty_file_ext_list}\n", style="bold red") # Print the following files do not have an extension: and then the empty file extension list

   # log_action("Listed all files in directory", f"Total files found: {len(file_list)}")
    
    return file_list, file_ext_list # Return the file list and the file extension list because we will use them later in the program

def list_all_subdirectories(): #WORKS BUT ALSO RETURNS ALL FILES IN THE DIRECTORY.  NEED TO LIMIT TO DIRECTORIES ONLY
    
    global console
    global file_list

    cwd = os.getcwd()

    subdirectories = [dir for dir in os.listdir(cwd) if os.path.isdir(dir)]

    console.print("The following subdirectories were found in the current directory: ", style="bold green")
    for subdirectory in subdirectories:
        console.print(subdirectory, style="bold green")
    console.print("\n")

    return subdirectories

def list_files_by_type(): #COMPLETE
    global console
    global file_list

    cwd = os.getcwd()
    file_list =[file for file in os.listdir() if os.path.isfile(file)] # List comprehension that gets all the files in the current directory and saves it to file_list
    file_type = Prompt.ask("What type of files would you like to list? Provide the extension (e.g. .zip, .pdf, .exe), or leave blank for all files")
    matching_files = [file for file in file_list if file.endswith(file_type)]
    
    if not matching_files:
        console.print(f"No {file_type} files found.  Exiting file type listing option", style="bold red")
        return
    elif file_type == "":
        console.print(f"Providing an empty file type will list all files without an extension", style = "bold red")
        console.print(f"Total files without an extension found: {len(matching_files)}", style = "bold red")
        console.print(f"Files found: {matching_files}", style = "bold red")
    else:
        console.print(f"Total {file_type} files found: {len(matching_files)}", style="bold red")
        console.print(f"Files found: {matching_files}", style="bold red")

    
    return file_list

def change_directory(): #LISTS FILES AS WELL.  NEED TO LIMIT TO DIRECTORIES ONLY
    
    global console
    global file_list

    cwd = os.getcwd()

    console.print(f"You are currnetly in the directory: {cwd}", style="bold green")
    console.print("This query will show all files and directories in your current directory", style="bold green")
    console.print("The following files and directories are in your current directory: ", style="bold green")
    
    try:
        if len(os.listdir(cwd)) == 0:
            console.print("The current directory is empty", style="bold red")
        else:
            for file in os.listdir(cwd):
                console.print(file, style="bold red")
    except FileNotFoundError:
        console.print("An error occurred while trying to list the files and directories in the current directory", style="bold red")

    user_query = Prompt.ask("Do you want to change the directory?", choices=["yes", "no"])

    if user_query == "no":
        console.print("Exiting out of directory change option", style="bold green")
        return
    else:
        new_directory = Prompt.ask("What is the name of the directory you want to change to?  Only provide the name of the directory, not the full path")

    if os.path.exists(new_directory):
        os.chdir(new_directory)
        console.print(f"Changed directory to {new_directory}", style="bold green")
    else:
        console.print(f"{new_directory} does not exist in the current directory or you have tried to change to a file instead of a directory.", style="bold red")
        user_query = Prompt.ask("Do you want to try again?", choices=["yes", "no"], style="bold green")
        if user_query == "no":
            console.print("Exiting out of directory change option", style="bold green")
            return
        else:
            change_directory()

    return file_list

def create_subdirectory(): #NEED TO CONFIRM THAT THE USER IS CREATING DIRECTORIES ONLY AND NOT FILES
    cwd = os.getcwd()
    console.print(f"These are the available directories within the {cwd} directory: ", style="bold green")
    list_all_subdirectories()
    new_directory = Prompt.ask("What is the name of the new directory you would like to create? Please provide the name of the directory only, not the full path", style="bold green")
    if os.path.exists(new_directory):
        console.print(f"The {new_directory} directory already exists in the current directory", style="bold red")
        prompt = Prompt.ask("Do you want to try again? ", choices=["yes","no"], style = "bold green")
        if prompt == 'no':
            console.print("Exiting out of subdirectory creation option", style = "bold red")
            return
        else:
            create_subdirectory()
    else:
        os.mkdir(new_directory)
        console.print(f"Created {new_directory} directory in the {cwd} directory", style = "bold green")

def delete_subdirectory():
    cwd = os.getcwd()
    console.print(f"These are the available directories within the {cwd} directory: ", style="bold green")
    list_all_subdirectories()
    prompt = Prompt.ask("Do you want to continue with deleting a subdirectory?", choices=["yes","no"], style="bold green")
    if prompt == "no":
        console.print("Exiting out of the subdirectory deletion option", style="bold red")
        return
    else:
        subdirectory_to_delete = Prompt.ask("What is the name of the subdirectory you would like to delete? Please provide the name of the directory only, not the full path", style="bold green")
        if os.path.exists(subdirectory_to_delete):
            console.print(f"Confirm deletion of {subdirectory_to_delete}", style="bold red")
            confirm = Prompt.ask("Yes or No?", choices=['yes','no'], style="bold green")
            if confirm == "no":
                console.print("Exiting out of subdirectory deletion option", style="bold red")
                return
            else:
                shutil.rmtree(subdirectory_to_delete)
                console.print(f"Deleted {subdirectory_to_delete} directory", style="bold red")

def organize_files_by_type():
    global console
    global file_list
    global file_ext_list

    cwd = os.getcwd()

    if file_list == [] or file_ext_list == []:
         file_list = os.listdir(cwd)
         for file in file_list:
            file_ext = os.path.splitext(file)[1]
            if file_ext not in file_ext_list:
                file_ext_list.append(file_ext)

    console.print("The following types of files were found in your Downloads folder: ", style="bold red")
    
    for file_ext in file_ext_list:
        console.print(file_ext, style="bold red")
    
    console.print("Your files will be organized into folders based off of general types - e.g. images, documents, executables, zip files, etc.", style="bold red")
    confirm = Prompt.ask("Are you sure you want to organize your files?", choices=["yes", "no"])
    if confirm == "no":
        console.print("Exiting out of option", style="bold red")
        return
    else:
        console.print("Organizing files...", style="bold red")
        cwd = os.getcwd()
        folders = ["Images", "Documents", "Executables", "Zip_Files", "XLSX_Files", "ISO_Files", "Audio", "Torrent", "Ini_Files", "Programming_Files", "Incomplete_Files"]
        
        # Create folders if they don't exist
        for folder in folders:
            folder_path = os.path.join(cwd, folder)
            if not os.path.exists(folder_path):
                try:
                    os.mkdir(folder_path)
                    console.print(f"Created {folder} directory...")
                except OSError as e:
                    console.print(f"Error creating {folder} directory: {e}", style="bold red")
                    continue
        
        # Track failed moves to report at the end
        failed_moves = []
        
        for file in file_list:
            if not os.path.isfile(file):
                continue
                
            try:
                target_folder = None
                if file.endswith((".jpg", ".jpeg", ".png", ".gif")):
                    target_folder = "Images"
                elif file.endswith((".doc", ".docx", ".pdf", ".txt")):
                    target_folder = "Documents"
                elif file.endswith((".exe", ".msi", ".bin", ".bat")):
                    target_folder = "Executables"
                elif file.endswith((".zip", ".tar", ".gz", ".7z", ".tgz")):
                    target_folder = "Zip_Files"
                elif file.endswith((".xlsx")):
                    target_folder = "XLSX_Files"
                elif file.endswith((".iso")):
                    target_folder = "ISO_Files"
                elif file.endswith((".mp4", ".mp3")):
                    target_folder = "Audio"
                elif file.endswith((".torrent")):
                    target_folder = "Torrent"
                elif file.endswith((".ini")):
                    target_folder = "Ini_Files"
                elif file.endswith((".py", ".java", ".cpp", ".c", ".html", ".css", ".js", ".php", ".sql", ".json")):
                    target_folder = "Programming_Files"
                elif file.endswith((".part")):
                    target_folder = "Incomplete_Files"
                
                if target_folder:
                    target_path = os.path.join(cwd, target_folder)
                    # Check if destination file already exists
                    dest_file = os.path.join(target_path, file)
                    if os.path.exists(dest_file):
                        # Add a number to the filename if it already exists
                        base, ext = os.path.splitext(file)
                        counter = 1
                        while os.path.exists(dest_file):
                            new_name = f"{base}_{counter}{ext}"
                            dest_file = os.path.join(target_path, new_name)
                            counter += 1
                    
                    shutil.move(file, dest_file, copy_function=shutil.copy2)
                else:
                    console.print(f"File {file} does not match any of the current categories", style="bold red")
            
            except (shutil.Error, OSError) as e:
                failed_moves.append((file, str(e)))
                continue
        
        if failed_moves:
            console.print("\nThe following files could not be moved:", style="bold red")
            for file, error in failed_moves:
                console.print(f"- {file}: {error}", style="bold red")
        else:
            console.print("All files have been organized successfully", style="bold red")

        return file_list, file_ext_list

def delete_files_by_type(): #COMPLETED (?) - NEED TO TEST
    global console
    global file_list

    cwd = os.getcwd()
    file_list = os.listdir(cwd) # Gets the list of all files and directories in the current working directory
    file_type = Prompt.ask("What type of files would you like to delete?  Provide one extension (e.g. .zip, .pdf, .exe)")

    matching_files = [file for file in file_list if file.endswith(file_type)]

    if not matching_files:
        console.print(f"No {file_type} files found", style="bold red")
    else:
        confirm = Prompt.ask(f"Are you sure you want to delete {len(matching_files)} {file_type} files?", choices=["yes", "no"])
        if confirm == "no":
            console.print("Exiting out of option", style="bold red")
            return
        else:
            for file in matching_files:
                os.remove(file)
            console.print(f"Deleted {len(matching_files)} {file_type} files", style="bold red")
    
    return file_list

def delete_specific_files(): #TESTED AND COMPLETED!
    global console
    global file_list

    cwd = os.getcwd()

    if file_list == []:
        file_list = os.listdir(cwd)
        #log_action("Refreshed file list", f"Found {len(file_list)} files")
    
    user_file_name_question = Prompt.ask("Do you know the name of the file you want to delete?", choices=["yes", "no"])

    if user_file_name_question == "no":
        log_action("List files requested before deletion")
        list_all_files_in_directory()
    else:
        file_name = Prompt.ask("What is the name of the file you want to delete? Please include the file extension, e.g. file.txt")
        if file_name in file_list:
            confirm = Prompt.ask(f"Are you sure you want to delete {file_name}?", choices=["yes", "no"])
            if confirm == "no":
                log_action("Delete operation cancelled", f"File: {file_name}")
                console.print("Exiting out of option", style="bold red")
                return
            else:
                try:
                    os.remove(file_name)
                   # log_action("File deleted successfully", f"File: {file_name}")
                    console.print(f"Deleted {file_name}", style = "bold red")
                except FileNotFoundError:
                    error_msg = f"{file_name} not found"
                    #log_action("Delete operation failed", error_msg)
                    console.print(error_msg + ". Please check the name of the file and try again", style = "bold red")
        else:
            error_msg = f"{file_name} not found"
            #log_action("Delete operation failed", error_msg)
            console.print(error_msg + ". Please check the name of the file and try again", style = "bold red")

    return file_list
                
def move_specific_files(): #COMPLETED (?) - NEED TO TEST 
    
    global console
    global file_list

    cwd = os.getcwd()

    user_file_name_question = Prompt.ask("Do you know the name of the file you want to move and do you know the directory you want to move it to?", choices=["yes", "no"])

    if user_file_name_question == "no":
        list_all_files_in_directory()
    else:
        file_name = Prompt.ask("What is the name of the file you want to move? Please include the file extension, e.g. file.txt")
        if file_name in file_list:
            new_directory = Prompt.ask("What is the name of the directory you want to move the file to? Only provide the name of the directory, not the full path")
            if os.path.exists(new_directory):
                confirm = Prompt.ask(f"Are you sure you want to move {file_name} to {new_directory}?", choices = ["yes", "no"])
                if confirm == "no":
                    console.print("Exiting out of file movement option", style = "bold red")
                    return
                else:
                    shutil.move(file_name, f"{cwd}/{new_directory}", copy_function = shutil.copy2)
                    console.print(f"Moved {file_name} to {new_directory}", style = "bold red")
            else:
                create_directory = Prompt.ask(f"{new_directory} does not exist.  Do you want to create the directory?", choices = ["yes", "no"])
                if create_directory == "no":
                    console.print("Exiting out of file movement option", style = "bold red")
                    return
                else:
                    os.mkdir(new_directory)
                    console.print(f"Created {new_directory} directory in {cwd}", style = "bold red")
                    shutil.move(file_name, f"{cwd}/{new_directory}", copy_function = shutil.copy2)
                    console.print(f"Moved {file_name} to {new_directory}", style = "bold red")
        else:
            console.print(f"{file_name} not found.  Please check the name of the file and try again.  Exiting out of file movement option", style = "bold red")
            return
    
    return file_list


    cwd = os.getcwd()

def automation(): #USE WATCHDOG TO MONITOR THE DOWNLOADS FOLDER AND ORGANIZE AUTOMATICALLY
    
    global console
    global file_list

    cwd = os.getcwd()
    folders = ["Images", "Documents", "Executables", "Zip_Files", "XLSX_Files", "ISO_Files", "Audio", "Torrent", "Ini_Files", "Programming_Files", "Incomplete_Files"]

    console.print(f"""You have selected the automation option.  The program will run in the background, organize your Downloads folder on a defined interval, and either delete files based off of user defined criteria such as file type, size, or age. 
                                The program will also create a log file that will record all actions taken by the program.  You can choose to stop the program at any time by pressing CTRL + C.  Would you like to continue?""", style="bold green")
    
    console.print(f"The followiong folders will be created in your Downloads folder: ", style="bold green")
    for folder in folders:
        console.print(folder, style="bold green")

    user_query = Prompt.ask("Would you like to continue?", choices=["yes", "no"])

    if user_query == "no":
        console.print("Exiting out of automation option", style="bold red")
        return
    else:
        console.print("Automation is starting...", style="bold green")

        while True:
            pass

def display_welcome_banner(): #TESTED AND COMPLETED
    fig = Figlet(font="slant")
    ascii_art = fig.renderText("Welcome to Zug File Organizer")

    # Create a Rich Text object with no wrapping
    banner_text = Text(ascii_art, style="bold bright_green", no_wrap=True)

    centered_banner = Align.center(banner_text)

    panel = Panel(centered_banner, border_style="bright_blue", title="[bold yellow] --- Welcome Banner --- [/bold yellow]", expand = True)
    console.print(panel)

def display_goodbye_banner(): #TESTED AND COMPLETED
    # Generate ASCII art using pyfiglet with the "slant" font for the goodbye message
    fig = Figlet(font="slant")
    ascii_art = fig.renderText("Goodbye from Zug File Organizer")

    # Create a Rich Text object with no wrapping
    banner_text = Text(ascii_art, style="bold bright_green", no_wrap=True)

    # Center the banner_text within the panel
    centered_banner = Align.center(banner_text)

    # Create the panel with a border and a title
    panel = Panel(
        centered_banner,
        border_style="bright_blue",
        title="[bold yellow] --- Goodbye Banner --- [/bold yellow]",
        expand=True
    )

    # Print the panel to the console
    console.print(panel)

def zug_initial_user_query(): #TESTED AND COMPLETED
    
    name = Prompt.ask("What is the username you are logged in as on your computer? [bold red] *CASE SENSITIVE* [/bold red]")

    # Confirm the username
    confirm = Prompt.ask("Are you sure this is the correct username? [bold red] *CASE SENSITIVE* [/bold red]", choices=["yes", "no"])
    
    while confirm == "no":
        name = Prompt.ask("What is the username you are logged in as on your computer? [bold red] *CASE SENSITIVE* [/bold red]")
        confirm = Prompt.ask("Are you sure this is the correct username? [bold red] *CASE SENSITIVE* [/bold red]", choices=["yes", "no"])

    if name in os.listdir("C:/Users"):
        console.print(f"User {name} found in Users directory", style="bold red")
    else:
        while name not in os.listdir("C:/Users"):
            user_query = Prompt.ask(f"User {name} was not found in the Users directory.  Do you wish to continue?  If so, please provide the correct username", choices=["yes", "no"])
            if user_query == "no":
                console.print("Exiting program", style="bold red")
                sys.exit()
            else:
                name = Prompt.ask("What is the username you are logged in as on your computer? [bold red] *CASE SENSITIVE* [/bold red]")
                confirm = Prompt.ask("Are you sure this is the correct username? [bold red] *CASE SENSITIVE* [/bold red]", choices=["yes","no"])
    
    # Change directory to Downloads folder
    cwd = os.getcwd()
    print(f"Current working directory: {cwd}")
    
    if cwd != f"C:/Users/{name}/Downloads":
        console.print("Changing directory to Downloads folder", style="bold red")
        os.chdir(f"C:/Users/{name}/Downloads")
        cwd = os.getcwd()
        print(f"Current working directory: {cwd}")
    else:
        console.print("Already in Downloads folder", style="bold red")

def main_program_loop():

    global console
    global file_list
    while True:
        # Display the configuration
        console.print(Panel(
                title="[bold yellow]--- Configuration Menu --- [/bold yellow]",
                border_style = "bright_blue",
                renderable= "[bold white]1. View All Files\n2. List All Subdirectories\n3. List Files By Type\n4. Change Directory\n5. Organize Files By Type\n6. Delete Files By Type\n7. Delete Specific Files\n8. Move Specific Files\n9. Exit\n10. Automation[/bold white]"
                ))
        console.print("\n")

        # Get the user's choice
        choice = Prompt.ask("What would you like to do?", choices=[str(i) for i in range(1,11)])

        # View all files in the directory
        if choice == "1":
            list_all_files_in_directory()

        # List all subdirectories in the current directory
        elif choice == "2":
            list_all_subdirectories()
                
        # List files by type 
        elif choice == "3":
            list_files_by_type()
        
        # Change directory
        elif choice == "4":
            change_directory()

            # Organize files by type
        elif choice == "5":
            organize_files_by_type()

        # Delete files by type
        elif choice == "6":
            delete_files_by_type()

        # Delete specific files
        elif choice == "7":
            delete_specific_files()

        #Move specific files
        elif choice == "8":
            move_specific_files()

        # Exit the program
        elif choice == "9":
            display_goodbye_banner()
            sys.exit()
        
        # Automation - Let the program organize the files for you in the background as a running process
        elif choice == "10":
            console.print("Automation is not available yet", style="bold red")
            continue

def main(): #IN PROGRESS - NEED TO COMPLETE THE OTHER FUNCTIONS

    global console
    global file_list

    # Display the welcome banner
    display_welcome_banner()
    
    # Query the user for their name, confirm the name, and change the directory to the Downloads folder
    zug_initial_user_query()

    # Main program loop
    main_program_loop()


if __name__ == '__main__':
    main()