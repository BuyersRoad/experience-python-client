$script_type = 'Powershell.exe'
$schedule_time = $args[0]
$task_name = $args[1]
$directory_location = $args[2]
$powerbi_script_path = $args[3]
$action = New-ScheduledTaskAction -Execute $script_type -WorkingDirectory $directory_location -Argument $powerbi_script_path
$trigger = New-ScheduledTaskTrigger -Monthly -At $schedule_time -DaysOfWeek Monday 
Register-ScheduledTask $task_name -Action $action -Trigger $trigger