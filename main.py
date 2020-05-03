import os
import crawler

def clear_terminal():
    os.system('clear')



if __name__ == "__main__":
    clear_terminal()

    changed_folders = crawler.run()     

    print('\n\n')
    
    for folder in changed_folders:
        print(folder.is_new, folder.path)
        
        for file in folder.new_files:
            print('            ', file)
        
        print('\n \n')