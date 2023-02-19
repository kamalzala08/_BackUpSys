import shutil
import os
import datetime
import hashlib
import datetime


def get_current_time():
    
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # current_time = datetime.datetime.now().strftime('%Y%m%d')
    return current_time


def backup_file(src_file, backup_dir):
    """
    Backs up a single file to the specified directory.
    Returns True if the file was backed up, False otherwise.
    """
    try:
        
        file_name = os.path.basename(src_file)
        # filename = os.path.splitext(file_name)[0]
        # extension = os.path.splitext(file_name)[1]
        
        # dest_file = os.path.join(backup_dir,filename+"_"+get_current_time()+extension)
        dest_file = os.path.join(backup_dir,file_name)

        # Check if the source file has been modified since the last backup
        if os.path.exists(dest_file):
            src_hash = get_file_hash(src_file)
            dest_hash = get_file_hash(dest_file)
            if src_hash == dest_hash:
                return False

        # Create the backup sub directory if it doesn't exist
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Copy the file to the backup directory
        shutil.copy2(src_file, dest_file)
        return True
    except Exception as e:
        print(f"Error backing up {src_file}: {e}")
        return False



def backup_files(src_dirs, backup_dir):
    """
    Backs up all files in the source directory and its subdirectories to the
    specified destination directory.
    Returns the number of files backed up.
    """
    count = 0
    try:
        # Create the root backup directory if it doesn't exist
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        for src_dir in src_dirs:
            # Create the subdirectory in the root backup directory
            sub_dir = os.path.join(backup_dir, os.path.basename(os.path.normpath(src_dir)))
            if not os.path.exists(sub_dir):
                os.makedirs(sub_dir)

            # Backup the files in the source directory and its subdirectories
            for root, dirs, files in os.walk(src_dir):
                for file_name in files:
                    src_file = os.path.join(root, file_name)
                    dest_subdir = os.path.relpath(root, src_dir)
                    new_backup_dir = os.path.join(sub_dir, dest_subdir)
                    
                    backed_up = backup_file(src_file, new_backup_dir)
                    if backed_up:
                        count += 1
                        print(f"Backed up {src_file} to {new_backup_dir}")

        print(f"Backed up {count} files at {datetime.datetime.now()}")
        return count

    except Exception as e:
        print(f"Error backing up files: {e}")
        return 0


def get_file_hash(file_path):
    """
    Returns the SHA256 hash of the specified file.
    """
    with open(file_path, 'rb') as f:
        data = f.read()
    return hashlib.sha256(data).hexdigest()


if __name__ == "__main__":

    # Set the source and destination directories
    src_dirs =["/home/kamal/Documents/COLLAGE/SEM-6/DSS/BACKUPSYS/main","/home/kamal/Documents/COLLAGE/SEM-6/DSS/BACKUPSYS/temp"]
    backup_dir = "/home/kamal/Documents/COLLAGE/SEM-6/DSS/BACKUPSYS/backup/"

    # Backup the files and print the number of files backed up
    backup_files(src_dirs, backup_dir)