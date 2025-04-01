class task_scheduler {

  # Ensure Git is installed (Manually check path instead of using Chocolatey)
  exec { 'install_git':
    command => '"C:\\Program Files\\Git\\bin\\git.exe" --version',
    path    => 'C:\\Program Files\\Git\\bin',
    onlyif  => '"C:\\Windows\\System32\\cmd.exe" /c "if exist \"C:\\Program Files\\Git\\bin\\git.exe\" echo true"',
  }

  # Ensure Python is installed (Manually specify path)
  exec { 'install_python':
    command => '"C:\\Python313\\python.exe" --version',
    path    => 'C:\\Python313',
    onlyif  => '"C:\\Windows\\System32\\cmd.exe" /c "if exist \"C:\\Python313\\python.exe\" echo true"',
  }

  # Set file permissions (Fix space issue in path & qualify cmd.exe)
  exec { 'set_permissions':
    command => '"C:\\Windows\\System32\\icacls.exe" "C:\\Users\\Manohar Reddy P\\Task-Scheduling\\task-scheduler" /grant Everyone:F /T',
    onlyif  => '"C:\\Windows\\System32\\cmd.exe" /c "if exist \"C:\\Users\\Manohar Reddy P\\Task-Scheduling\\task-scheduler\" echo true"',
  }

  # Execute the task scheduler script (Fix space issue in paths & qualify cmd.exe)
  exec { 'run_task_scheduler':
    command => '"C:\\Python313\\python.exe" "C:\\Users\\Manohar Reddy P\\Task-Scheduling\\app.py"',
    path    => 'C:\\Python313',
    timeout => 600,  # Timeout set to 10 minutes
    onlyif  => '"C:\\Windows\\System32\\cmd.exe" /c "if exist \"C:\\Users\\Manohar Reddy P\\Task-Scheduling\\app.py\" echo true"',
  }
}

include task_scheduler
